from django.db.models import Q
from django.http import Http404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from ..models import *


class OrganizationView(APIView):
    def get(self, request, format=None):
        data = Organization.objects.filter(title__contains=request.GET['item']).all()[:6]
        serilizer = OrgSerilizer(data, many=True)
        return Response(serilizer.data)

    def post(self, request, format=None):
        data = OrgSerilizer(data=request.data)
        if data.is_valid():
            data.save(owner=request.user)
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class OrgFactoryView(APIView):
    def get(self, request, pk, format=None):
        data = Factory.objects.filter(organization__exact=pk, title__contains=request.GET['item']).all()[:6]
        serilizer = FactorySerilizer(data, many=True)
        return Response(serilizer.data)


class FactoryView(APIView):
    def post(self, request, format=None):
        data = FactorySerilizer(data=request.data)
        if data.is_valid():
            data.save(owner=request.user)
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)




class DepartmentView(APIView):
    def post(self, request, format=None):
        data = DepartmentSerilizer(data=request.data)
        if data.is_valid():
            data.save(owner=request.user)
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class FactoryDepartmentView(APIView):
    def get(self, request, pk, format=None):
        data = Department.objects.filter(factory__exact=pk, title__contains=request.GET['item']).all()[:6]
        serilizer = DepartmentSerilizer(data, many=True)
        return Response(serilizer.data)




