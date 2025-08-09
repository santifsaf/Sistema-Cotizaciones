## Índice
1. [Descripción General](#cotizapp)
2. [Funcionalidades Principales](#-funcionalidades-principales)
3. [Tecnologías Utilizadas](#-tecnologías-utilizadas)
4. [Estructura del Proyecto](#-estructura-del-proyecto)
5. [Arquitectura de Base de Datos](#-arquitectura-de-base-de-datos)
6. [Relaciones del Sistema](#-relaciones-del-sistema)
7. [Datos de Demostración](#-datos-de-demostración)
8. [Configuración de Mail](#-configuración-de-mail)
9. [Seguridad y Protección de Login](#-seguridad-protección-contra-intentos-de-login-fallidos)
10. [Decisiones Técnicas](#-decisiones-técnicas)
11. [Ejecución con Docker](#-ejecución-con-docker)
12. [Instalación Manual](#-instalación-manual-sin-docker)
13. [Uso del Sistema](#-uso-del-sistema)

# 📄 CotizApp

**CotizApp** es una aplicación web desarrollada en **Django** que permite gestionar artículos, clientes y empresas para crear cotizaciones de forma simple y profesional.  
Podés loguearte, cargar previamente tus artículos, clientes y datos de tu empresa, y luego crear cotizaciones interactivas que se pueden descargar en PDF, imprimir o enviar por mail. 

## ------------------------------------------------------------------------------------------------------------------
## 🚀 Funcionalidades principales

✅ Views personalizadas para el registro, inicio de sesión de usuarios y la recuperación de contraseña via mail (Bloqueo automático tras 5 intentos fallidos)
✅ Carga y gestión de artículos con filtros de busqueda (nombre o descripcion).   
✅ Carga y gestión de clientes con filtros de busqueda (nombre o empresa).  
✅ Carga de datos de tu empresa (para incluir en la cotización)  
✅ Creación de cotizaciones a partir de artículos cargados (Permite exportar a PDF):  
- Totales, descuentos y cantidad de artículos cotizados actualizados dinámicamente mediante JavaScript.  
✅ Visualización y descarga de cotizaciones en **PDF** (gracias a WeasyPrint)  
- Filtros de busqueda (número de cotizacion o por cliente)
✅ Interfaz responsive básica con **Bootstrap**

## ------------------------------------------------------------------------------------------------------------------

## 🛠️ Tecnologías utilizadas

django-axes==8.0.0
Django 5.1
django-import-export 4.1.1
WeasyPrint 66.0
Docker para containerización
Base de datos: Postgres
Frontend: HTML, CSS, Bootstrap, JavaScript
Control de versiones: GitHub

## ------------------------------------------------------------------------------------------------------------------


## 📁 Estructura del proyecto

```
proyectoWeb/
├── .env.example       # variables de entorno (oculto)
├── .gitignore         # Archivos ignorados por Git (oculto)
├── fixtures           # Datos de demostración  
├── requirements.txt   # Dependencias del proyecto 
├── docker-compose.yml # Configuración de Docker
├── Dockerfile         # Imagen de Docker
├── media              # Archivos subidos por usuarios  
├── cotizApp/          # App principal y configuración Django
│   └── static/        # Archivos estáticos de cotizApp
├── login/             # Gestión de usuarios, autenticación y recuperación personalizada de credenciales
├── articulos/         # CRUD de artículos (FBV)
├── clientes/          # CRUD de clientes (CBV)
└── cotizaciones/      # CRUD de cotizaciones (CBV) con interfaz interactiva y generación de PDFs
```

## ------------------------------------------------------------------------------------------------------------------
## 🗄️ Arquitectura de Base de Datos

    User {
        int id PK
        string username
        string email
        string first_name
        string last_name
        datetime date_joined
        boolean is_active
    }

    Empresa {
        int id PK
        int usuario_log_id FK
        string nombre
        string cuit
        string telefono
        string mail
        datetime created
        date updated
    }

    Clientes {
        int id PK
        int usuario_log_id FK
        string nombre
        string nombre_empresa
        string cuit
        string telefono
        string mail
        datetime created
        date updated
    }

    Articulo {
        int id PK
        int usuario_log_id FK
        string imagen
        string nombre
        string descripcion
        int precio
        datetime created
        date updated
    }

    Cotizaciones {
        int id PK
        int usuario_id FK
        date fecha
        string condiciones_pago
        string numero_referencia UK
        int empresa_id FK
        int cliente_id FK
        text observaciones
        decimal descuento
        decimal total
        decimal total_con_descuento
        decimal costo_envio
        datetime created
        datetime updated
    }

    ArticulosCotizado {
        int id PK
        int cotizacion_id FK
        int articulo_id FK
        int cantidad
    }

## 🔗 Relaciones del Sistema
Relaciones de Usuario (User)

User → Empresa (uno a muchos): Cada usuario puede crear múltiples empresas, pero cada empresa pertenece a un solo usuario
User → Clientes (uno a muchos): Cada usuario puede gestionar múltiples clientes, pero cada cliente está asociado a un solo usuario
User → Articulo (uno a muchos): Cada usuario puede crear múltiples artículos, pero cada artículo pertenece a un solo usuario
User → Cotizaciones (uno a muchos): Cada usuario puede generar múltiples cotizaciones, pero cada cotización es creada por un solo usuario

## Relaciones de Cotizaciones

Empresa → Cotizaciones (uno a muchos): Una empresa puede aparecer en múltiples cotizaciones, pero cada cotización está asociada a una sola empresa
Clientes → Cotizaciones (uno a muchos): Un cliente puede tener múltiples cotizaciones, pero cada cotización pertenece a un solo cliente
Cotizaciones → ArticulosCotizado (uno a muchos): Una cotización puede contener múltiples artículos (items), estableciendo la relación padre-hijo

## Relación Muchos a Muchos

Articulo ↔ Cotizaciones (muchos a muchos): Un artículo puede aparecer en múltiples cotizaciones y una cotización puede contener múltiples artículos. Esta relación se gestiona a través de la tabla intermedia ArticulosCotizado, que además almacena la cantidad de cada artículo en la cotización.

## ------------------------------------------------------------------------------------------------------------------

## 📊 Datos de Demostración

**Para desarrolladores que clonan el repositorio:** Este proyecto incluye un fixture completo con datos de ejemplo para probar todas las funcionalidades.

### Cargar datos demo
```bash
python manage.py loaddata demo_basic_data_utf8
```

**El fixture incluye:**
- **5 Empresas**: TechSolutions, GastroMax, ConstruirYA, EcoLimpio, LogisPro
- **5 Artículos tech**: Mouse Gamer ($45.000), Teclado Mecánico ($75.000), Monitor 24" ($180.000), Auriculares Pro ($150.000), Webcam HD ($88.200)
- **5 Clientes empresariales**: JP Import, ML Textiles, CD Servicios, AT Logística, LG Distribuciones

Una vez cargados los datos, podrás crear cotizaciones usando los artículos y clientes pre-cargados.

## ------------------------------------------------------------------------------------------------------------------

## 📧 Configuración de Mail

Este proyecto incluye funcionalidad de reset de contraseña por email con views personalizadas.

💡 Esta configuración ya está implementada en este proyecto. Solo es necesario editar el .env con los datos de tu cuenta si querés cambiar el remitente o desplegar el proyecto en otro entorno.

Requiere las siguientes variables de entorno en un archivo .env:

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=nombre_de_app@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
DEFAULT_FROM_EMAIL=nombre_de_app@gmail.com
⚠️ Importante: se debe generar una contraseña de aplicación desde la cuenta de Gmail, no usar la contraseña personal.

## ------------------------------------------------------------------------------------------------------------------

## 🔐 Seguridad: Protección contra intentos de login fallidos (django-axes)

Este proyecto usa django-axes para prevenir ataques. 

Después de 5 intentos fallidos, el usuario o IP queda bloqueado temporalmente.

## ⚙️ Configuración
Límite de intentos: 5

Tiempo de bloqueo: 1 hora

Bloqueo combinado por usuario + IP

## 🛠️ Desbloquear usuarios (desde la terminal)
Accedé al shell de Django:
python manage.py shell
Y ejecutá:
from axes.handlers.proxy import AxesProxyHandler

# Desbloquear por nombre de usuario
AxesProxyHandler.reset_attempts(username='usuario')

# O por dirección IP
AxesProxyHandler.reset_attempts(ip_address='127.0.0.1')

# O desbloquear todo 
AxesProxyHandler.reset_attempts()

## ------------------------------------------------------------------------------------------------------------------

## 🔍 Decisiones técnicas

### Arquitectura de Views
El proyecto implementa **ambos enfoques de Django** para demostrar versatilidad técnica:

- **Artículos**: Function-Based Views (FBV) - enfoque tradicional y directo
- **Clientes y Cotizaciones**: Class-Based Views (CBV) - enfoque orientado a objetos

Esta decisión fue intencional para mostrar dominio de ambas metodologías. En proyectos reales, se recomienda mantener consistencia según las preferencias del equipo y la complejidad de la lógica de negocio.

### Containerización con Docker
Aunque CotizApp no es una aplicación con muchas dependencias, decidí implementar containerización como una oportunidad de aprendizaje y buenas prácticas de desarrollo. Docker facilita la reproducibilidad del entorno y simplifica el proceso para otros desarrolladores.

### Personalización del login con Google

Para manejar logins con Google, se implementó un **SocialAccountAdapter** personalizado sobre `django-allauth`.  
Este adapter intercepta el flujo en el método `pre_social_login` y:

- Verifica si ya existe un usuario con el email proporcionado.
- Si existe, conecta automáticamente la cuenta social con el usuario y realiza el login sin pasar por el registro.
- Evita duplicación de usuarios y mejora la experiencia de login.
- Mantiene la compatibilidad con futuras actualizaciones de `django-allauth` sin modificar su código fuente.

Esta decisión técnica permite centralizar la lógica de vinculación de cuentas y mantener el código desacoplado, siguiendo las buenas prácticas recomendadas por Django Allauths

## Uso de Cloudinary para almacenamiento de medios
Se eligió Cloudinary para alojar las imágenes subidas por usuarios (artículos, etc.) por su plan gratuito, CDN global y optimización automática de imágenes.

El campo imagen del modelo Articulo usa CloudinaryField para integración directa con Cloudinary.

Esto elimina la necesidad de almacenar y servir archivos estáticos o media desde el servidor local, mejorando rendimiento y escalabilidad.

Los fixtures referencian imágenes mediante el public_id de Cloudinary.

Se mantiene un placeholder (imagen por defecto) alojado en Cloudinary para artículos sin imagen asignada.

Las credenciales sensibles (API key, secret) se gestionan con variables de entorno para proteger la seguridad.

En desarrollo local se recomienda usar un fallback a imágenes locales para evitar dependencia directa de Cloudinary.

## UptimeRobot 
Se implementó un monitor externo utilizando UptimeRobot para verificar la disponibilidad del sistema cada 5 minutos. Esto se debe a que el servicio de hosting gratuito puede poner la aplicación en estado de suspensión tras periodos de inactividad.


## ------------------------------------------------------------------------------------------------------------------

## 🐳 Ejecución con Docker 

Para facilitar la configuración y despliegue, el proyecto está completamente dockerizado:

### Opción 1: Docker Compose 
```bash
# Clonar el repositorio
git clone https://github.com/usuario/proyectoWeb.git
cd proyectoWeb

# Levantar la aplicación
docker-compose up

# La app estará disponible en http://localhost:8000
```

### Comandos útiles de Docker
```bash
docker-compose build      # Construir la imagen (solo la primera vez)
docker-compose up -d      # Levantar en segundo plano
docker-compose down       # Detener y limpiar contenedores
docker-compose logs       # Ver logs de la aplicación
```

## ------------------------------------------------------------------------------------------------------------------

## 📦 Instalación manual (sin Docker)

### Requerimientos
Ver archivo `requirements.txt` para todas las dependencias.

### Pasos de instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/usuario/proyectoWeb.git
cd proyectoWeb
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Aplicar migraciones:**
```bash
python manage.py migrate
```

5. **Crear un superusuario:**
```bash
python manage.py createsuperuser
```

6. **Ejecutar el servidor de desarrollo:**
```bash
python manage.py runserver
```

## ------------------------------------------------------------------------------------------------------------------

## 🎯 Uso del sistema

### Para usuarios finales:
1. **Registro** → Crear cuenta
2. **Login** → Acceder al sistema  
3. **Configuración** → Cargar datos de empresa
4. **Inventario** → Cargar artículos propios
5. **Clientes** → Agregar información de clientes
6. **Cotizaciones** → Crear y generar PDFs

### Para desarrolladores:
1. **Clone** → Descargar repositorio
2. **Docker** → `docker-compose up` y listo
3. **Fixtures** → Cargar datos demo (opcional)
4. **Testing** → Probar funcionalidades

