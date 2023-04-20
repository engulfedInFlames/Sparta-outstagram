from django.shortcuts import render, get_object_or_404
from django.db.models.query_utils import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status

from .models import Post
from comments.models import Comment
from .serializers import PostSerializer, PostListSerializer
from comments.serializers import CommentSerializer


class Posts(APIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.all()
        serilaizer = PostListSerializer(posts, many=True)
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
    # permission_classes = [IsAuthenticatedOrReadOnly]

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


class Feeds(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Q objects
        q = Q()
        for user in request.user.followings.all():
            q.add(Q(user=user), q.OR)
        feeds = Post.objects.filter(q)
        serilaizer = PostListSerializer(feeds, many=True)
        return Response(serilaizer.data)


class PostComments(APIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        return get_object_or_404(Post, id=id)

    def get(self, request, id):
        post = self.get_object(id)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(
                user=request.user,
                post_id=id,
            )
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_201_CREATED)


class PostLikes(APIView):
    # permission_classes=[IsAuthenticated]

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        user = request.user
        like_user = post.like_user
        print(user)
        if user in like_user.all():
            like_user.remove(user.id)
            return Response("좋아요를 취소했습니다.", status=status.HTTP_200_OK)
        else:
            like_user.add(user.id)
            return Response("좋아요를 했습니다.", status=status.HTTP_200_OK)
