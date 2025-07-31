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
- Base de datos: **SQLite**
- Frontend: **HTML**, **CSS**, **Bootstrap**, **JavaScript**
- Control de versiones: **GitHub**

---

## 📦 Instalación y configuración

### Requerimientos
Ver archivo `requirements.txt` para todas las dependencias.

### Pasos de instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/usuario/proyectoWeb.git
cd proyectoWeb
```

2. **Crear entorno virtual (recomendado):**
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
├── cotizApp/          # App principal y configuración Django
├── login/             # Gestión de usuarios y autenticación
├── articulos/         # CRUD de artículos (FBV)
├── clientes/          # CRUD de clientes (CBV)
├── cotizaciones/      # CRUD de cotizaciones (CBV)
├── static/            # Archivos estáticos globales
├── fixtures/          # Datos de demostración
├── media/             # Archivos subidos por usuarios
└── requirements.txt   # Dependencias del proyecto
```

**Nota**: Cada app contiene sus propios templates en `app/templates/`

---

## 🔍 Decisiones técnicas

### Arquitectura de Views
El proyecto implementa **ambos enfoques de Django** para demostrar versatilidad técnica:

- **Artículos**: Function-Based Views (FBV) - enfoque tradicional y directo
- **Clientes y Cotizaciones**: Class-Based Views (CBV) - enfoque orientado a objetos

Esta decisión fue **intencional** para mostrar dominio de ambas metodologías. En proyectos reales, se recomienda mantener consistencia según las preferencias del equipo y la complejidad de la lógica de negocio.

### Otras decisiones de arquitectura

No se implementó **API REST** ya que el proyecto funciona completamente desde el navegador mediante vistas clásicas de Django. Se puede agregar fácilmente con Django REST Framework si se requiere una aplicación móvil o frontend moderno.

**Caché**: No se aplicó cacheado porque el sistema no maneja alto tráfico ni grandes volúmenes de datos. 

**Seguridad**: El proyecto usa el sistema de sesiones estándar de Django. No se incluyó seguimiento de tokens avanzado porque no hay sesiones distribuidas ni múltiples dispositivos por usuario.

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
2. **Setup** → Configurar entorno
3. **Fixtures** → Cargar datos demo
4. **Testing** → Probar funcionalidades
