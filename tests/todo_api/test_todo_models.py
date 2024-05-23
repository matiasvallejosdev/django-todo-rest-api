import pytest

from todo_api.models import Task, TaskList
from model_bakery import baker

pytestmark = [pytest.mark.unit, pytest.mark.django_db]


def test_task_list_str():
    """Test that the __str__ method of TaskList returns the correct string"""
    task_list = baker.make(TaskList, name="Inbox")
    assert str(task_list) == "Inbox"


def test_task_str():
    """Test that the __str__ method of Task returns the correct string"""
    task = baker.make(Task, title="Task")
    assert str(task) == "Task"
