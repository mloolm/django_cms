from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _
from django.apps import apps
import json

#Session
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 1209600  # 2 недели
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('APP_SECRET_KEY', 'django-insecure-!z45h4#7ni^31063we9p%uqc!wr*3yx8x1@cyw!q5mu^-fg9$e')

if os.getenv('DJANGO_ENV', 'dev') == 'production':
    DEBUG = False
else:
    DEBUG = True

main_host = os.getenv('APP_HOST', 'yourdomain.com')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', main_host]

#DONATIONS
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', None)
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', None)

PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID', None)
PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET', None)
PAYPAL_MODE = os.getenv('PAYPAL_MODE', None)

#Cache
CACHEOPS = {
    'blog.*': {'ops': 'all', 'timeout': 3600},
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'KEY_PREFIX': 'common_cache:',
        },
    },
    'cacheops': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'KEY_PREFIX': 'cacheops:',
        },
    }
}

CACHE_TTL = 3600

#Logging
log_mode = False
if log_mode:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_otp",
    "django_otp.plugins.otp_totp",  # TOTP (Google Authenticator, Authy)
    "django_otp.plugins.otp_static",  # Reserve Codes 2FA
    "two_factor",
    'blog',
    'tinymce',
    'donations'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    "django_otp.middleware.OTPMiddleware",  # Must be before Require2FAMiddleware
    'rs.admin_middleware.AdminLocaleMiddleware',
]

ROOT_URLCONF = 'rs.urls'

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
                'blog.context_processors.global_context'
            ],
        },
    },
]

WSGI_APPLICATION = 'rs.wsgi.application'

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

#Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Используем MySQL
        'NAME': os.getenv('DATABASE_NAME', 'app'),  # Имя базы данных
        'USER': os.getenv('DATABASE_USER', 'app'),  # Пользователь
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'password'),  # Пароль
        'HOST': os.getenv('DATABASE_HOST', 'dj_db'),  # Контейнер с базой данных
        'PORT': os.getenv('DATABASE_PORT', '3306'),  # Порт MySQL
        'OPTIONS': {
                    'charset': 'utf8mb4',
                    'init_command': "SET NAMES 'utf8mb4' COLLATE 'utf8mb4_general_ci'",
                },
        'TEST': {
            'NAME': 'test_'+os.getenv('DATABASE_NAME', 'app'),  # Имя существующей тестовой базы данных
        },
    },


}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

TIME_ZONE = os.getenv('APP_TIME_ZONE', 'UTC') #https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
USE_I18N = True
USE_TZ = True

LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'en')
languages_json = os.getenv('LANGUAGES', '[["en", "English"]]')
languages_json = json.loads(languages_json)
LANGUAGES = languages_json
ADMIN_LANGUAGES = languages_json

LOCALE_PATHS = [
    BASE_DIR / 'locale',  # Path for translation files
]



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

#2FA && LOGIN
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'two_factor:login'
TWO_FACTOR_REMEMBER_COOKIE_AGE = 30 * 86400
LOGIN_REDIRECT_URL = "/"

TWO_FACTOR_PATCH_ADMIN = True

#Tiny MCE
TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'advlist autolink lists link image add_from_gallery charmap anchor pagebreak code',
    'toolbar': 'undo redo | image | add_from_gallery | formatselect | bold italic | alignleft aligncenter alignright | link | code',
    'height': 700,
    'width': '100%',
    'menubar': True,
    'images_upload_url': '/upload-image/',
    'automatic_uploads': True,
    'file_picker_types': 'image',
    'image_list': '/api/img-list/',
    'relative_urls': True,
    'convert_urls': False,
    'external_plugins': {
        'add_from_gallery': '/static/js/add_from_gallery/plugin.js',
    },
    'content_css': [
        '/static/src/css/styles.css',
    ],
}

X_FRAME_OPTIONS = 'SAMEORIGIN'

CSP_DEFAULT_SRC = ("'self'", "https://yourdomain.com")

#Content
POST_ON_PAGE =  os.getenv('APP_POSTS_ON_PAGE', 12)