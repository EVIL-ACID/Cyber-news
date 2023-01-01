from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.


class Post(models.Model):
    post_author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    post_title = models.CharField(max_length=100)
    post_link = models.URLField()
    post_text = models.TextField(blank=True)
    post_points = models.PositiveIntegerField(default=0)
    post_date = models.DateTimeField(auto_now_add=True)



class Comment(MPTTModel):
    
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'    
    )
    comment_author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)
    comment_points = models.PositiveIntegerField(default=0)

    # class MPTTMeta:
    #     order_insertion_by = ['comment_date']

class upVote(models.Model):
    upvote_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    upvote_post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE)
