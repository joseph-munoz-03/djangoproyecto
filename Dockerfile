FROM python:3.12-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=SGIEVpy.settings

# Directorio de trabajo
WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar proyecto
COPY . .

# Carpeta de estáticos
RUN mkdir -p staticfiles

# 🚀 Comando de inicio (IMPORTANTE)
CMD bash -c "\
python manage.py migrate --noinput && \
python manage.py collectstatic --noinput && \
python crear_usuarios.py && \
python crear_ventas.py && \
gunicorn --bind 0.0.0.0:${PORT:-10000} --workers 1 --worker-class sync SGIEVpy.wsgi:application\
"