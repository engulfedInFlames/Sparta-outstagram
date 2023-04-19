from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Comment
from .serializers import CommentSerializer


class Comments(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serilaizer = CommentSerializer(comments, many=True)
        return Response(serilaizer.data)

    def post(self, request):
        pass


class CommentDetail(APIView):
    def get_object(self, id):
        return get_object_or_404(Comment, id=id)

    def get(self, request, id):
        post = self.get_object(id)
        pass

    def put(self, request, id):
        post = self.get_object(id)
        pass

    def delete(self, request, id):
        post = self.get_object(id)
        pass
