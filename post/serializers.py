from rest_framework import serializers

from post.models import CommentLike, Post, PostComment, PostLike
from users.models import User


class UserSerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'photo')


class PostSerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializers(read_only=True)
    post_likes_count = serializers.SerializerMethodField('get_post_likes_count')
    post_comments_count = serializers.SerializerMethodField('get_post_comments_count')
    me_liked = serializers.SerializerMethodField('get_me_liked')

    class Meta:
        model = Post
        fields = ('id', 'author', 'image', 'caption', 'created_at','post_likes_count', 'post_comments_count', 'me_liked')
        exrta_kwargs = {'image': {'required': False}}
    @staticmethod
    def get_post_likes_count(obj):
        return obj.likes.count()

    @staticmethod
    def get_post_comments_count(obj):
        return obj.comments.count()

    def get_me_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                PostLike.objects.get(post=obj, author=request.user)
                return True
            except PostLike.DoesNotExist:
                return False

        return False


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializers(read_only=True)
    replies = serializers.SerializerMethodField('get_replies')
    me_liked = serializers.SerializerMethodField('get_me_liked')
    likes_count = serializers.SerializerMethodField('get_likes_count')

    class Meta:
        model = PostComment
        fields = ('id', 'author', 'comment', "parent", 'created_time', 'replies')

    def get_replies(self, obj):
        if obj.child.exists():
            serializer = self.__class__(obj.child.all(), many=True, context=self.context)
            return serializer.data
        else:
            return None

    def get_me_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(author=user).exists()
        else:
            return False

    @staticmethod
    def get_likes_count(obj):
        return obj.likes.count()


class PostLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializers(read_only=True)

    class Meta:
        model = PostLike
        fields = ("id", 'author', 'post',)


class CommentLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializers(read_only=True)
    comment = CommentSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = ('id', 'author', 'comment',)
