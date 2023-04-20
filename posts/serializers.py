from rest_framework.serializers import ModelSerializer, SerializerMethodField, StringRelatedField
from .models import Post


class PostListSerializer(ModelSerializer):
    user = StringRelatedField(
        read_only=True,
    )
    like_users_count = SerializerMethodField(
        read_only=True,
    )
    comments_count = SerializerMethodField(
        read_only=True,
    )

    def get_like_users_count(self, post):
        return post.like_users.count()

    def get_comments_count(self, post):
        # 다른 필드들도 보여주고 싶을 때는 CommentSerializer, 또는 TinyCommentSerializer를 사용
        return post.comments.count()

    class Meta:
        model = Post
        fields = "id", "title", "content", "photo", "user", "like_users_count", "comments_count",


class PostSerializer(ModelSerializer):

    user = StringRelatedField(
        read_only=True,
    )
    comments = SerializerMethodField(
        read_only=True,
    )
    like_users = StringRelatedField(many=True,)

    def get_comments(self, post):
        # 다른 필드들도 보여주고 싶을 때는 CommentSerializer, 또는 TinyCommentSerializer를 사용
        return post.comments.all().values("content")

    class Meta:
        model = Post
        fields = "id", "user", "title", "content", "photo", "like_users", "comments",


class TinyPostSerializer(ModelSerializer):

    user = StringRelatedField(
        read_only=True,
    )

    like_users_count = SerializerMethodField(
        read_only=True,
    )

    def get_like_users_count(self, post):
        return post.like_users.count()

    class Meta:
        model = Post
        fields = "id", "user", "title", "content", "photo", "like_users_count",
