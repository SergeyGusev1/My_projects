import short_url
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count, F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from api.filters import RecipeFilter, SearchFilter
from api.serializers import (
    FavoriteSerializer,
    IngredientSerilizer,
    RecipeListSerialzer,
    RecipePostSerializer,
    ShoppingCartSerializer,
    SubscriptionCreateSerializer,
    SubscriptionSerializer,
    TagSerializer,
    UserAvatarSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import Subscription, User

from .permission import IsAuthorOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerilizer
    permission_class = (AllowAny, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = SearchFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter]
    filterset_class = RecipeFilter
    ordering_fields = ['-created', 'cooking_time', 'name']
    search_fields = ['name', 'description', 'author__username']

    def get_queryset(self):
        queryset = Recipe.objects.all().annotate(
            favorites_count=Count('favorites', distinct=True),
            shopping_carts_count=Count('shopping_carts', distinct=True)
        ).select_related(
            'author'
        ).prefetch_related(
            'tags',
            'ingredients'
        )
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['put', 'patch'], url_path='edit')
    def edit_recipe(self, request, pk=None):
        instance = self.get_object()

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            instance,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='get-link')
    def get_short_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        short_code = short_url.encode_url(recipe.id)
        domain = request.build_absolute_uri('/')[:-1]
        short_link = f'{domain}/s/{short_code}'
        return Response(
            {'short-link': short_link},
            status=status.HTTP_200_OK
        )

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeListSerialzer
        return RecipePostSerializer

    @action(detail=False, methods=['get'], url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        user = request.user

        shopping_cart_items = (ShoppingCart.objects.
                               filter(user=user).select_related('recipe'))

        if not shopping_cart_items.exists():
            return Response(
                {'error': 'Корзина пуста'},
                status=status.HTTP_400_BAD_REQUEST
            )

        ingredients_data = self._get_shopping_cart_ingredients(user)

        file_content = self._generate_shopping_list_txt(ingredients_data)

        response = HttpResponse(
            file_content,
            content_type='text/plain; charset=utf-8'
        )
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"'
        )
        return response

    def _get_shopping_cart_ingredients(self, user):
        return (IngredientInRecipe.objects
                .filter(recipe__shopping_carts__user=user)
                .values(
                    name=F('ingredient__name'),
                    unit=F('ingredient__measurement_unit')
                )
                .annotate(total_amount=Sum('amount'))
                .order_by('name'))

    def _generate_shopping_list_txt(self, ingredients_data):
        content = 'Список покупок\n\n'
        for item in ingredients_data:
            content += (
                f"• {item['name']}: {item['total_amount']} {item['unit']}\n"
            )
        return content

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        """Добавить/удалить рецепт в избранное"""
        recipe = self.get_object()
        user = request.user

        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'error': 'Рецепт уже в избранном'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FavoriteSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            deleted_count, _ = Favorite.objects.filter(
                user=user,
                recipe=recipe
            ).delete()
            if deleted_count == 0:
                return Response(
                    {'error': 'Рецепт не найден в избранном'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'error': 'Рецепт уже в корзине'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'error': 'Рецепт уже в корзине'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = ShoppingCartSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            deleted_count, _ = ShoppingCart.objects.filter(
                user=user, recipe=recipe
            ).delete()
            if deleted_count == 0:
                return Response(
                    {'error': 'Рецепта нет в корзине'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['subscribe', 'avatar', 'set_password', 'me']:
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(detail=False, methods=['post'], url_path='set_password')
    def set_password(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not current_password or not new_password:
            return Response(
                {'error': 'Требуется current_password и new_password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(current_password):
            return Response(
                {'current_password': 'Неверный текущий пароль'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['put', 'delete'], url_path='me/avatar')
    def avatar(self, request):
        user = request.user

        if request.method == 'PUT':
            serializer = UserAvatarSerializer(user, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            if user.avatar:
                user.avatar.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(
                {'detail': 'Аватар не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        return Response(self.get_serializer(request.user).data)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated], url_path='subscribe')
    def subscribe(self, request, pk=None):

        author = get_object_or_404(User, pk=pk)
        user = request.user
        if request.method == 'POST':
            serializer = SubscriptionCreateSerializer(
                data={'author': author.id},
                context={'request': request}
            )
            if serializer.is_valid():
                subscribe = Subscription.objects.create(
                    user=user,
                    author=author
                )
                subscribe.save()
                return Response(f'Вы подписались на {author}',
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            deleted_count, _ = Subscription.objects.filter(
                user=user, author=author
            ).delete()
            if deleted_count == 0:
                return Response(
                    {'error': 'Вы не подписаны на этого пользователя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(request.method, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user

        author_ids = Subscription.objects.filter(
            user=user
        ).values_list('author_id', flat=True)

        subscribed_authors = User.objects.filter(
            id__in=author_ids
        ).annotate(
            recipes_count=Count('recipes')
        ).order_by('id')

        page = self.paginate_queryset(subscribed_authors)
        serializer = SubscriptionSerializer(page, many=True,
                                            context={'request': request})
        return self.get_paginated_response(serializer.data)
