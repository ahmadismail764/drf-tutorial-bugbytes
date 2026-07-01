from django.shortcuts import render
from rest_framework import generics, viewsets
from accounts.models import User
from accounts.serializers import UserSerializer

# Endpoints provided by this view:
# - GET    : returns a list of users (list endpoint)
# - HEAD   : returns headers for the list endpoint
# - OPTIONS: returns allowed HTTP methods and metadata for the endpoint
# class UserListView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     pagination_class = None

# Endpoints provided by this view:
# - GET    : returns a list of users (list endpoint)
# - HEAD   : returns headers for the list endpoint
# - OPTIONS: returns allowed HTTP methods and metadata for the endpoint
# - POST   : creates a new user (create endpoint)
# - GET    : returns a single user by id (retrieve endpoint)
# - PUT    : updates a single user by id (update endpoint)
# - PATCH  : partially updates a single user by id (partial_update endpoint)
# - DELETE : deletes a single user by id (destroy endpoint)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer