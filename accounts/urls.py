from django.contrib import admin
from django.urls import path

from accounts.views import (
    CustomTokenObtainPairView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/token/",
        CustomTokenObtainPairView.as_view()
    ),
]
