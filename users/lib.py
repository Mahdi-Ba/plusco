import requests


class SmsNotify:
    def __init__(self, **kwargs):
        url = "https://notify.gardeshpay.com/api/token/"
        payload = {
            "username": "app_agent",
            "password": "aNewAgentAppears"
        }
        headers = {'content-type': 'application/json'}
        response = requests.request("POST", url, json=payload, headers=headers)
        self.refresh = response.json()['refresh']
        self.access = response.json()['access']

    def send(self, **kwargs):

        url = "https://notify.gardeshpay.com/notify/via-sms/send/"

        payload = {
            "text": kwargs['text'],
            "receiver_number": kwargs['receiver_number']
        }
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + self.access
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        if response.status_code == 200:
            return True
        else:
            url = "https://notify.gardeshpay.com/api/token/refresh/"

            payload = {
                "refresh": self.refresh
            }
            headers = {
                'content-type': "application/json",
                'authorization': "Bearer " + self.access

            }
            response = requests.request("POST", url, json=payload, headers=headers)
            if response.status_code != 200:
                return False
            else:
                self.access = response.json()['access']
                self.send(text=kwargs['text'], receiver_number=kwargs['receiver_number'])
