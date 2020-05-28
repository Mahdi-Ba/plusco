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


class DepartmentPositioView(APIView):
    def get(self, request, pk, format=None):
        data = Position.objects.filter(department__exact=pk).all()
        serilizer = PositionSerilizer(data, many=True)
        return Response(serilizer.data)


class DepartmentMemberView(APIView):
    def get(self, request, format=None):
        authority = UserAuthority.objects.get(user=request.user)
        authority = DepartmentMemberSerilizer(authority, many=False)
        return Response(authority.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request.data['user'] = str(request.user.id)
        data = DepartmentMemberSerilizer(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        authority = UserAuthority.objects.get(user=request.user)
        authority = DepartmentMemberSerilizer(authority, data=request.data)
        if authority.is_valid():
            authority.save()
            return Response(authority.data, status=status.HTTP_200_OK)
        return Response(authority.errors, status=status.HTTP_400_BAD_REQUEST)


class FactoryDepartmentView(APIView):
    def get(self, request, pk, format=None):
        data = Department.objects.filter(factory__exact=pk, title__contains=request.GET['item']).all()[:6]
        serilizer = DepartmentSerilizer(data, many=True)
        return Response(serilizer.data)


class FactoryAreaView(APIView):
    def get(self, request, pk, format=None):
        data = Area.objects.filter(factory__exact=pk, title__contains=request.GET['item']).all()[:6]
        serilizer = AreaSerilizer(data, many=True)
        return Response(serilizer.data)


class AreaView(APIView):
    def post(self, request, format=None):
        data = AreaSerilizer(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class PartAreaView(APIView):
    def get(self, request, pk, format=None):
        data = Part.objects.filter(area__exact=pk, title__contains=request.GET['item']).all()[:6]
        serilizer = PartSerilizer(data, many=True)
        return Response(serilizer.data)


class PartView(APIView):
    def post(self, request, format=None):
        data = PartSerilizer(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

class PositionView(APIView):
    def post(self, request, format=None):
        data = PositionSerilizer(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

