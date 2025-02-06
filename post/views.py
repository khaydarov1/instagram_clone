from .models import CommentLike, Post, PostComment, PostLike
from rest_framework.response import Response
from .serializers import PostSerializers, CommentSerializer, PostLikeSerializer, CommentLikeSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from shared.custom_pagination import CustomPagination


class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializers
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.all()


class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRerieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = PostSerializers(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save
        return Response(serializer.data)

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostCommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        queryset = PostComment.objects.filter(post__id=post_id)
        return queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)
