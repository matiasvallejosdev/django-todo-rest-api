import pytest
from core.utils import check_email, is_valid_uuid

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    "email, expected",
    [
        ("matias@vallejos.com", True),
        ("noemail", False),
        ("matias@vallejos", False),
        ("matiasvallejos.com", False),
        ("", False),
        ("@", False),
        ("mati@", False),
        ("@example.com", False),
    ],
)
def test_check_email(email: str, expected: bool):
    assert check_email(email) == expected


@pytest.mark.parametrize(
    "uuid, expected",
    [
        ("123e4567-e89b-12d3-a456-426614174000", True),
        ("123e4567-e89b-12d3-a456-4266141740", False),
        ("123e4567-e89b-12d3-a456-4266141740000", False),
    ],
)
def test_is_valid_uuid(uuid: str, expected: bool):
    assert is_valid_uuid(uuid) == expected
