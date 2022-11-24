from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    user_id = serializers.CharField()

    def save(self):
        user_id = self.validated_data['user_id']
        message = self.validated_data['message']
