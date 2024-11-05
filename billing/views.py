# from django.shortcuts import render
# from rest_framework import generics
# from .models import Billing
# from .serializers import BillingSerializer

# # Create your views here.

# class BillingListCreateView(generics.ListCreateAPIView):
#     queryset = Billing.objects.all()
#     serializer_class = BillingSerializer

# class BillingDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Billing.objects.all()
#     serializer_class = BillingSerializer



from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Billing  # Assuming you have a Billing model
from .serializers import BillingSerializer  # Assuming you have a BillingSerializer

class BillingListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access

    def get(self, request):
        """
        GET /billing/
        Allows users to view billing entries based on their role.
        """
        if request.user.role == 'admin':
            billings = Billing.objects.all()
        elif request.user.role == 'lawyer':
            billings = Billing.objects.filter(lawyer=request.user)  # Replace with the actual relationship field
        elif request.user.role == 'client':
            billings = Billing.objects.filter(client=request.user)  # Replace with the actual relationship field
        else:
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        serializer = BillingSerializer(billings, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        POST /billing/
        Allows Admin and Lawyer to create new billing entries.
        """
        if request.user.role not in ['admin', 'lawyer']:
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        serializer = BillingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BillingDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access

    def get(self, request, pk):
        """
        GET /billing/<pk>/
        Allows users to view a specific billing entry based on their role.
        """
        billing = get_object_or_404(Billing, pk=pk)

        if request.user.role == 'admin' or \
           (request.user.role == 'lawyer' and billing.lawyer == request.user) or \
           (request.user.role == 'client' and billing.client == request.user):
            serializer = BillingSerializer(billing)
            return Response(serializer.data)
        
        return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        """
        PUT /billing/<pk>/
        Allows Admin and Lawyer to update a specific billing entry.
        """
        billing = get_object_or_404(Billing, pk=pk)

        if request.user.role not in ['admin', 'lawyer']:
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        serializer = BillingSerializer(billing, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        DELETE /billing/<pk>/
        Allows only Admin to delete a specific billing entry.
        """
        billing = get_object_or_404(Billing, pk=pk)

        if request.user.role != 'admin':
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        billing.delete()
        return Response({"message": "Billing entry deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
