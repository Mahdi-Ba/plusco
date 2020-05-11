from rest_framework.test import APITestCase
from users.models import User
from wallets.models import Wallet
from transactions.models import Transaction, TransactionType, TransactionStatus
from services.models import Service

class GpayTestCase(APITestCase):
    def createUser(self, **kwargs):
        user = User.objects.create_user(mobile= kwargs['phone'], password=123456789)
        user.save()
        return user

    def login(self, **kwargs):
        data = {
            "mobile": kwargs['user'].mobile,
            "password": "123456789"
        }
        self.res = self.client.post('/api/v1/users/api-token-auth/', data)
        self.token = self.res.json()['token']
        self.client.credentials(HTTP_AUTHORIZATION='GPAY ' + self.token)

    def chargeWallet(self,**kwargs):
        wallet = Wallet.objects.filter(owner=kwargs['user']).first()
        wallet.amount += int(kwargs['amount'])
        wallet.save()
        return wallet


    def createTransactionStatus(self):
        waiting_status = TransactionStatus.objects.create(title='waiting')
        success_status = TransactionStatus.objects.create(title='success')
        error_status =TransactionStatus.objects.create(title='error')
        return {'wait':waiting_status,'success':success_status,'error':error_status}

    def createTransactionType(self):
        TransactionType.objects.create(title='gateway')
        TransactionType.objects.create(title='wallet')

    def creteServiceId(self,**kwargs):
        service = Service.objects.create(title=kwargs['method'],service_method=kwargs['method'],is_active=1)
        return service


    def createTransaction(self,**kwargs):
        return Transaction.objects.create(owner=kwargs['owner'],service=kwargs['service'],tr_status=kwargs['status'])


