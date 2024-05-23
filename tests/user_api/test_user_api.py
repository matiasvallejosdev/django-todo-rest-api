import pytest

from rest_framework import status
from django.urls import reverse


pytestmark = [pytest.mark.e2e, pytest.mark.django_db]
USER_ME_URL = reverse("user_api:me")


def test_unautheticated_request_not_allowed(api_client):
    req = api_client.get(USER_ME_URL, format="json")
    assert req.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_me_post_not_allowed(api_client_with_credentials):
    req = api_client_with_credentials.post(USER_ME_URL, data={}, format="json")
    assert req.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_user_me_retrieve_success(api_client_with_credentials, user):
    req = api_client_with_credentials.get(USER_ME_URL, format="json")
    assert req.status_code == status.HTTP_200_OK
    assert req.data["email"] == user.email
    assert req.data["first_name"] == user.first_name
