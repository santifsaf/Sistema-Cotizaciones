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

- Python 3.11 o posterior (Docker usa 3.11)
- Django 5.2 LTS
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
|-- .env.docker.example # Variables de desarrollo en Docker
|-- requirements.txt
|-- dockerfile
|-- docker-compose.yml
|-- build.sh
|-- start.sh
|-- gunicorn.conf.py
`-- manage.py
```

## Variables de entorno

El repositorio incluye un archivo `.env.example` con las variables necesarias para levantar la app.

Para desarrollo local sin Docker, la configuracion espera el archivo `proyectoWeb/.env`:

```bash
copy .env.example proyectoWeb\.env
```

Variables principales:

```env
SECRET_KEY=tu_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
DATABASE_SSL_REQUIRE=False

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
DATABASE_SSL_REQUIRE=True
DEFAULT_PROTOCOL=https
```

En Render, si existe `RENDER_EXTERNAL_HOSTNAME`, la aplicacion lo usa para `ALLOWED_HOSTS`.
`DATABASE_SSL_REQUIRE` es independiente de `DEBUG` y su valor predeterminado es
`True`. Para PostgreSQL local sin TLS debe ser `False`; SQLite no usa esta opcion.

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

## Actualizar dependencias

Con el entorno virtual activo:

```bash
python -m pip install -r requirements.txt
python -m pip check
python manage.py migrate
python manage.py collectstatic --noinput
```

Las migraciones incluyen las actualizaciones de las aplicaciones externas,
como django-allauth y django-axes. En Docker:

```bash
docker compose up --build -d
```

## Tests

Para correr los tests usando SQLite local:

```powershell
$env:DATABASE_URL='sqlite:///test.sqlite3'
python manage.py collectstatic --noinput
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

Docker Compose es exclusivamente para desarrollo local. Usa una base PostgreSQL
propia y nunca toma `DATABASE_URL` de `proyectoWeb/.env` ni las credenciales de
`proyectoWeb/.env.db`.

En la primera instalacion, crear el archivo local de configuracion:

```powershell
Copy-Item .env.docker.example .env.docker
```

El archivo `.env.docker` no se versiona ni se incluye en la imagen. Completar
Cloudinary y Google solamente si se van a probar esas integraciones; el email
local se imprime en los logs. Las credenciales PostgreSQL incluidas son solo
para la base de desarrollo, que no publica su puerto en el host.

Para levantar la app:

```bash
docker compose up --build -d
docker compose logs -f web
```

La app queda disponible en:

```text
http://localhost:8000
```

Compose espera el healthcheck de PostgreSQL, ejecuta migraciones y
`collectstatic` en el servicio `setup`, y luego inicia `runserver` con recarga
del codigo. Los datos se guardan en el volumen `cotizapp-dev_postgres_data`;
los estaticos generados usan otro volumen para no modificar los archivos del
repositorio. Este proyecto Compose tiene un nombre distinto del anterior y
no reutiliza ni elimina sus datos.

Comandos de administracion:

```bash
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py test --noinput
docker compose down
```

`docker compose down` conserva los datos. Para aplicar nuevas migraciones con
los contenedores ya iniciados, usar `docker compose run --rm setup`.

La imagen de produccion ejecuta como usuario sin privilegios. Su comando
predeterminado es `sh ./start.sh`: recolecta estaticos y arranca Gunicorn.
`gunicorn.conf.py` se carga tambien con el comando directo de Gunicorn y usa
`0.0.0.0:$PORT` (8000 si no existe `PORT`). `WEB_CONCURRENCY` controla los
workers (1 por defecto) y `GUNICORN_TIMEOUT` el timeout (120 segundos).

## Deploy en Render

El servicio existente `Sistema-Cotizaciones` usa el entorno Python nativo de
Render, el repositorio `santifsaf/Sistema-Cotizaciones`, la rama `main` y Root
Directory vacio. Docker se usa para desarrollo local; la imagen local anterior
`proyectoweb-web` no determina el entorno de Render.

Conservar este servicio y su base externa. Las credenciales se configuran en
Environment del servicio, incluyendo Cloudinary, Google y email. No copiar las
variables locales de Docker a Render. `.python-version` fija la rama 3.11,
igual que Docker; Render selecciona su ultimo parche. Si existe una variable
`PYTHON_VERSION` en Environment, tiene prioridad sobre este archivo y debe
contener una version completa compatible, o eliminarse para usar el archivo.

Variables principales de produccion:

```env
DEBUG=False
DATABASE_URL=postgresql://usuario:password@host-externo/base
DATABASE_SSL_REQUIRE=True
DEFAULT_PROTOCOL=https
DEFAULT_DOMAIN=nombre-del-servicio.onrender.com
```

Configurar tambien `SECRET_KEY` con un valor secreto propio. No usar las
credenciales de `.env.docker.example` en Render.

Los cambios son compatibles con los comandos actualmente configurados en
Render, por lo que no es necesario cambiar el panel antes de hacer push:

```sh
# Build Command actual
./build.sh && pip install -r requirements.txt && python manage.py collectstatic --noinput

# Start Command actual
python manage.py migrate && gunicorn proyectoWeb.wsgi:application
```

`build.sh` esta versionado como ejecutable y con finales de linea LF.
La configuracion de Gunicorn se carga automaticamente desde `gunicorn.conf.py`.
El build comprueba las dependencias, genera un PDF de prueba y recolecta los
estaticos antes de que Render arranque la nueva version. Las migraciones siguen
ejecutandose antes de iniciar Gunicorn; la base y las credenciales existentes
se conservan.

Despues del despliegue, se puede simplificar el Build Command a:

```sh
sh ./build.sh
```

El script ya instala `requirements.txt` y ejecuta `collectstatic`; no repetir
esos comandos en el panel de Render.

Si el plan no permite Pre-Deploy Command (por ejemplo, Free), dejar ese campo
vacio y usar este Start Command:

```sh
python manage.py migrate --noinput && sh ./start.sh
```

Esto mantiene las migraciones antes de Gunicorn, como en el arranque anterior.
Se ejecutan una vez por arranque de la instancia, no por worker. En Free solo
hay una instancia; si se habilitan varias instancias, mover las migraciones a
un comando de pre-deploy antes de escalar.

Con un plan que permita pre-deploy, usar:

- Pre-Deploy Command: `python manage.py migrate --noinput`.
- Start Command: `sh ./start.sh`.

Si en el futuro se cambia el servicio a Docker:

- Dockerfile Path: `./dockerfile`.
- Docker Command: dejar vacio para usar `sh ./start.sh` si hay pre-deploy.
- Con pre-deploy, usar `python manage.py migrate --noinput` en ese campo.
- Sin pre-deploy, usar `/bin/sh -c 'python manage.py migrate --noinput && sh ./start.sh'`
  como Docker Command.

`build.sh` instala dependencias Python, comprueba WeasyPrint generando un PDF y recolecta
estaticos. Las bibliotecas Linux de Pango/HarfBuzz deben estar disponibles en el
entorno nativo; si no lo estan, usar Docker, que ya las instala.

Free no permite Render Shell ni jobs puntuales, por lo que esas funciones no
son una alternativa para sus migraciones. Tampoco permite conexiones salientes
a los puertos SMTP 25, 465 o 587: si se usa Free, el registro y la recuperacion
de contrasena requieren un proveedor de email accesible por HTTPS o un plan
que permita SMTP. Esto no se resuelve cambiando los comandos de arranque.

Las imagenes de usuarios se conservan en Cloudinary; el filesystem del servicio
no debe usarse como almacenamiento persistente de uploads. El Auto-Deploy
actual es On Commit: un push a `main` dispara un despliegue.

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
