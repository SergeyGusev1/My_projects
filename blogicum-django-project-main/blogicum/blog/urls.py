from blog import views
from django.contrib.auth.decorators import login_required
from django.urls import path

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'category/<slug:category>/',
        views.category_posts,
        name='category_posts'
    ),
    path(
        'profile/<slug:username>/',
        views.BlogProfileDetailView.as_view(),
        name='profile'
    ),
    path(
        'edit_profile/',
        login_required(views.ProfileUpdateView.as_view()),
        name='edit_profile'
    ),
    path(
        'posts/create/',
        views.PostCreateView.as_view(),
        name='create_post'
    ),
    path(
        'posts/<int:pk>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:pk>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post'
    ),
    path('<int:pk>/comment', views.add_comment, name='add_comment'),
    path(
        'posts/<int:post_id>/comment/<int:comment_id>/edit_comment/',
        views.edit_comment,
        name='edit_comment'
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.delete_comment,
        name='delete_comment',
    ),
]
