from django.contrib import admin
from .models import Post, PostLike, PostComment, CommentLike


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'caption', 'created_time')
    search_fields = ('id','caption', 'author__username')
    list_filter = ('created_time',)


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'comment', 'created_time')
    search_fields = ('id', 'comment', 'author__username')



class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author')
    search_fields = ('id', 'author__username')
    
    
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'author', 'created_time')
    search_fields = ('id', 'author__username')
    
admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)