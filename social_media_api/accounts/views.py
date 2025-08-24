from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.response import Response

from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, TokenSerializer

class RegisterView(generics.CreateAPIView):
  serializer_class = RegisterSerializer
  permission_classes = [permissions.AllowAny]

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = Token.objects.get(user=user)
    return Response({
      'user': serializer.data,
      'token': token.key
    }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
  serializer_class = LoginSerializer
  permission_classes = [permissions.AllowAny]

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(
      username=serializer.validated_data['username'],
      password=serializer.validated_data['password']
    )
    if user:
      token, created = Token.objects.get_or_create(user=user)
      return Response({'token': token.key})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class RetrieveTokenView(APIView):
  def post(self, request):
    user = request.user
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})
    

class FollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
      try:
        user_to_follow = get_user_model().objects.get(id=user_id)
        request.user.following.add(user_to_follow)
        return Response({'status': 'followed'}, status=status.HTTP_200_OK)
      except get_user_model().DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class UnfollowUserView(generics.GenericAPIView):
  queryset = CustomUser.objects.all()
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request, user_id):
    try:
      user_to_unfollow = get_user_model().objects.get(id=user_id)
      request.user.following.remove(user_to_unfollow)
      return Response({'status': 'unfollowed'}, status=status.HTTP_200_OK)
    except get_user_model().DoesNotExist:
      return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)