# Deploy Django a Render con Docker

## Pasos para deployar:

### 1. Actualizar requirements.txt
```bash
pip install gunicorn whitenoise
pip freeze > requirements.txt
```

### 2. Subir a GitHub
```bash
git add .
git commit -m "Agregar configuración Docker para Render"
git push origin main
```

### 3. En Render.com

1. **Crear nuevo servicio:**
   - Ve a render.com → "New +" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Selecciona la rama `main`

2. **Configuración del servicio:**
   - **Name:** tu-app-name
   - **Environment:** Docker
   - **Build Command:** `docker build -f deploy/Dockerfile -t app .`
   - **Start Command:** `gunicorn --bind 0.0.0.0:8000 --workers 4 SGIEVpy.wsgi:application`

3. **Variables de entorno (muy importante):**
   ```
   DEBUG=False
   ALLOWED_HOSTS=tu-app.onrender.com
   SECRET_KEY=tu-clave-secreta-muy-segura
   DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_bd
   ```

4. **Plan:** Free (recomendado inicialmente) o superior si lo requieres

### 4. Configurar settings.py para producción

```python
# settings.py
import os
import dj_database_url

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

# Base de datos
if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600
        )
    }

# Archivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Seguridad en producción
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
```

### 5. En producción - Ejecutar migraciones:

Una vez deployado en Render, ejecuta:
```bash
render-deploy: python manage.py migrate
```

O en la consola de Render:
```bash
python manage.py migrate
```

## Notas importantes:

- El `Dockerfile` está en la carpeta `deploy/`
- Asegúrate de que `requirements.txt` esté actualizado
- No subas `secrets` al repositorio (usa Environment Variables)
- El archivo `.dockerignore` excluye archivos innecesarios
- Para bases de datos MySQL, usa `dj_database_url` con `DATABASE_URL`

## Para probar localmente con Docker:

```bash
# Ir a la carpeta deploy
cd deploy

# Construir la imagen
docker build -f Dockerfile -t mi-app:latest ..

# Ejecutar el contenedor
docker run -p 8000:8000 mi-app:latest

# O usar docker-compose
docker-compose up --build
```
