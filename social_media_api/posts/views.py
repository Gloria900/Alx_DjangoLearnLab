from rest_framework import viewsets, permissions, filters, generics
from rest_framework.pagination import PageNumberPagination

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification

class IsAuthorOrReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    return obj.author == request.user

class StandardResultsSetPagination(PageNumberPagination):
  page_size = 10
  page_size_query_param = 'page_size'
  max_page_size = 50

class PostViewSet(viewsets.ModelViewSet):
  queryset = Post.objects.all().order_by('-created_at')
  serializer_class = PostSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
  pagination_class = StandardResultsSetPagination
  filter_backends = [filters.SearchFilter]
  search_fields = ['title', 'content']

  def perform_create(self, serializer):
    serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
  queryset = Comment.objects.all().order_by('-created_at')
  serializer_class = CommentSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
  pagination_class = StandardResultsSetPagination

  def perform_create(self, serializer):
    serializer.save(author=self.request.user)

# implement feeds for post
class FeedView(APIView):
  permission_classes = [IsAuthenticated]
  
  def get(self, request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    feed_data = [
      {
        "id": posts.id,
        "author": posts.author.username,
        "title": posts.title,
        "content": posts.content,
        "created_at": posts.created_at,
      }
      for post in posts
    ]
    return Response(feed_data)
  

class LikePostView(APIView):
  permission_classes = [IsAuthenticated]
  
  def post(self, request, pk):
    post = generics.get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if created:
      # create a notification for the post's author
      if post.author != request.user:
        Notification.objects.create(
          recipient=post.author,
          actor = request.user,
          verb='liked your post',
          target=post,
        )
      return Response({'message': 'Post liked successfuly!'})
    else:
      return Response({'message': 'you already liked this post.'}, status=400)
    
class UnlikePostView(APIView):
  permission_classes = [IsAuthenticated]
  
  def post(self, request, pk):
    post = generics.get_object_or_404(Post, pk=pk)
    like = Like.objects.filter(user=request.user, post=post)
    
    if like.exists():
      like.delete()
      return Response({'message': 'Post unliked successfully!'})
    else:
      return Response({'message': 'You have not liked this post yet.'}, status=400)