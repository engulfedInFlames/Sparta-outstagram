from django.urls import path
from . import views

urlpatterns = [
    path("", views.Posts.as_view(), name="all_posts"),
    path("<int:id>", views.PostDetail.as_view(), name="only_one_post"),
]
