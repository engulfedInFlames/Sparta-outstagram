from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.template_urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/articles/", include("articles.urls")),
    path("api/token/", views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
