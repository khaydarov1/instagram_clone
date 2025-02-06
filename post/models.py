from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, MaxLengthValidator
from shared.models import BaseModel

User = get_user_model()


class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='post_images', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    caption = models.TextField(validators=[MaxLengthValidator(2000)])

    class Meta:
        db_table = 'posts'
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ['-created_time']


class PostComment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(validators=[MaxLengthValidator(2000)])
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='child',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.author


class PostLike(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'post'],
                                    name='unique_post_like')
        ]


class CommentLike(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='comment_likes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'comment'],
                                    name='unique_comment_like')
        ]
