from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view(), name="all_users"),
    path("<int:id>/", views.UserDetail.as_view(), name="only_one_user"),
    path("<int:id>/followings/", views.UserFollowings.as_view(),
         name="all_followings"),
]
