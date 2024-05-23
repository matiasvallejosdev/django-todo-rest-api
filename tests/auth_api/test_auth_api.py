import pytest

from rest_framework import status
from django.urls import reverse


pytestmark = [pytest.mark.e2e, pytest.mark.django_db]
CONNECTION_URL = reverse("auth_api:connection")


def test_unauthenticated_connection(api_client):
    res = api_client.post(CONNECTION_URL, data={}, format="json")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_authenticadted_connection(api_client_with_credentials, user):
    api_client_with_credentials.force_authenticate(user=user)
    res = api_client_with_credentials.post(CONNECTION_URL, data={}, format="json")
    assert res.status_code == status.HTTP_200_OK
    assert res.data == {"message": "Connection successfully!"}
