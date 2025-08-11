import os
import django
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectoWeb.settings')
django.setup()

username = 'santif'
email = 'santiagoafuentes@gmail.com'
password = 'Borusia0605'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' creado.")
else:
    print(f"Superuser '{username}' ya existe.")