from pathlib import Path
from django.contrib.messages import constants as messages
from decouple import config
import dj_database_url
import os
import cloudinary

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'proyectoWeb', 'fixtures'),
]


ALLOWED_HOSTS = []



INSTALLED_APPS = [
    'crispy_forms',
    'crispy_bootstrap5',
    'login',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cotizApp',
    'articulos',
    'clientes',
    'cotizaciones',
    'import_export',
    'axes',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 1 
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret': config('GOOGLE_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

SOCIALACCOUNT_ADAPTER = 'login.adapters.MySocialAccountAdapter'


# Configuración para forzar verificación email
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = "mandatory" 
SOCIALACCOUNT_EMAIL_VERIFICATION = "optional"



CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'axes.middleware.AxesMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]


AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend", 
    "django.contrib.auth.backends.ModelBackend",
    'allauth.account.auth_backends.AuthenticationBackend',
]

AXES_FAILURE_LIMIT = 5  
AXES_COOLOFF_TIME = 1 
AXES_LOCKOUT_PARAMETERS = ['username', 'ip_address']
AXES_VERBOSE = True
AXES_RESET_ON_SUCCESS = True 
AXES_ENABLE_ADMIN = True

ROOT_URLCONF = 'proyectoWeb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'login' / 'templates'],
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

WSGI_APPLICATION = 'proyectoWeb.wsgi.application'


DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=not config('DEBUG', default=False, cast=bool),
    )
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8,}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es' 
USE_I18N = True
USE_L10N = True
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET'),
    secure=True,
)

STATIC_URL = 'static/'        
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = [
    BASE_DIR / "cotizApp/static",    
]

STATIC_ROOT= BASE_DIR / 'staticfiles'    

MEDIA_URL = '/media/'

MEDIA_ROOT=BASE_DIR / 'proyectoWeb/media'  


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}

LOGOUT_REDIRECT_URL = '/home/'
LOGIN_REDIRECT_URL = '/home/'
LOGIN_URL = '/login/registration/login/'
LOGIN_REDIRECT_URL = '/home/' 

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

ALLOWED_HOSTS = [EXTERNAL_HOSTNAME] if EXTERNAL_HOSTNAME else ['localhost', '127.0.0.1']


# Configuración de email
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')


# Configuración SMTP (para producción)
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@tudominio.com')
SERVER_EMAIL = config('SERVER_EMAIL', default='noreply@tudominio.com')

# Configuración para reset de contraseña
PASSWORD_RESET_TIMEOUT = config('PASSWORD_RESET_TIMEOUT', default=3600, cast=int)
DEFAULT_DOMAIN = config('DEFAULT_DOMAIN', default='127.0.0.1:8000')
DEFAULT_PROTOCOL = config('DEFAULT_PROTOCOL', default='http')

# En settings.py para producción
if not DEBUG:
     SECURE_SSL_REDIRECT = True
     SECURE_HSTS_SECONDS = 31536000
     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
     SECURE_HSTS_PRELOAD = True
     SESSION_COOKIE_SECURE = True
     CSRF_COOKIE_SECURE = True

     SESSION_COOKIE_HTTPONLY = True
     CSRF_COOKIE_HTTPONLY = True
     X_FRAME_OPTIONS = 'DENY'
    
    # Para servidores proxy (como Nginx)
     SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
