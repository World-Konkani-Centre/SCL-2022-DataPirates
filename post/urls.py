from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    SubPostCreateView,
)
from . import views
from django.urls import re_path

urlpatterns = [
    path('', views.following_posts, name='user-home'),
    path('new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path("post/<int:pk>/" + "#".format() + "comments", PostDetailView.as_view(), name='post-detail-comment'),
    path('update/<int:pk>/', views.postUpdateView, name='post-update'),
    path('delete/<int:pk>/', views.deletePost, name='post-delete'),
    path('post/<int:pk>/subpost/new/',
         SubPostCreateView.as_view(), name="subpost-create"),
    path('post/<int:pk>/subpost/<int:id>/update/',
         views.updateSubpost, name="subpost-update"),
    path('post/<int:pk>/subpost/<int:id>/delete/',
         views.deleteSubpost, name="subpost-delete"),
    path('search/', views.search, name='search'),
    path('post/<int:pk>/postComment/', views.postComment, name="postComment"),
    path('post/<int:pk>/star/', views.star, name="postStar"),
    path('stars/', views.starlist, name="stars"),
    path('categories/<slug:slug>/', views.categoryList, name='category'),
    path('flow/', PostListView.as_view(), name='landing-page'),
     path('explore/', views.explore, name='explore'),
]

