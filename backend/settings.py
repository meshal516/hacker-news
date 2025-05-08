import os # Add os import for environment variables
import certifi # Import certifi

# --- BEGIN .env loading for settings.py ---
from dotenv import load_dotenv

# Determine the base directory (where settings.py is located)
# This assumes settings.py is in hacker-news/backend/
BASE_DIR_FOR_ENV = os.path.dirname(os.path.abspath(__file__))
ENV_PATH_FOR_SETTINGS = os.path.join(BASE_DIR_FOR_ENV, '.env')

if os.path.exists(ENV_PATH_FOR_SETTINGS):
    print(f"settings.py: Loading environment variables from: {ENV_PATH_FOR_SETTINGS}")
    load_dotenv(dotenv_path=ENV_PATH_FOR_SETTINGS, override=True)
else:
    print(f"settings.py WARNING: .env file not found at {ENV_PATH_FOR_SETTINGS}, relying on system environment variables.")
# --- END .env loading for settings.py ---


KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_SECURITY_PROTOCOL = os.environ.get('KAFKA_SECURITY_PROTOCOL')
KAFKA_SASL_MECHANISM = os.environ.get('KAFKA_SASL_MECHANISM', 'PLAIN')
KAFKA_SASL_USERNAME = os.environ.get('KAFKA_SASL_USERNAME')
KAFKA_SASL_PASSWORD = os.environ.get('KAFKA_SASL_PASSWORD')
KAFKA_TOPIC_PREFIX = os.environ.get('KAFKA_TOPIC_PREFIX')


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL', 'redis://localhost:6379/0'), 
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                # Use certifi for CA certificates
                "ssl_cert_reqs": "required",
                "ssl_ca_certs": certifi.where()
            }
        }
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('RDS_DB_NAME', 'my_default_db_name'),
        'USER': os.environ.get('RDS_USERNAME', 'my_default_user'),
        'PASSWORD': os.environ.get('RDS_PASSWORD', 'mysecretpassword'),
        'HOST': os.environ.get('RDS_HOSTNAME', 'localhost'),
        'PORT': os.environ.get('RDS_PORT', '5432'),
        'TEST': {
            'NAME': os.environ.get('TEST_DB_NAME', 'test_hacker_news_db'),
            'HOST': os.environ.get('TEST_DB_HOST', 'localhost'),
            'USER': os.environ.get('TEST_DB_USER', 'mysecretpassword'),
            'PASSWORD': os.environ.get('TEST_DB_PASSWORD'),
            'PORT': os.environ.get('TEST_DB_PORT'),
        }
    }
}


DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '0.0.0.0,localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'django_redis',
    'core',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-=+s#eq#s$p@0v^@y(l5z7*k%h&9t&q3!x_g8o9f@w#z@b2q6u7') # Replace in production!

ROOT_URLCONF = 'urls' # Define the root URL configuration

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
  
        'APP_DIRS': True, # Looks for templates in app subdirectories (e.g., admin app's templates)
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

# LOGGING CONFIGURATION
# ==============================================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {module}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO', # Default level for the console handler
            'class': 'logging.StreamHandler',
            'formatter': 'simple', # Use the 'simple' formatter defined above
        },
    },
    'loggers': {
        'django': { # Configure Django's own loggers
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'), # Control Django's verbosity
            'propagate': False, # Don't pass to root logger if handled here
        },
        'tasks': { # Logger for your 'tasks.py' module (and any submodules if named tasks.something)
            'handlers': ['console'],
            'level': 'INFO', # Ensure INFO messages from tasks module are processed
            'propagate': False, # Don't pass to root if we handle it here
        },
 
    },
    'root': { # Fallback for any logger not explicitly configured
        'handlers': ['console'],
        'level': 'WARNING', # Set a higher level for root to reduce noise from other libraries
    }
}

# END LOGGING CONFIGURATION

