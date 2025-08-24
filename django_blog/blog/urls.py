from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, profile_view, ListView,DetailView, CreateView, UpdateView, DeleteView
import views

# URL routes for authentication & profile management
urlpatterns = [
  # Built-in login view, using custom template
  path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
  
  # Built-in logout view, using custom template
  path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
  
  # Custom registration view
  path('register/', register_view, name='register'),
  
  # Profile page (requires login)
  path('profile/', profile_view, name='profile'),

  # /post/ → list
  path("post/", ListView.as_view(), name="post-list"),
  # /post/new/ → create
  path("post/new/", CreateView.as_view(), name="post-create"),
  # /post/<pk>/ → detail
  path("post/<int:pk>/", DetailView.as_view(), name="post-detail"),
  # /post/<pk>/edit/ → update
  path("post/<int:pk>/update/", UpdateView.as_view(), name="post-update"),
  # /post/<pk>/delete/ → delete
  path("post/<int:pk>/delete/", DeleteView.as_view(), name="post-delete"),
 
  path('post/<int:pk>/comments/new/', views.CommentCreateView, name='add_comment'),
  path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='edit_comment'),
  path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),

   path('search/', views.search, name='search'),
  path('tags/<str:tag_name>/', views.TaggedPostListView.as_view(), name='tagged_posts'),
  path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='post_by_tag'),
]
