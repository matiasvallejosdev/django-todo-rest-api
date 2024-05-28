"""
Views for todo_api endpoints
"""

from django.shortcuts import get_object_or_404

from .models import Task, TaskList
from .serializers import (
    TaskSerializer,
    TaskDetailSerializer,
    TaskCreateSerializer,
    TaskListSerializer,
    TaskCountSerializer,
)

from rest_framework.exceptions import NotFound
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from urllib.parse import unquote

from uuid import UUID


class TaskViewSet(viewsets.ModelViewSet):
    """Class for viewset tasks"""

    model = Task
    serializer_class = TaskDetailSerializer
    queryset = Task.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "task_uuid"

    def get_queryset(self):
        queryset = self.queryset.filter(created_by=self.request.user)
        task_list = self.request.query_params.get("list", "")

        # Guard clause for empty task_list
        if not task_list:
            return queryset.order_by("created_at").distinct()

        # Define filter mappings for task_list values
        filter_mapping = {
            "inbox": {"task_list__isnull": True},
            "upcoming": {"due_date__isnull": False},
        }

        # Apply predefined filters if available
        if task_list in filter_mapping:
            queryset = queryset.filter(**filter_mapping[task_list])
        else:
            try:
                # Decode and normalize the task_list value
                task_list = unquote(task_list).lower().replace(" ", "-")
                # Validate the UUID
                task_list_uuid = UUID(task_list)
            except (ValueError, TypeError):
                raise NotFound("Invalid UUID format for task list.")

            # Verify the existence of the TaskList with the given UUID
            get_object_or_404(TaskList, list_uuid=task_list_uuid)
            queryset = queryset.filter(task_list__list_uuid=task_list_uuid)

        return queryset.order_by("created_at").distinct()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "list":
            return TaskSerializer
        elif self.action == "create" or self.action == "update":
            return TaskCreateSerializer
        elif self.action == "count_tasks":
            return TaskCountSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(methods=["GET"], detail=False, url_path="count")
    def count_tasks(self, queryset, *args, **kwargs):
        tasks = self.get_queryset().count()
        completed_tasks = self.get_queryset().filter(completed=True).count()
        pending_tasks = self.get_queryset().filter(completed=False).count()
        data = {
            "total": tasks,
            "completed": completed_tasks,
            "pending": pending_tasks,
        }

        serializer = TaskCountSerializer(data, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="upcoming")
    def upcoming_tasks(self, request, *args, **kwargs):
        """
        List all upcoming tasks scheduled ordered by date
        """
        tasks = self.get_queryset().filter(due_date__isnull=False).order_by("due_date")
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskListViewSet(viewsets.ModelViewSet):
    """Class for viewset task lists"""

    model = TaskList
    serializer_class = TaskListSerializer
    queryset = TaskList.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "list_uuid"

    def get_queryset(self):
        queryset = self.queryset.filter(created_by=self.request.user)
        return queryset.order_by("created_at").distinct()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def retrieve(self, request, list_uuid=None, *args, **kwargs):
        """
        Retrieve a task list object by list_uuid.
        """
        list_uuid = list_uuid.lower()
        if list_uuid in ["inbox", "upcoming"]:
            data = {
                "list_uuid": list_uuid,
                "name": list_uuid,
            }
            serializer = self.get_serializer(data)
            return Response(serializer.data)
        queryset = self.get_queryset()

        try:
            # Attempt to retrieve the task list by UUID
            task_list = queryset.get(list_uuid__iexact=list_uuid)
        except TaskList.DoesNotExist:
            return Response(
                {"message": "List not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Serialize and return the task list
        serializer = self.get_serializer(task_list)
        return Response(serializer.data)
