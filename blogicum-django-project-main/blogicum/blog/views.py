from blog.models import Category, Comment, Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .forms import CommentForm, ProfileUpdateForm


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


def index(request):
    post_list = Post.objects.select_related(
        'category', 'location'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if (
            (post.is_published
             and post.category.is_published
             and post.pub_date < timezone.now())
            or (self.request.user.is_authenticated
                and post.author == self.request.user)
        ):
            return post
        raise Http404('Страница не найдена')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


def category_posts(request, category):
    category_object = get_object_or_404(
        Category,
        slug=category,
        is_published=True
    )
    post_list = Post.objects.select_related(
        'category'
    ).filter(
        is_published=True,
        category__slug__exact=category,
        pub_date__lte=timezone.now(),
        category__is_published__exact=True
    )
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'category': category_object
    }
    return render(request, 'blog/category.html', context)


class BlogProfileDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()
        if object == self.request.user:
            posts = Post.objects.filter(
                author=self.object.id
            )
        else:
            posts = Post.objects.filter(
                author=self.object.id,
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now()
            ).annotate(
                comment_count=Count('comments')
            ).order_by('-pub_date')
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class ProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self, quertyset=None):
        return self.request.user


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'text', 'pub_date', 'location', 'category', 'image')
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('blog:profile', kwargs={'username': username})


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    fields = ('title', 'text', 'pub_date', 'location', 'category', 'image')
    template_name = 'blog/create.html'

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('blog:profile', kwargs={'username': username})

    def handle_no_permission(self):

        return redirect(reverse(
            'blog:post_detail',
            kwargs={'post_id': self.get_object().pk})
        )


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('blog:profile', kwargs={'username': username})


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=pk)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post_id)
    else:
        form = CommentForm(instance=comment)
    return render(
        request,
        'blog/comment.html',
        {'form': form, 'comment': comment}
    )


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(
        request,
        'blog/comment.html',
        {'comment': comment}
    )
