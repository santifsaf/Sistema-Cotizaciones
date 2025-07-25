# 📄 CotizApp

**CotizApp** es una aplicación web desarrollada en **Django** que permite gestionar artículos, clientes y empresas para crear cotizaciones de forma simple y profesional.  
Podés loguearte, cargar previamente tus artículos, clientes y datos de tu empresa, y luego crear cotizaciones interactivas que se pueden descargar en PDF, imprimir o enviar por mail. 

---

## 🚀 Funcionalidades principales

✅ Registro e inicio de sesión de usuarios.  
✅ Carga y administración de artículos.  
✅ Carga y administración de clientes.  
✅ Carga de datos de tu empresa (para incluir en la cotización).  
✅ Creación de cotizaciones a partir de artículos cargados:  
- Totales, descuentos y cantidad de articulos cotizados actualizados dinámicamente mediante un script JS.  
✅ Visualización y descarga de cotizaciones en **PDF** (gracias a WeasyPrint).  
✅ Interfaz responsive básica con **Bootstrap**.

---

## 🛠️ Tecnologías utilizadas

- [Django 5.1](https://www.djangoproject.com/)
- [Django REST Framework 3.15.2](https://www.django-rest-framework.org/)
- [django-import-export 4.1.1](https://django-import-export.readthedocs.io/)
- [WeasyPrint 66.0](https://weasyprint.org/)
- Base de datos: **SQLite**
- Frontend: **HTML**, **CSS básico**, **Bootstrap**, **JavaScript puro**
- Control de versiones: **GitHub**

---

## 📦 Requerimientos

Archivo `requirements.txt` 

Instalalos con:

```bash
pip install -r requirements.txt



⚙️ Instalación y ejecución

1. Clonar el repositorio:
git clone https://github.com/usuario/CotizApp.git
cd CotizApp

2. Crear entorno virtual (opcional pero recomendado):
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

3. Instalar dependencias:
pip install -r requirements.txt

4. Aplicar migraciones:
python manage.py migrate

5.Crear un superusuario:
python manage.py createsuperuser

6.Ejecutar el servidor de desarrollo:
python manage.py runserver