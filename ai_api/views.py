import os
import json

from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import AutocompleteTaskSerializer
from .prompts import get_autocomplete_agent_prompt

from groq import Groq


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)


class AutocompleteTaskView(RetrieveAPIView):
    serializer_class = AutocompleteTaskSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        input_text = request.query_params.get("input_text", "")
        title = request.query_params.get("title", "")
        list_tasks = request.query_params.get("list_tasks", "")
        list_tasks = list_tasks.split(",") if list_tasks else []

        if not input_text or not title:
            return Response(
                {
                    "error": "input_text and title query parameters are required. list_tasks is optional"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        prompt = get_autocomplete_agent_prompt(title, list_tasks, input_text)

        try:
            chat_completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": prompt,
                    }
                ],
            )
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            completion = chat_completion.choices[0].message.content
            print(completion)
            if "status" not in completion:
                return Response(
                    {"error": "There is an error building completion"}, status=status.HTTP_400_BAD_REQUEST
                )
            completion_json = json.loads(completion)
        except (KeyError, json.JSONDecodeError) as e:
            return Response(
                {"error": "Invalid response from chat completion"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if completion_json.get("status") == "error":
            return Response(
                {"error": completion_json["message"]}, status=status.HTTP_400_BAD_REQUEST
            )

        text = completion_json.get("text", "")
        serializer = self.serializer_class(data={"text": text})

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
