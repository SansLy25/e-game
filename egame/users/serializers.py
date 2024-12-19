from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    exams = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ("id", "username", "exams")
