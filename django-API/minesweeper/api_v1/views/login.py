# coding: utf8
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import reset_token
from minesweeper.api_v1.schemas.login import (UserSchema)
from minesweeper.api_v1.serializers.login import (NativeLoginSerializer)

"""
    Login
"""


class NativeLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = NativeLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user

            # Get Token
            token = reset_token(user)
            setattr(user, 'token', token)

            schema = UserSchema().dump(user).data

            return Response({"response": schema}, status=status.HTTP_200_OK)

        else:

            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

