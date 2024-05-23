import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(
        email="matiasvallejos@outlook.com", password="myuserpsasword"
    )


@pytest.fixture
def user2():
    User = get_user_model()
    return User.objects.create_user(
        email="abelardovallejos@outlook.com", password="myuserpsasword"
    )


@pytest.fixture
def api_client_with_credentials(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client
