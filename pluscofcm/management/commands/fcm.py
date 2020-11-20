from django.core.management.base import BaseCommand
from fcm_django.models import FCMDevice
from users.models import User

from datetime import datetime, timedelta
from django.utils import timezone


# def update_blog():
#     blog_data = Blog.objects.all()
#     for data in blog_data:
#         data.date = datetime.now()
#         data.save()

class Command(BaseCommand):
    help = 'python manage.py fcm'

    def handle(self, **options):
        now = timezone.now()
        twenty_nine_min_ago = now - timedelta(minutes=29)
        thirty_min_ago = now - timedelta(minutes=30)
        # users = str.split(options['userId'][0], ',')
        users_query = User.objects.filter(say_hi=False, date_joined__lt=str(twenty_nine_min_ago), date_joined__gte=str(thirty_min_ago)).all()
        users = users_query.all()
        for user in users:
            if FCMDevice.objects.filter(user_id=user.id, active=1).exists():
                device = FCMDevice.objects.filter(user_id=user.id, active=1).all()
                device.send_message(title='خوش آمدید', body='ورود شما را به خانواده گردش پی خوش آمد میگوییم')
        users_query.update(say_hi=True)
    # def add_arguments(self, parser):
    #     # parser.add_argument('user', type=int)
    #     parser.add_argument('--userId', action='append', type=str)
