from django.http import HttpResponse
from django.shortcuts import redirect, render
from zeep import Client

from finances.models import FactoryPlan
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
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            factory_plan = FactoryPlan.objects.get(id=request.GET['id'])
            if factory_plan.increase_count >0:
                factory_plan.count += factory_plan.increase_count
            factory_plan.is_success = True
            factory_plan.ref_id = str(result.RefID)
            factory_plan.save()
            return render(request, 'callback/index.html', {'transaction': request.GET['id'], 'status': True,
                                                           'message': 'با موفقیت انجام شد'})
        elif result.Status == 101:
            return render(request, 'callback/index.html', {'transaction': request.GET['id'], 'status': False,
                                                           'message': 'قبلا ارسال شده است'})
        else:
            return render(request, 'callback/index.html', {'transaction': request.GET['id'], 'status': False,
                                                           'message': 'خطا در انجام تراکنش '})
    else:
        return render(request, 'callback/index.html', {'transaction': request.GET['id'], 'status': False, 'message': 'تراکنش توسط کاربر کنسل شده است'})

