#from six import python_2_unicode_compatible
import os
from .common import Common

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    DEBUG = True
    DOMAIN = "127.0.0.1:8000"

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ("django_nose",)
    TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
    NOSE_ARGS = [
        BASE_DIR,
        "-s",
        "--nologcapture",
        "--with-coverage",
        "--with-progressive",
        "--cover-package=project",
    ]

    # Mail
    # EMAIL_HOST = "localhost"
    # EMAIL_PORT = 1025
    # EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST=os.getenv('EMAIL_HOST')
    EMAIL_PORT = 465
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = True
    EMAIL_HOST_USER=os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD=os.getenv('EMAIL_HOST_PASSWORD')
