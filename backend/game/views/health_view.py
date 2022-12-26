from django import db
from django.http import HttpResponse


def health_check_view(request):
    db.connection.ensure_connection()
    return HttpResponse("ok")
