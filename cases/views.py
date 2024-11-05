from django.shortcuts import render
from rest_framework import generics
from .models import Case
from .serializers import CaseSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class CaseListCreateView(generics.ListCreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticated]

class CaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticated]
