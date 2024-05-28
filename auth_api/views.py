from rest_framework.views import APIView
from rest_framework import permissions

import os

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from rest_framework.response import Response


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = f"{os.environ.get('BASE_URL', 'http://localhost:3000')}/api/auth/callback/google"
    client_class = OAuth2Client


class GitHubLoginView(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = f"{os.environ.get('BASE_URL', 'http://localhost:3000')}/api/auth/callback/github"
    client_class = OAuth2Client


class ConnectionView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return Response({"message": "Connection successfully!"})
