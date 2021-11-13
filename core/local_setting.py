# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
import os


# DEBUG = True

from crypt_file_config.class_file import FileConfig


ALLOWED_HOSTS = ["localhost", '192.168.0.17']

SECRET_KEY = '!QAZ"WSX#$%&¡?*[:;'

DEBUG = True

MEDIA_ROOT ="/tmp/"

system_config = FileConfig()
config = system_config.get_key_value("local_setting")

"""DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config['database']['name'],
        # "NAME": "prueba3",
        "USER": config['database']['user'],
        "PASSWORD": config['database']['password'],
        "HOST": config['database']['host'],
        "PORT": "3306",
    }
}
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_storage',
        'USER': 'octavio',
        'PASSWORD': 'root@2021',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




