from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status

from .models import Comment
from .serializers import CommentSerializer


class Comments(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serilaizer = CommentSerializer(comments, many=True)
        return Response(serilaizer.data)


class CommentDetail(APIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        return get_object_or_404(Comment, id=id)

    def get(self, request, id):
        comment = self.get_object(id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, id):
        comment = self.get_object(id)
        serializer = CommentSerializer(
            comment,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            comment = serializer.save()
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        comment = self.get_object(id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
