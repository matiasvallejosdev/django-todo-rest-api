from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("todo_api.urls"), name="task"),
    path("api/user/", include("user_api.urls"), name="user"),
    path("api/auth/", include("auth_api.urls"), name="auth"),
    path("api/ai/", include("ai_api.urls"), name="ai"),
    path("accounts/", include("allauth.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
