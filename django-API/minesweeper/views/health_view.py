from rest_framework.views import APIView
from rest_framework.response import Response


class HealthView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response("ok", status=200)


health_view = HealthView.as_view()
