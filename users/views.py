from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .models import User, LoginHistory, Client
from .serializers import RegisterSerializer, UserSerializer

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow anyone to register

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow anyone to login

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Authenticate using email and password
        user = authenticate(email=email, password=password)

        if user is not None:
            LoginHistory.objects.create(user=user)
            access_token = RefreshToken.for_user(user).access_token
            return Response({
                "access": str(access_token),
                "message": "Login successful."
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

class LoggedInUsersView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def get(self, request):
        # Check if the user has the role 'client'
        if request.user.role == 'client':
            return Response({"error": "You do not have permission to view this data."}, 
                            status=status.HTTP_403_FORBIDDEN)

        if request.user.role == 'lawyer':
            # Fetch clients associated with the lawyer
            clients = request.user.clients.all()  # This retrieves the clients linked to the lawyer
            serializer = UserSerializer(clients, many=True)
            return Response(serializer.data)

        # If the user is an admin, they can view all users
        users = User.objects.all()  # Retrieve all users
        serializer = UserSerializer(users, many=True)  # Serialize the user data
        return Response(serializer.data)

class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access

    def get(self, request, pk):
        # Allow lawyers to view only their own clients by ID
        if request.user.role == 'lawyer':
            client = get_object_or_404(Client, pk=pk, lawyer=request.user)  # Check if the client belongs to the lawyer
            serializer = UserSerializer(client)
            return Response(serializer.data)

        # Allow admins to view any user by ID
        if request.user.role == 'admin':
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)

        return Response({"error": "You do not have permission to view this data."}, 
                        status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        # Check if the user is an admin or a lawyer updating their own client
        if request.user.role == 'admin':
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User updated successfully."}, status=status.HTTP_200_OK)
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.role == 'lawyer':
            client = get_object_or_404(Client, pk=pk, lawyer=request.user)  # Check if the client belongs to the lawyer
            serializer = UserSerializer(client, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Client updated successfully."}, status=status.HTTP_200_OK)
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "You do not have permission to update this data."}, 
                        status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        # Check if the user is an admin
        if request.user.role == 'admin':
            user = get_object_or_404(User, pk=pk)
            user.delete()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        # Check if the user is a lawyer trying to delete their own client
        if request.user.role == 'lawyer':
            client = get_object_or_404(Client, pk=pk, lawyer=request.user)  # Check if the client belongs to the lawyer
            client.delete()
            return Response({"message": "Client deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"error": "You do not have permission to delete this data."}, 
                        status=status.HTTP_403_FORBIDDEN)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can logout

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Logout failed. Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
