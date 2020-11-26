"""gpay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from rest_framework import permissions

#
# from django.conf.urls import url
# from rest_framework_swagger.views import get_swagger_view
#
# schema_view = get_swagger_view(title='Pastebin API')


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="PLUSCO",
        default_version='v1',
        description="Test api",
        terms_of_service="jobteam.ir",
        contact=openapi.Contact(email="baharimahdi93@gmail.com"),
        license=openapi.License(name="Mahdi Bahari"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # url(r'^$', schema_view),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/users/', include('users.urls')),
    path('v1/pages/', include('pages.urls')),
    path('v1/structure/', include('organizations.urls')),
    path('v1/reports/', include('reports.urls')),
    path('v1/fcm/', include('pluscofcm.urls')),
    path('v1/finances/', include('finances.urls')),
    path('v1/silk/', include('silk.urls', namespace='silk')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
