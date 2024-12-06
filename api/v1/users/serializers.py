from django.contrib.auth.password_validation import validate_password

from users.models import User
from rest_framework import serializers


class StreamLabsSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('password', 'email', 'battletag')
        extra_kwargs = {
            'battletag': {'required': True}
        }

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            battletag=validated_data.get('battletag'),
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

