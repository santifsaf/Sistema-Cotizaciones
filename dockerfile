# Imagen base de Python
FROM python:3.11-slim

# Directorio de la app
WORKDIR /app

# Variables de entorno para optimizar opcionales
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copia e instala dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir
RUN pip install -r requirements.txt


# Instala librerías necesarias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*


# Copia el código fuente de la app
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
