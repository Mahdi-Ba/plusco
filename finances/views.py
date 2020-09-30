from django.http import HttpResponse
from django.shortcuts import redirect, render
from fcm_django.models import FCMDevice
from zeep import Client

from finances.models import FactoryPlan
from organizations.models import UserAuthority
from plusco.settings import BASE_URL

MERCHANT = '329811de-8125-4fce-836d-a1f0d048c5e0'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Toman / Required
description = "خرید بسته"  # Required
mobile = '09195000200'  # Optional
CallbackURL = BASE_URL + "v1/finances/verify/"
email = ''


def send_request(factory_plan):
    result = client.service.PaymentRequest(MERCHANT, factory_plan.price_with_tax, description, email,
                                           factory_plan.user.mobile, CallbackURL + '?id=' + str(factory_plan.id))
    if result.Status == 100:
        return True, 'https://www.zarinpal.com/pg/StartPay/' + str(result.Authority)
    else:
        return False, 'Error code: ' + str(result.Status)


def verify(request):
    if request.GET.get('Status') == 'OK':
        factory_plan = FactoryPlan.objects.filter(id=request.GET['id']).first()
        if factory_plan == None:
            return render(request, 'callback/index.html', {'transaction': request.GET['id'], 'status': False,
                                                           'message': 'خطا در انجام تراکنش '})

        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], factory_plan.price_with_tax)
        if result.Status == 100:
            if factory_plan.increase_count > 0:
                factory_plan.count += factory_plan.increase_count
            factory_plan.is_success = True
            factory_plan.ref_id = str(result.RefID)
            factory_plan.save()
            authority = UserAuthority.objects.filter(department__factory=factory_plan.factory, is_active=True,
                                                     status_id=4).all().values_list('user', flat=True)
            device = FCMDevice.objects.filter(user_id__in=authority).all()
            payload = {
                "type": "pay-close",
                "id": request.GET['id'],
                "priority": "high",
                "click_action": "FLUTTER_NOTIFICATION_CLICK"
            }
            device.send_message(title='پرداخت شد', body='پرداخت کارگاه با موفقیت انجام شد ', data=payload)
            return render(request, 'callback/index.html', {'transaction': request.GET['id'], 'status': True,
                                                           'message': 'با موفقیت انجام شد'})
        elif result.Status == 101:
            return render(request, 'callback/index.html', {'transaction': request.GET['id'], 'status': False,
                                                           'message': 'قبلا ارسال شده است'})
        else:
            return render(request, 'callback/index.html', {'transaction': request.GET['id'], 'status': False,
                                                           'message': 'خطا در انجام تراکنش '})
    else:
        return render(request, 'callback/index.html',
                      {'transaction': request.GET['id'], 'status': False, 'message': 'تراکنش توسط کاربر کنسل شده است'})
