# CotizApp

CotizApp es una aplicacion web desarrollada con Django para gestionar articulos, clientes y empresas, y generar cotizaciones profesionales en PDF.

La app permite que cada usuario administre sus propios datos, cree cotizaciones con articulos previamente cargados y conserve informacion historica de clientes, empresas y precios aunque esos registros se modifiquen o eliminen despues.

## Funcionalidades

- Registro, login y recuperacion de contrasena por email.
- Verificacion de email para nuevos usuarios.
- Login con Google mediante `django-allauth`.
- Proteccion contra intentos fallidos de login con `django-axes`.
- Gestion de empresas propias.
- Gestion de clientes propios.
- Gestion de articulos propios con imagen, descripcion y precio.
- Creacion de cotizaciones con multiples articulos.
- Calculo automatico de cantidades, descuentos y totales.
- Condiciones de pago:
  - `Precio de lista`: mantiene el precio original del articulo.
  - `Efectivo`: aplica un 10% de descuento sobre el precio del articulo.
- Generacion y descarga de cotizaciones en PDF.
- Busqueda de articulos, clientes y cotizaciones.
- Almacenamiento de imagenes con Cloudinary.
- Archivos estaticos servidos con WhiteNoise.

## Tecnologias

- Python
- Django
- PostgreSQL
- SQLite para desarrollo local opcional
- Bootstrap
- JavaScript
- WeasyPrint
- Cloudinary
- django-allauth
- django-axes
- WhiteNoise
- Docker
- Gunicorn

## Estructura del proyecto

```text
proyectoWeb/
|-- articulos/        # Gestion de articulos
|-- clientes/         # Gestion de clientes
|-- cotizaciones/     # Creacion, listado y PDF de cotizaciones
|-- cotizApp/         # App principal, templates base y archivos estaticos
|-- login/            # Autenticacion, registro y recuperacion de contrasena
|-- proyectoWeb/      # Configuracion principal de Django
|-- .env.example      # Ejemplo de variables de entorno
|-- requirements.txt
|-- dockerfile
|-- docker-compose.yml
|-- build.sh
`-- manage.py
```

## Variables de entorno

El repositorio incluye un archivo `.env.example` con las variables necesarias para levantar la app.

Para desarrollo local y Docker Compose, la configuracion actual espera el archivo `proyectoWeb/.env`:

```bash
copy .env.example proyectoWeb\.env
```

Variables principales:

```env
SECRET_KEY=tu_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret

GOOGLE_CLIENT_ID=tu_google_client_id
GOOGLE_SECRET=tu_google_secret

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
DEFAULT_FROM_EMAIL=tu_email@gmail.com
SERVER_EMAIL=tu_email@gmail.com

PASSWORD_RESET_TIMEOUT=3600
DEFAULT_DOMAIN=127.0.0.1:8000
DEFAULT_PROTOCOL=http
```

Para produccion:

```env
DEBUG=False
DATABASE_URL=postgres://usuario:password@host:puerto/db
DEFAULT_PROTOCOL=https
```

En Render, si existe `RENDER_EXTERNAL_HOSTNAME`, la aplicacion lo usa para `ALLOWED_HOSTS`.

## Instalacion local

```bash
git clone https://github.com/santifsaf/Sistema-Cotizaciones.git
cd Sistema-Cotizaciones

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

La app queda disponible en:

```text
http://127.0.0.1:8000
```

## Tests

Para correr los tests usando SQLite local:

```powershell
$env:DATABASE_URL='sqlite:///test.sqlite3'
python manage.py test
```

Tambien se pueden ejecutar los checks de Django:

```bash
python manage.py check
python manage.py check --deploy
```

## Datos de demostracion

El proyecto incluye fixtures con datos de ejemplo:

```bash
python manage.py loaddata demo_basic_data_utf8
```

Incluye empresas, clientes y articulos de prueba para crear cotizaciones rapidamente.

## Modelo de datos principal

- `Empresa`: datos de la empresa del usuario.
- `Clientes`: clientes asociados al usuario.
- `Articulo`: articulos cargados por el usuario.
- `Cotizaciones`: cabecera de la cotizacion.
- `ArticulosCotizado`: articulos incluidos en cada cotizacion.

Las cotizaciones guardan datos historicos de empresa, cliente y articulos para que los PDFs sigan mostrando la informacion original aunque luego se editen o eliminen registros.

## Reglas de negocio

- Cada usuario solo puede ver y administrar sus propios articulos, clientes, empresas y cotizaciones.
- Las cotizaciones se crean a partir de articulos propios del usuario logueado.
- Si una cotizacion usa `Precio de lista`, se guarda el precio original del articulo.
- Si una cotizacion usa `Efectivo`, se guarda el precio del articulo con un 10% de descuento.
- Los descuentos adicionales de la cotizacion se aplican sobre el subtotal de los articulos cotizados.
- El costo de envio se guarda como dato separado del subtotal.

## Seguridad

La aplicacion incluye:

- Login requerido para acceder a vistas privadas.
- Separacion de datos por usuario.
- Proteccion contra intentos fallidos de login con `django-axes`.
- Redireccion HTTPS y cookies seguras cuando `DEBUG=False`.
- Variables sensibles fuera del codigo fuente.
- Archivos estaticos servidos con WhiteNoise.
- Imagenes de usuarios almacenadas en Cloudinary.

## Docker

Para levantar la app con Docker Compose:

```bash
docker-compose up --build
```

La app queda disponible en:

```text
http://localhost:8000
```

La configuracion de Docker Compose usa:

- `proyectoWeb/.env` para las variables de la app.
- `proyectoWeb/.env.db` para las variables del contenedor PostgreSQL.

## Deploy

La aplicacion esta preparada para deploy con:

- PostgreSQL mediante `DATABASE_URL`.
- WhiteNoise para archivos estaticos.
- Cloudinary para imagenes.
- Gunicorn como servidor WSGI.
- Variables de entorno para credenciales y configuracion sensible.

Antes de deployar:

```bash
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic --noinput
```

## Uso del sistema

1. Registrarse o iniciar sesion.
2. Cargar los datos de empresa.
3. Cargar clientes.
4. Cargar articulos.
5. Crear una cotizacion seleccionando cliente, empresa, condicion de pago y articulos.
6. Descargar la cotizacion en PDF.
