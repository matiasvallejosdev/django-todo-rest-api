import pytest

from model_bakery import baker
from rest_framework import status
from django.urls import reverse

from todo_api.models import TaskList

pytestmark = [pytest.mark.e2e, pytest.mark.django_db]
LISTS_URL = reverse("todo_api:lists-list")


def test_unauthenticated_connection(api_client):
    res = api_client.get(LISTS_URL)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def tasks_detail_url(list_uuid):
    return reverse("todo_api:lists-detail", kwargs={"list_uuid": list_uuid})


def test_list_task_lists(api_client_with_credentials, user):
    baker.make(TaskList, created_by=user, _quantity=5)

    res = api_client_with_credentials.get(LISTS_URL)

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 5


def test_list_task_lists_limited_to_user(api_client_with_credentials, user2):
    baker.make(TaskList, created_by=user2, _quantity=5)
    res = api_client_with_credentials.get(LISTS_URL)
    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 0


def test_retrieve_list(api_client_with_credentials, user):
    list = baker.make(TaskList, created_by=user)
    res = api_client_with_credentials.get(tasks_detail_url(list.list_uuid))
    assert res.status_code == status.HTTP_200_OK
    assert res.data["list_uuid"] == str(list.list_uuid)
    assert res.data["name"] == list.name


def test_retrieve_list_not_found(api_client_with_credentials, user):
    baker.make(TaskList, created_by=user)
    res = api_client_with_credentials.get(tasks_detail_url("not-found"))
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_retrieve_list_limited_to_user(api_client_with_credentials, user2):
    list = baker.make(TaskList, created_by=user2)
    res = api_client_with_credentials.get(tasks_detail_url(list.list_uuid))
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_retrieve_inbox_list_not_found(api_client_with_credentials, user):
    baker.make(TaskList, created_by=user, name="inbox")
    res = api_client_with_credentials.get(tasks_detail_url("inbox"))
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_create_list(api_client_with_credentials, user):
    payload = {"name": "New List"}
    res = api_client_with_credentials.post(LISTS_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == payload["name"]


def test_create_list_invalid(api_client_with_credentials, user):
    payload = {"name": ""}
    res = api_client_with_credentials.post(LISTS_URL, payload)
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_update_list(api_client_with_credentials, user):
    list = baker.make(TaskList, created_by=user)
    payload = {"name": "Updated List"}
    res = api_client_with_credentials.patch(tasks_detail_url(list.list_uuid), payload)
    assert res.status_code == status.HTTP_200_OK
    assert res.data["name"] == payload["name"]


def test_invalid_update_list(api_client_with_credentials, user):
    list = baker.make(TaskList, created_by=user)
    payload = {"name": ""}
    res = api_client_with_credentials.patch(tasks_detail_url(list.list_uuid), payload)
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_update_list_limited_to_user(api_client_with_credentials, user2):
    list = baker.make(TaskList, created_by=user2)
    payload = {"name": "Updated List"}
    res = api_client_with_credentials.patch(tasks_detail_url(list.list_uuid), payload)
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_list(api_client_with_credentials, user):
    list = baker.make(TaskList, created_by=user)
    res = api_client_with_credentials.delete(tasks_detail_url(list.list_uuid))
    assert res.status_code == status.HTTP_204_NO_CONTENT
    assert not TaskList.objects.filter(list_uuid=list.list_uuid).exists()


def test_delete_list_not_found(api_client_with_credentials, user):
    baker.make(TaskList, created_by=user)
    res = api_client_with_credentials.delete(tasks_detail_url("not-found"))
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert TaskList.objects.count() == 1


def test_delete_list_limited_to_user(api_client_with_credentials, user2):
    list = baker.make(TaskList, created_by=user2)
    res = api_client_with_credentials.delete(tasks_detail_url(list.list_uuid))
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert TaskList.objects.count() == 1
