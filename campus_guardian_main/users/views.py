from rest_framework import generics
from .models import User
from .serializers import UserWithLoginSerializer

# List all users or create one
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserWithLoginSerializer

# Retrieve, update or delete a user by ID
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserWithLoginSerializer
