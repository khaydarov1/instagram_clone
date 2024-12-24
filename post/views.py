from .models import CommentLike, Post, PostComment, PostLike
from .serializers import PostSerializers, CommentSerializer, PostLikeSerializer, CommentLikeSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from shared.custom_pagination import CustomPagination

class PostListAPIView(generics.ListAPIView):
    serializer_class= PostSerializers
    permission_classes=[AllowAny, ]
    pagination_class=CustomPagination
    
    def get_queryset(self):
        return Post.objects.all()
    