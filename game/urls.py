from django.urls import path

from game.views.user_view import UsersView

urlpatterns = [
    path('user', UsersView.as_view())
]
