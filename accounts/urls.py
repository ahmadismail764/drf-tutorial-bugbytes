from django.urls import path
from accounts.views import UserListView

urlpatterns = [
    path('users/', UserListView.as_view()),
]