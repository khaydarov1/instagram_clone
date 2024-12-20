from rest_framework import serializers

from post.models import Post, PostLike
from users.models import User

class UserSerializers(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    
    
    class Meta:
        model = User
        fields = ('id','username','photo')

class PostSerializers(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    author=UserSerializers(read_only=True)
    post_likes_count=serializers.SerializerMethodField('get_post_likes_count')
    post_comments_count=serializers.SerializerMethodField('get_post_comments_count')
    me_liked=serializers.SerializerMethodField('get_me_liked')
    
    
    class Meta:
        model = Post
        fields = ('id', 'author', 'image', 'caption', 'created_at', 'post_likes', 'post_comments_count', 'me_liked')
    
    def get_post_likes_count(self,obj):
        return obj.likes.count()
    
    def get_post_comments_count(self,obj):
        return obj.comments.count()
    
    def get_me_liked(self,obj):
        request=self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                like=PostLike.objects.get(post=obj,author=request.user)
                return True
            except PostLike.DoesNotExist:
                return False
    
        return False