from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Comment


class CommentSerializer(ModelSerializer):

    user = SerializerMethodField(
        read_only=True
    )

    post = SerializerMethodField(
        read_only=True
    )

    def get_user(self, comment):
        return comment.user.email

    def get_post(self, comment):
        return comment.post.title

    class Meta:
        model = Comment
        fields = "id", "content", "user", "post",
