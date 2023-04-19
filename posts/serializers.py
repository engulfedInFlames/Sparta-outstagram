from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Post


class PostSerializer(ModelSerializer):

    user = SerializerMethodField(
        read_only=True
    )

    def get_user(self, object):
        return object.user.email

    class Meta:
        model = Post
        fields = "id", "title", "content", "photo", "user"
