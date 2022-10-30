import os
from os.path import join
from distutils.util import strtobool
from datetime import timedelta
import dj_database_url
from configurations import Configuration
from corsheaders.defaults import default_headers



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Common(Configuration):

    INSTALLED_APPS = (
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # Third party apps
        "rest_framework",  # utilities for rest apis
        "rest_framework.authtoken",  # token authentication
        "django_filters",  # for filtering rest endpoints
        "djoser",
        "social_django",
        "tagging",
        # Your apps
        "project.users",
        "project.services",
        "project.interest",
        "project.explore",
        "project.detail",
        "storages",
    )

    # https://docs.djangoproject.com/en/2.0/topics/http/middleware/
    MIDDLEWARE = (
        "django.middleware.security.SecurityMiddleware",
        "corsheaders.middleware.CorsPostCsrfMiddleware",
        "corsheaders.middleware.CorsMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "social_django.middleware.SocialAuthExceptionMiddleware",
    )

    ALLOWED_HOSTS = ["*"]
    ROOT_URLCONF = "project.urls"
    SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
    WSGI_APPLICATION = "project.wsgi.application"

    # Email
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    ADMINS = (("Author", "meetluckyadogun@gmail.com"),)

    # Postgres
    DATABASES = {
        "default": dj_database_url.config(
            default="postgres://postgres:@postgres:5432/postgres",
            conn_max_age=int(os.getenv("POSTGRES_CONN_MAX_AGE", 600)),
        )
    }

    # General
    APPEND_SLASH = False
    TIME_ZONE = "UTC"
    LANGUAGE_CODE = "en-us"
    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    USE_I18N = False
    USE_L10N = True
    USE_TZ = True
    LOGIN_REDIRECT_URL = "/"

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/

    # STATIC_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), "static"))
    # STATICFILES_DIRS = []
    # STATIC_URL = "/static/"
    # STATICFILES_FINDERS = (
    #     "django.contrib.staticfiles.finders.FileSystemFinder",
    #     "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # )

    # # Media files
    # MEDIA_ROOT = join(os.path.dirname(BASE_DIR), "media")
    # MEDIA_URL = "/media/"

    USE_SPACES = os.getenv('USE_SPACES') == 'FALSE'

    if USE_SPACES:
        # settings
        AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
        AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
        AWS_DEFAULT_ACL = 'public-read'
        AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
        AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
        # static settings
        AWS_LOCATION = 'static'
        STATIC_URL = f'https://{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/'
        STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
        # public media settings
        PUBLIC_MEDIA_LOCATION = 'media'
        MEDIA_URL = f'https://{AWS_S3_ENDPOINT_URL}/{PUBLIC_MEDIA_LOCATION}/'
        #DEFAULT_FILE_STORAGE = 'project.config.storage_backends.PublicMediaStorage'
        DEFAULT_FILE_STORAGE = 'storage.PublicMediaStorage'
    else:
        STATIC_URL = '/static/'
        STATIC_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), "static"))
        MEDIA_URL = '/media/'
        MEDIA_ROOT = join(os.path.dirname(BASE_DIR), "media")

    STATICFILES_DIRS = []

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": STATICFILES_DIRS,
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",

                    "social_django.context_processors.backends",
                    "social_django.context_processors.login_redirect",
                ],
            },
        },
    ]

    # Set DEBUG to False as a default for safety
    # https://docs.djangoproject.com/en/dev/ref/settings/#debug
    # DEBUG = strtobool(os.getenv("DJANGO_DEBUG", "no"))
    DEBUG = True

    # Password Validation
    # https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # Logging
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "django.server": {
                "()": "django.utils.log.ServerFormatter",
                "format": "[%(server_time)s] %(message)s",
            },
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
            },
            "simple": {"format": "%(levelname)s %(message)s"},
        },
        "filters": {
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            },
        },
        "handlers": {
            "django.server": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "django.server",
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
            "mail_admins": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "propagate": True,
            },
            "django.server": {
                "handlers": ["django.server"],
                "level": "INFO",
                "propagate": False,
            },
            "django.request": {
                "handlers": ["mail_admins", "console"],
                "level": "ERROR",
                "propagate": False,
            },
            "django.db.backends": {"handlers": ["console"], "level": "INFO"},
        },
    }

    # Custom user app
    AUTH_USER_MODEL = "users.User"

    # Django Rest Framework
    REST_FRAMEWORK = {
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
        "PAGE_SIZE": int(os.getenv("DJANGO_PAGINATION_LIMIT", 10)),
        "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
        "DEFAULT_RENDERER_CLASSES": (
            "rest_framework.renderers.JSONRenderer",
            "rest_framework.renderers.BrowsableAPIRenderer",
        ),
        "DEFAULT_PERMISSION_CLASSES": [
            # "rest_framework.permissions.IsAuthenticated",
            'rest_framework.permissions.AllowAny',
        ],
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework.authentication.SessionAuthentication",
            "rest_framework.authentication.TokenAuthentication",
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        ),
    }

    SIMPLE_JWT = {
        "AUTH_HEADER_TYPES": ("Bearer","Token","JWT",),
        "BLACKLIST_AFTER_ROTATION": False,
        "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=2),
    }
    
    white_list = ['http://localhost:8000/accounts/profile/'] # URL you add to google developers console as allowed to make redirection

    # Djoser
    DJOSER = {
        "PASSWORD_RESET_CONFIRM_URL": "#/password/reset/confirm/{uid}/{token}",
        "USERNAME_RESET_CONFIRM_URL": "#/username/reset/confirm/{uid}/{token}",
        "ACTIVATION_URL": "activate/{uid}/{token}",
        "SEND_ACTIVATION_EMAIL": False,
        "LOGIN_FIELD": "email",
        "SERIALIZERS": {'user_create': 'project.users.serializers.UserRegistrationSerializer'}, 
        'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': white_list # Redirected URL we listen on google console       
    }

    # Custom Settings
    SITE_NAME = "Your Site"

    # CORS Header
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000/",
        "http://localhost:8000/",
        "http://127.0.0.1:3000/",
        "https://yoursite.com/",
        "https://yourside.herokuapp.com",
    ]
    CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
    CORS_ALLOW_HEADERS = list(default_headers)


    AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.facebook.FacebookOAuth2",

    # Crucial when logging into admin with username & password
    "django.contrib.auth.backends.ModelBackend",
    )

    # Client ID and Client Secret obtained from console.developers.google.com
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "565700308053-virs9lpblofiu6b0rq9bpkb7drgqse1p.apps.googleusercontent.com"

    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "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"

    SOCIAL_AUTH_RAISE_EXCEPTIONS = False
    # SOCIAL_AUTH_POSTGRES_JSONFIELD = True # Optional, how token will be saved in DB
   

    SOCIAL_AUTH_FACEBOOK_KEY = "783561869389000"  # App ID
    SOCIAL_AUTH_FACEBOOK_SECRET = "73c8e6c8354eb096ad451e5ef1f0ec02"  # App Secret  


    SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
    SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
        'fields': 'email'
    }
    
    #Django tagging custom settings
    FORCE_LOWERCASE_TAGS = True
    
    #Configure DEFAULT_AUTO_FIELD in settings
    DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

    