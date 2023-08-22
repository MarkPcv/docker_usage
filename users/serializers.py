from rest_framework import serializers

from config.services import get_bot_url
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for model `users.User`
    """
    invite_link = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_invite_link(self, obj):
        return get_bot_url()
