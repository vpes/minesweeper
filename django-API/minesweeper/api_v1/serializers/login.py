"""
    Login
"""

# coding: utf8


from django.db.models import Q
from django.contrib.auth import authenticate, get_user_model

from rest_framework import serializers


class NativeLoginSerializer(serializers.Serializer):

    email_phone = serializers.CharField()
    password = serializers.CharField(min_length=7)

    def validate(self, data):

        email_phone = data.get('email_phone')
        password = data.get('password')

        user = get_user_model().objects.filter(
            Q(email=email_phone) | Q(phone=email_phone, phone_valided=True)
        )

        if user:

            if len(user) > 1:
                error_message = "Multiple records returned"
                error_message.update({"app": "users_native_login"})
                raise serializers.ValidationError({"login": error_message})

            user = user[0]

        else:

            error_message = "Invalid email"
            error_message.update({"app": "users_native_login"})
            raise serializers.ValidationError({"login": error_message})

        user = authenticate(
            username=user.username,
            password=password
        )

        if user is not None:
            self.user = user
            return data

        else:
            error_message = "Invalid authentication"
            error_message.update({"app": "users_native_login"})
            raise serializers.ValidationError({"login": error_message})

        return data


