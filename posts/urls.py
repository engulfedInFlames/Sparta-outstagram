from django.urls import path
from . import views

urlpatterns = [
    path("", views.Posts.as_view(), name="all_posts"),
    path("feed/", views.Feeds.as_view(), name="all_feed_posts"),
    path("<int:id>/", views.PostDetail.as_view(), name="only_one_post"),
    path("<int:id>/comments/", views.PostComments.as_view(), name="all_comments"),
    path("<int:id>/likes/", views.PostLikes.as_view(), name="all_likes"),
]
