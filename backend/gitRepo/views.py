from django.shortcuts import render
from rest_framework import viewsets, generics, mixins
from .models import Repository
from .serializers import RepositorySerializer


# Create your views here.
class RepoViewSet(viewsets.ModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
