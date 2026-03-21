FROM python:3.12-slim

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=SGIEVpy.settings

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema para PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar el proyecto
COPY . .

# Crear directorio para archivos estáticos
RUN mkdir -p staticfiles

# Comando de inicio
CMD bash -c "python manage.py migrate --noinput && python manage.py collectstatic --noinput && python crear_usuarios.py && gunicorn --bind 0.0.0.0:${PORT:-10000} --workers 1 --worker-class sync SGIEVpy.wsgi:application"

# No ejecutar collectstatic en build time (requiere BD)
