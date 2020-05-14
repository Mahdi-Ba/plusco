from django.utils.text import slugify
from rest_framework import serializers
from ..models import Page
from django.urls import reverse


class PageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_url')

    class Meta:
        model = Page
        fields = ['id', 'title', 'url']

    def get_url(self, instance):
        return reverse('page_detail', kwargs={'slug': instance.slug})


class PageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'title', 'content', 'slug', 'created']
