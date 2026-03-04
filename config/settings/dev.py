from .base import *
import os
DEBUG = True

SECRET_KEY = "django-insecure--pyzp1l)4g)i*gbmt_sug*f!sq5$l!m47$fxghg#r_ze%gq)0e"

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# LOCAL DATABASE (only used on your laptop)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


try:
    from .local import *
except ImportError:
    pass


import ssl
ssl._create_default_https_context = ssl._create_unverified_context