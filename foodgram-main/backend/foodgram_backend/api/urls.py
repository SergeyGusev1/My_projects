from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework_nested import routers

from api import views

app_name = 'api'

main_router = routers.DefaultRouter()
main_router.register('recipes', views.RecipeViewSet, basename='recipes')
main_router.register('tags', views.TagViewSet, basename='tags')
main_router.register('ingredients', views.IngredientViewSet,
                     basename='ingredients')
main_router.register('users', views.UserViewSet, basename='users')

recipes_router = routers.NestedDefaultRouter(main_router,
                                             'recipes', lookup='recipe')


urlpatterns = [
    path('recipes/<int:pk>/edit', RedirectView.as_view(
        url='/api/recipes/%(pk)s/edit/',
        permanent=False
    )),
    path('', include(main_router.urls)),
    path('', include(recipes_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
