# 📄 CotizApp

**CotizApp** es una aplicación web desarrollada en **Django** que permite gestionar artículos, clientes y empresas para crear cotizaciones de forma simple y profesional.  
Podés loguearte, cargar previamente tus artículos, clientes y datos de tu empresa, y luego crear cotizaciones interactivas que se pueden descargar en PDF, imprimir o enviar por mail. 

---

## 🚀 Funcionalidades principales

✅ Registro e inicio de sesión de usuarios  
✅ Views personalizadas para la recuperación de contraseña  
✅ Carga y administración de artículos  
✅ Carga y administración de clientes  
✅ Carga de datos de tu empresa (para incluir en la cotización)  
✅ Creación de cotizaciones a partir de artículos cargados:  
- Totales, descuentos y cantidad de artículos cotizados actualizados dinámicamente mediante JavaScript  
✅ Visualización y descarga de cotizaciones en **PDF** (gracias a WeasyPrint)  
✅ Interfaz responsive básica con **Bootstrap**

---

## 🛠️ Tecnologías utilizadas

- [Django 5.1](https://www.djangoproject.com/)
- [django-import-export 4.1.1](https://django-import-export.readthedocs.io/)
- [WeasyPrint 66.0](https://weasyprint.org/)
- **Docker** para containerización
- Base de datos: **SQLite**
- Frontend: **HTML**, **CSS**, **Bootstrap**, **JavaScript**
- Control de versiones: **GitHub**

---

## 🐳 Ejecución con Docker (Recomendado)

Para facilitar la configuración y despliegue, el proyecto está completamente dockerizado:

### Opción 1: Docker Compose (la más fácil)
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

---

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

---

## 📧 Configuración de Email

Este proyecto incluye funcionalidad de **reset de contraseña por email** con views personalizadas.

### Desarrollo
- Configurado para mostrar emails en consola
- No requiere configuración adicional

### Producción
Requiere configurar variables de entorno. Crear archivo `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
DEFAULT_FROM_EMAIL=tu_email@gmail.com
```

---

## 📊 Datos de Demostración

**Para desarrolladores que clonan el repositorio:** Este proyecto incluye un fixture completo con datos de ejemplo para probar todas las funcionalidades.

### Cargar datos demo
```bash
python manage.py loaddata fixtures/demo_data.json
```

**El fixture incluye:**
- **5 Empresas**: TechSolutions, GastroMax, ConstruirYA, EcoLimpio, LogisPro
- **5 Artículos tech**: Mouse Gamer ($45.000), Teclado Mecánico ($75.000), Monitor 24" ($180.000), Auriculares Pro ($150.000), Webcam HD ($88.200)
- **5 Clientes empresariales**: JP Import, ML Textiles, CD Servicios, AT Logística, LG Distribuciones

Una vez cargados los datos, podrás crear cotizaciones usando los artículos y clientes pre-cargados.

---

## 📁 Estructura del proyecto

```
proyectoWeb/
├── fixtures         # Datos de demostración  
├── requirements.txt  # Dependencias del proyecto 
├── docker-compose.yml # Configuración de Docker
├── Dockerfile        # Imagen de Docker
├── media/            # Archivos subidos por usuarios  
├── cotizApp/         # App principal y configuración Django
│   └── static/       # Archivos estáticos de cotizApp
├── login/            # Gestión de usuarios, autenticación y recuperación personalizada de credenciales
├── articulos/        # CRUD de artículos (FBV)
├── clientes/         # CRUD de clientes (CBV)
└── cotizaciones/     # CRUD de cotizaciones (CBV) con funcionalidad para generar PDFs
```

---

## 🔍 Decisiones técnicas

### Arquitectura de Views
El proyecto implementa **ambos enfoques de Django** para demostrar versatilidad técnica:

- **Artículos**: Function-Based Views (FBV) - enfoque tradicional y directo
- **Clientes y Cotizaciones**: Class-Based Views (CBV) - enfoque orientado a objetos

Esta decisión fue **intencional** para mostrar dominio de ambas metodologías. En proyectos reales, se recomienda mantener consistencia según las preferencias del equipo y la complejidad de la lógica de negocio.

### Containerización con Docker
Aunque CotizApp no es una aplicación compleja que requiera necesariamente Docker, decidí implementar containerización como una oportunidad de aprendizaje y buenas prácticas de desarrollo. Docker facilita la reproducibilidad del entorno y simplifica el proceso de setup para otros desarrolladores.

---

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

