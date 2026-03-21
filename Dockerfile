FROM python:3.12-slim

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema para MariaDB
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    mariadb-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn whitenoise

# Copiar el proyecto
COPY . .

# Crear directorio para archivos estáticos
RUN mkdir -p staticfiles

# Ejecutar migraciones y recopilar archivos estáticos
RUN python manage.py collectstatic --noinput || true
