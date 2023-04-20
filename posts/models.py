from django.db import models
from django.conf import settings


class Post(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    title = models.CharField(max_length=120)
    content = models.TextField()

    # ImageField는 NULL이 되지 않는다.
    photo = models.ImageField(blank=True, upload_to="%y/%m/%d")
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="like_posts",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.title)
