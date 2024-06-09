from rest_framework import serializers


class AutocompleteTaskSerializer(serializers.Serializer):
    text = serializers.CharField()

    # check if the status is completed, then the text should not be empty
    def validate(self, data):
        if not data["text"]:
            raise serializers.ValidationError(
                "Text is required when status is completed"
            )
        return data
