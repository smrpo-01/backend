from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings

from rest_framework_jwt.views import ObtainJSONWebToken
from .serializers import JWTSerializer

import os


class ObtainJWTView(ObtainJSONWebToken):
    serializer_class = JWTSerializer


class EmineoView(View):
    def get(self, request):
        try:
            with open(os.path.join(settings.BASE_DIR, 'app/dist', 'index.html')) as file:
                return HttpResponse(file.read())

        except:
            return HttpResponse(
                """
                index.html not found ! build your React app !!
                """,
                status=501,
            )
