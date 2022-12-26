from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class AppIndexView(APIView):
    renderer_classes = (StaticHTMLRenderer,)
    permission_classes = ()

    def get(self, request):
        return Response("Welcome to enfight api", content_type="text/plain")
