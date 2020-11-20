from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import Page, PageSerializer, PageContentSerializer


class PageList(APIView):
    def get(self, request, format=None):
        page = Page.objects.filter().all()
        serializer = PageSerializer(page, many=True)
        return Response(serializer.data)


class PageDetail(APIView):
    def get(self, request, slug, format=None):
        try:
            transaction = Page.objects.get(slug=slug)
            serializer = PageContentSerializer(transaction)
            return Response(serializer.data)
        except Page.DoesNotExist:
            raise Http404
