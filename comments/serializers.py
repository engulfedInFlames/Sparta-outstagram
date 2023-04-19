from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Comment


class CommentSerializer(ModelSerializer):

    user = SerializerMethodField()

    def get_user(self, object):
        return object.user.email

    class Meta:
        model = Comment
        fields = "id", "content", "user",
