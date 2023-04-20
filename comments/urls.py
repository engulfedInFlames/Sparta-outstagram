from django.urls import path
from . import views

urlpatterns = [
    path("", views.Comments.as_view(), ),
    path("<int:id>/", views.CommentDetail.as_view(), ),
]
