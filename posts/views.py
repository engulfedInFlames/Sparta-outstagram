from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status

from .models import Post
from .serializers import PostSerializer


class Posts(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serilaizer = PostSerializer(posts, many=True)
        return Response(serilaizer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            post = serializer.save(user=request.user)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    def get_object(self, id):
        return get_object_or_404(Post, id=id)

    def get(self, request, id):
        post = self.get_object(id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, id):
        post = self.get_object(id)
        serializer = PostSerializer(
            post,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            post = serializer.save()
            serializer = PostSerializer(post)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        post = self.get_object(id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
