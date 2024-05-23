"""
Tests for the Django admin modifications.
"""

import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def admin_user(db):
    user = get_user_model().objects.create_superuser(
        email="admin@example.com", password="testpass123"
    )
    return user


@pytest.fixture
def sample_user(db):
    payload = {
        "email": "user@example.com",
        "password": "testpass123",
        "first_name": "User",
        "last_name": "Test",
    }
    return get_user_model().objects.create_superuser(**payload)


@pytest.fixture
def authenticated_client(client, admin_user):
    client.force_login(user=admin_user)
    return client


def test_list_users_page(authenticated_client, sample_user):
    """Test that users are listed on page."""
    url = reverse("admin:core_user_changelist")
    res = authenticated_client.get(url)
    assert sample_user.first_name in res.content.decode()
    assert sample_user.last_name in res.content.decode()
    assert sample_user.email in res.content.decode()


def test_edit_user_page(authenticated_client, sample_user):
    """Test editing user on page."""
    url = reverse("admin:core_user_change", args=[sample_user.userId])
    res = authenticated_client.get(url)
    assert res.status_code == 200


def test_create_user_page(authenticated_client):
    url = reverse("admin:core_user_add")
    res = authenticated_client.get(url)
    assert res.status_code == 200
