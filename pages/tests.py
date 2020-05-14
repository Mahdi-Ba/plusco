from gpay.tests import GpayTestCase
from rest_framework import status
from .models import Page
from .api.serializers import PageContentSerializer, PageSerializer


class ServicesTestCase(GpayTestCase):
    def setUp(self):
        self.user = self.createUser(phone="09195000200")
        self.login(user=self.user)
        self.page = Page.objects.create(
            title='test it',
            content="today is rainy 20 farvardin 99 "
        )
        self.serlizer = PageSerializer(Page.objects.all(), many=True)
        self.one_serlizer = PageContentSerializer(self.page, many=False)

    def test_page_list(self):
        res = self.client.get('/api/v1/page/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        assert self.serlizer.data == res.json()

    def test_page_detail(self):
        res = self.client.get('/api/v1/page/'+self.page.slug)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        assert self.one_serlizer.data == res.json()
