import pytest
from rest_framework import status
from django.urls import reverse

pytestmark = [pytest.mark.django_db, pytest.mark.ai]

AUTOCOMPLETE_URL = reverse("ai_api:autocomplete")


def test_ai_autocomplete(api_client_with_credentials):
    params = {"input_text": "The quick brown fox jumps over the lazy dog."}
    res = api_client_with_credentials.get(AUTOCOMPLETE_URL, params)

    assert res.status_code == status.HTTP_200_OK
    assert "text" in res.data, "Response does not contain 'text' key"
    assert len(res.data["text"]) > 0, "Response 'text' is empty"
