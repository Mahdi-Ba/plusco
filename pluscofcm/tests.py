from rest_framework import status
from gpay.tests import GpayTestCase
from faker import Faker


class FcmTestCase(GpayTestCase):
    def setUp(self):
        self.user = self.createUser(phone="09195000200")
        self.login(user=self.user)

    def test_get_type(self):
        res = self.client.get('/api/v1/fcm/type')
        assert res.status_code == status.HTTP_200_OK

    def test_store_fcm_device(self):
        data = {
            'registration_id': 'fxuh85hIzAw:APA91bHK_s4ZS3MskKQOH7Cecj1OTYylSRIHmQmIW9nwkJutFpLGdM2WyZRkkrWV7nhRZLlKrauLvzHTCO6xAxwxhWyxFFheZJAUVgUcR9YzoTT3UPi6LJTDMTFyZAD81Nt4Ly5qTbjk',
            'type': 'android',
            'device_id': '123',
            'name': 'GardeshPayAndroidApp'
        }
        res = self.client.post('/api/v1/fcm/devices',data)
        assert res.status_code == status.HTTP_201_CREATED
