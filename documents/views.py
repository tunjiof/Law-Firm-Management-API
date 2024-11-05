from django.shortcuts import render
from rest_framework import generics
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class DocumentListCreateView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
