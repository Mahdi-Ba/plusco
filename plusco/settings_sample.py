from pathlib import Path
import os
import environ
import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
#env = environ.Env()
#environ.Env.read_env(".env")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default='x7fr16u^9_z_^c^!5@1l)=m!6uo_es4mcem+%uvs66l7-oi_!s')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=True)

ALLOWED_HOSTS = env.list("HOSTS", default=['www.api.plascoapp.com/', 'plusco.com', '127.0.0.1', '185.97.119.108',
                                           'api.plascoapp.com'])

BASE_URL = "http://api.plascoapp.com/"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djoser',
    'rest_framework',
    'rest_framework.authtoken',
    'users.apps.UsersConfig',
    'jalali_date',
    'ckeditor',
    'ckeditor_uploader',
    'django_json_widget',
    'drf_yasg',
    'organizations',

    'rest_auth',
    # 'allauth',
    'rest_auth.registration',
    'django.contrib.sites',
    'django_filters'
    # 'allauth.account',
    # 'jalali_date',
    # "django_jalali",
    # "allauth.socialaccount"

]

FCM_DJANGO_SETTINGS = {
    "APP_VERBOSE_NAME": "fcm",
    "FCM_SERVER_KEY": "AAAAP_lyPlY:APA91bH-cLsF2vsJU3ejgPYj3OpeTwPKlo_rJ8KFgO7_Hbc6JjCRcLMo_un1pUc4sROMPB1qIh8uwdsuv3x2kF-HglzYAOBPs1s4bRYbUHq89pxAFDuyUNbExPqHDBrvM27IGjWF3mla",
}

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'silk.middleware.SilkyMiddleware',

]

ROOT_URLCONF = 'plusco.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'plusco.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

 DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'plascodb',
         'USER': 'plascouser',
         'PASSWORD': 'Mnujs5_tkr39B4',
         'HOST': '127.0.0.1',  # Or an IP Address that your DB is hosted on
         'PORT': '3306',
         'OPTIONS': {
             # Tell MySQLdb to connect with 'utf8mb4' character set
             'charset': 'utf8mb4',
         },
     }
 }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    # 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets")
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'none',
    },
}
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        # 'Basic': {
        #       'type': 'basic'
        # },
        'PLUSCO': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'PLUSCO eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2Vyb'

        }
    }
}
JWT_AUTH = {
    # 'JWT_ENCODE_HANDLER':
    # 'rest_framework_jwt.utils.jwt_encode_handler',
    #
    # 'JWT_DECODE_HANDLER':
    # 'rest_framework_jwt.utils.jwt_decode_handler',
    #
    # 'JWT_PAYLOAD_HANDLER':
    # 'rest_framework_jwt.utils.jwt_payload_handler',
    #
    # 'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    # 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    #
    # 'JWT_RESPONSE_PAYLOAD_HANDLER':
    # 'rest_framework_jwt.utils.jwt_response_payload_handler',
    #
    # 'JWT_SECRET_KEY': settings.SECRET_KEY,
    # 'JWT_GET_USER_SECRET_KEY': None,
    # 'JWT_PUBLIC_KEY': None,
    # 'JWT_PRIVATE_KEY': None,
    # 'JWT_ALGORITHM': 'HS256',
    #
    #
    # 'JWT_LEEWAY': 0,
    # 'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
    # 'JWT_AUDIENCE': None,
    # 'JWT_ISSUER': None,
    #
    #
    # 'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    #
    #
    # 'JWT_AUTH_COOKIE': None,

    'JWT_VERIFY': True, 'JWT_VERIFY_EXPIRATION': False, 'JWT_ALLOW_REFRESH': False, 'JWT_AUTH_HEADER_PREFIX': 'PLUSCO',
}

SMS_API_KEY = env("SMS_API_KEY",
                  default="4C48474D77574C4C385A7A737A48344B356A6B69726B6543717741396B32527A626C6D34774F654E5550633D")
SMS_SERVICE = env("SMS_SERVICE", default=False)
SITE_ID = 1
