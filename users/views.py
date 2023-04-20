from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser
from .serializers import UserSerializer, UserDetailSerializer,  CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class Users(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, id):
        return get_object_or_404(CustomUser, id=id)

    def get(self, request, id):
        user = self.get_object(id)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        user = self.get_object(id)
        serializer = UserDetailSerializer(
            user, data=request.data, partial=True,)
        if serializer.is_valid():
            user = serializer.save()
            serializer = UserDetailSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = self.get_object(id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserFollowings(APIView):
    # permission_classes=[IsAuthenticated]

    def post(self, request, id):
        you = get_object_or_404(CustomUser, id=id)
        me = request.user
        if me in you.following.all():
            you.following.remove(me.id)
            return Response("팔로우를 취소했습니다.", status=status.HTTP_200_OK)
        else:
            you.following.add(me.id)
            return Response("팔로우 했습니다.", status=status.HTTP_200_OK)


class Home(APIView):
    def get(self, request):
        return render(request, "home.html")


class Signup(APIView):
    def get(self, request):
        return render(request, "users/signup.html")


class Login(APIView):
    def get(self, request):
        return render(request, "users/login.html")
