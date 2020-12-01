from django.conf import settings
import kavenegar
import random

sms_api_key = getattr(settings, "SMS_API_KEY",
                      "4C48474D77574C4C385A7A737A48344B356A6B69726B6543717741396B32527A626C6D34774F654E5550633D")
sms_service = getattr(settings, "SMS_SERVICE", True)


def create_random_otp():
    if sms_service:
        otp = random.randint(11111, 99999)
        return str(otp)
    else:
        return str(11111)


def send_otp(otp: int, mobile):
    if not sms_service:
        print(f"{mobile}:{otp}")
        return
    mobile = "0" + mobile
    api_key = sms_api_key
    api = kavenegar.KavenegarAPI(api_key)

    params = {
        'receptor': mobile,
        'template': 'plasco',
        'token': otp,
        'type': 'sms',
    }

    response = api.verify_lookup(params)
