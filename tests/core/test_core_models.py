import pytest
from django.contrib.auth import get_user_model

pytestmark = [pytest.mark.unit, pytest.mark.django_db]


def test_create_user_with_email_successfully():
    """Test creating user with email successfully"""
    email = "test@example.com"
    password = "1a9r86"
    user = get_user_model().objects.create_user(email=email, password=password)

    assert user.email == email
    assert user.check_password(password)


@pytest.mark.parametrize(
    "email, expected",
    [
        ("test1@EXAMPLE.COM", "test1@example.com"),
        ("Test2@example.com", "test2@example.com"),
        ("test_3@example.com", "test_3@example.com"),
        ("test4@EXample.COM", "test4@example.com"),
    ],
)
def test_normalize_user_email(email, expected):
    """Test normalize emails"""
    password = "1a9r86"
    user = get_user_model().objects.create_user(email=email, password=password)
    assert user.email == expected


@pytest.mark.parametrize(
    "email",
    [
        "",
        "@",
        "mati@",
        "mati@.com",
        "@example.com",
    ],
)
def test_new_user_invalid_email(email):
    """Test invalid or empty email raises error"""
    password = "1a9r86"
    with pytest.raises(ValueError):
        get_user_model().objects.create_user(email=email, password=password)


@pytest.mark.parametrize(
    "email, expected",
    [
        ("test1@EXAMPLE.COM", "test1@example.com"),
        ("Test2@example.com", "test2@example.com"),
        ("test_3@example.com", "test_3@example.com"),
        ("test4@EXample.COM", "test4@example.com"),
    ],
)
def test_create_user_without_username(email, expected):
    """Test creating user without username successfully instancing new random username"""
    password = "1a9r86"
    user = get_user_model().objects.create_user(email=email, password=password)
    assert user.username is not None


def test_create_superuser():
    """Test create superuser with password"""
    email = "test@example.com"
    password = "test1954"
    user = get_user_model().objects.create_superuser(email=email, password=password)

    assert user.is_superuser
    assert user.is_staff
