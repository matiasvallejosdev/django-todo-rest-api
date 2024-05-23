import pytest

from model_bakery import baker
from rest_framework import status
from django.urls import reverse

from todo_api.models import Task, TaskList

pytestmark = [pytest.mark.e2e, pytest.mark.django_db]
TASKS_URL = reverse("todo_api:tasks-list")
TASKS_DETAIL_URL = "todo_api:tasks-detail"
TASKS_COUNT_URL = reverse("todo_api:tasks-count")


def tasks_detail_url(task_uuid):
    return reverse(TASKS_DETAIL_URL, kwargs={"task_uuid": task_uuid})


def test_unauthenticated_connection(api_client):
    res = api_client.get(TASKS_URL)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_tasks(api_client_with_credentials, user):
    list = baker.make(TaskList, created_by=user)
    baker.make(Task, created_by=user, task_list=list, _quantity=5)

    res = api_client_with_credentials.get(TASKS_URL)

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 5


def test_list_task_limited_to_user(api_client_with_credentials, user, user2):
    list = baker.make(TaskList, created_by=user)
    baker.make(Task, created_by=user, task_list=list, _quantity=5)
    baker.make(Task, created_by=user2, _quantity=5)

    res = api_client_with_credentials.get(TASKS_URL)

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 5


def test_list_task_by_list_uuid(api_client_with_credentials, user):
    list = baker.make(TaskList, created_by=user)
    baker.make(Task, created_by=user, task_list=list, _quantity=3)
    baker.make(Task, created_by=user, _quantity=5)

    res = api_client_with_credentials.get(f"{TASKS_URL}?list={list.list_uuid}")

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 3


def test_list_task_by_upcoming(api_client_with_credentials, user):
    list = baker.make(TaskList, created_by=user)
    baker.make(Task, created_by=user, task_list=list, _quantity=5)
    baker.make(Task, created_by=user, _quantity=5)
    baker.make(Task, created_by=user, _quantity=3, due_date="2021-01-01T00:00:00Z")

    res = api_client_with_credentials.get(f"{TASKS_URL}?list=upcoming")

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 3


def test_list_task_by_inbox(api_client_with_credentials, user):
    list = baker.make(TaskList, created_by=user, name="inbox")
    baker.make(Task, created_by=user, task_list=list, _quantity=2)
    baker.make(Task, created_by=user, _quantity=5, task_list=None)

    res = api_client_with_credentials.get(f"{TASKS_URL}?list=inbox")

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 5


def test_retrieve_task(api_client_with_credentials, user):
    task = baker.make(Task, created_by=user)

    res = api_client_with_credentials.get(tasks_detail_url(task.task_uuid))

    assert res.status_code == status.HTTP_200_OK
    assert res.data["title"] == task.title


def test_retrieve_task_limited_to_user(api_client_with_credentials, user, user2):
    task = baker.make(Task, created_by=user2)

    res = api_client_with_credentials.get(tasks_detail_url(task.task_uuid))

    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.data == {"detail": "Not found."}


def test_create_task_valid(api_client_with_credentials, user):
    list = baker.make(TaskList, created_by=user)
    task = baker.prepare(Task, created_by=user, task_list=list)
    payload = {
        "title": task.title,
        "completed": task.completed,
        "task_list": list.list_uuid,
        "due_date": "2021-01-01T00:00:00Z",
        "created_by": user.id,
    }

    res = api_client_with_credentials.post(TASKS_URL, data=payload, format="json")

    assert res.status_code == status.HTTP_201_CREATED

    print(res.data)
    assert res.data.get("title") == payload["title"]
    assert res.data.get("completed") == payload["completed"]
    assert str(res.data.get("task_list")) == str(payload["task_list"])
    assert res.data.get("due_date") == payload["due_date"]


def test_create_task_invalid(api_client_with_credentials, user):
    task = baker.prepare(Task, created_by=user)
    payload = {"title": "", "completed": task.completed, "created_by": user.id}

    res = api_client_with_credentials.post(TASKS_URL, data=payload, format="json")

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.data == {"title": ["This field may not be blank."]}


def test_delete_task_success(api_client_with_credentials, user):
    task = baker.make(Task, created_by=user)

    res = api_client_with_credentials.delete(tasks_detail_url(task.task_uuid))

    assert res.status_code == status.HTTP_204_NO_CONTENT
    assert Task.objects.count() == 0


def test_delete_task_limited_to_user(api_client_with_credentials, user, user2):
    task = baker.make(Task, created_by=user2)

    res = api_client_with_credentials.delete(tasks_detail_url(task.task_uuid))

    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert Task.objects.count() == 1


def test_update_task(api_client_with_credentials, user):
    task = baker.make(Task, created_by=user)
    payload = {"title": "New title", "completed": True}

    res = api_client_with_credentials.patch(
        tasks_detail_url(task.task_uuid),
        data=payload,
        format="json",
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["title"] == payload["title"]
    assert res.data["completed"] == payload["completed"]


def test_partial_update_task(api_client_with_credentials, user):
    task = baker.make(Task, created_by=user)
    payload = {"due_date": "2021-01-01T00:00:00Z"}

    res = api_client_with_credentials.patch(
        tasks_detail_url(task.task_uuid),
        data=payload,
        format="json",
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["due_date"] == payload["due_date"]
    assert res.data["completed"] == task.completed


def test_update_limited_to_user(api_client_with_credentials, user, user2):
    task = baker.make(Task, created_by=user2)
    payload = {"title": "New title", "completed": True}

    res = api_client_with_credentials.patch(
        tasks_detail_url(task.task_uuid),
        data=payload,
        format="json",
    )

    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert Task.objects.count() == 1
    assert Task.objects.get().title != payload["title"]
    assert Task.objects.get().completed != payload["completed"]


def test_count_tasks_valid(api_client_with_credentials, user):
    # Test with UUID
    task_list = baker.make(TaskList, created_by=user)
    baker.make(Task, created_by=user, task_list=task_list, _quantity=2, completed=True)
    baker.make(Task, created_by=user, task_list=task_list, _quantity=3, completed=False)

    res = api_client_with_credentials.get(
        f"{TASKS_COUNT_URL}?list={task_list.list_uuid}"
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["total"] == 5
    assert res.data["completed"] == 2
    assert res.data["pending"] == 3


def test_count_upcoming_tasks_valid(api_client_with_credentials, user):
    task_list = baker.make(TaskList, created_by=user)
    baker.make(Task, created_by=user, task_list=task_list, _quantity=2, completed=True)
    baker.make(Task, created_by=user, task_list=task_list, _quantity=3, completed=False)
    baker.make(
        Task,
        created_by=user,
        task_list=task_list,
        _quantity=3,
        completed=False,
        due_date="2021-01-01T00:00:00Z",
    )

    res = api_client_with_credentials.get(f"{TASKS_COUNT_URL}?list=upcoming")

    assert res.status_code == status.HTTP_200_OK
    assert res.data["total"] == 3
    assert res.data["completed"] == 0
    assert res.data["pending"] == 3


def test_count_tasks_limited_to_user(api_client_with_credentials, user, user2):
    task_list = baker.make(TaskList, created_by=user)
    baker.make(Task, created_by=user, task_list=task_list, _quantity=2, completed=True)
    baker.make(Task, created_by=user, task_list=task_list, _quantity=3, completed=False)
    baker.make(Task, created_by=user2, _quantity=5)

    res = api_client_with_credentials.get(
        f"{TASKS_COUNT_URL}?list={task_list.list_uuid}"
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["total"] == 5
    assert res.data["completed"] == 2
    assert res.data["pending"] == 3


def test_count_tasks_invalid_uuid(api_client_with_credentials, user):
    res = api_client_with_credentials.get(f"{TASKS_COUNT_URL}?list=invalid-uuid")
    assert res.status_code == status.HTTP_404_NOT_FOUND
