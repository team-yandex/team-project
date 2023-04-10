import os
from pathlib import Path

from django.contrib.messages import constants as message_constants
import dotenv


dotenv.load_dotenv()
dotenv.load_dotenv(dotenv_path='../example.env')

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv('SECRET_KEY', 'notsecret')

DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

if DEBUG:
    ALLOWED_HOSTS = '*'
else:
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost')
ALLOWED_HOSTS = ALLOWED_HOSTS.split(',')

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'default@example.com')

IS_ACTIVE = (
    os.getenv('IS_ACTIVE', 'True' if DEBUG else 'False').capitalize() == 'True'
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig',
    'sorl.thumbnail',
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
]
if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if DEBUG:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'whn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'whn.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / 'static_dev']
STATIC_ROOT = BASE_DIR / 'static'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'send_mail'
EMAIL_URL = '/uploads/'
EMAIL_TEXT_SIGN_UP = """Здравствуйте!

Вы получили это сообщение, так как зарегистрировались на Yadjango.

Для активации своего профиля перейдите по ссылке:
{link}

Спасибо, что присоединились к нам!

© whn
"""

MESSAGE_TAGS = {
    message_constants.SUCCESS: 'w-100 alert alert-success text-center',
    message_constants.ERROR: 'w-100 alert alert-danger text-center',
}

LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'users.User'
