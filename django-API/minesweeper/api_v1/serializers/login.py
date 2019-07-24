"""
    Login
"""

# coding: utf8


from django.db.models import Q
from django.contrib.auth import authenticate, get_user_model

from rest_framework import serializers


class NativeLoginSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField(min_length=1)

    def validate(self, data):

        email = data.get("email")
        password = data.get("password")

        user, created = get_user_model().objects.get_or_create(email=email,
                                                         defaults={
                                                             "username": email,
                                                             "first_name": email,
                                                             "last_name": email
                                                         })
        if created:
            user.set_password(password)
            user.save()
        else:
            user = authenticate(username=user.username, password=password)

        if user is not None:
            self.user = user
            return data
        else:
            error_message = {"app": "users_native_login",
                             "details": "Invalid authentication",
                             "code": 401}
            raise serializers.ValidationError({"login": error_message})
        return data
