from django.urls import path
from . import views

urlpatterns = [
    path("", views.Comments.as_view(), name="all_comments"),
    path("<int:id>", views.CommentDetail.as_view(), name="only_one_comment"),
]
