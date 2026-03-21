# Deploy Django a Render con Docker y MariaDB

## Pasos para deployar:

### 1. Actualizar requirements.txt
```bash
pip install gunicorn whitenoise
pip freeze > requirements.txt
```

### 2. Subir a GitHub
```bash
git add .
git commit -m "Agregar configuración Docker para Render con MariaDB"
git push origin main
```

### 3. Crear servicio MariaDB en Render (Opcional)

Si aún no tienes una base de datos MariaDB:

1. Ve a render.com → "New +" → "MySQL"
2. Nombre: `proyecto-db`
3. Copia las credenciales cuando se cree

**O usa un proveedor externo como:**
- **PlanetScale** (MySQL compatible)
- **ClearDB** (MySQL en Heroku)
- Tu propio servidor MariaDB

### 4. En Render.com - Crear Web Service

1. **Crear nuevo servicio:**
   - Ve a render.com → "New +" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Selecciona la rama `main`

2. **Configuración del servicio:**
   - **Name:** tu-app-django
   - **Environment:** Docker
   - **Build Command:** `docker build -f deploy/Dockerfile -t app .`
   - **Start Command:** `gunicorn --bind 0.0.0.0:8000 --workers 4 SGIEVpy.wsgi:application`

3. **Variables de entorno (MUY IMPORTANTE):**

   | Nombre | Valor |
   |--------|-------|
   | `DEBUG` | `False` |
   | `SECRET_KEY` | Clickear "Generate" para autogenerar |
   | `ALLOWED_HOSTS` | `tu-app.onrender.com` |
   | `DB_ENGINE` | `django.db.backends.mysql` |
   | `DB_NAME` | nombre de tu BD en MariaDB |
   | `DB_USER` | usuario de MariaDB |
   | `DB_PASSWORD` | contraseña de MariaDB |
   | `DB_HOST` | host de tu MariaDB (ej: `db.onrender.com`) |
   | `DB_PORT` | `3306` |

4. **Plan:** Free (recomendado inicialmente)

### 5. Ejecutar migraciones después del deploy

Una vez que el servicio esté deployado, abre la consola de Render:

```bash
python manage.py migrate
```

### 6. Crear usuario administrador (Opcional)

```bash
python manage.py createsuperuser
# o
python crear_usuarios.py
```

## Notas importantes:

- El `Dockerfile` está en la carpeta `deploy/`
- MariaDB es compatible con MySQL en Django
- Asegúrate de que `requirements.txt` esté actualizado
- No subas `secrets` al repositorio (usa Environment Variables)
- El archivo `.dockerignore` excluye archivos innecesarios
- `whitenoise` maneja archivos estáticos en producción

## Para probar localmente con Docker:

```bash
# Construir la imagen
docker build -f deploy/Dockerfile -t mi-app:latest .

# Ejecutar el contenedor
docker run -p 8000:8000 \
  -e DB_NAME=proyecto \
  -e DB_USER=root \
  -e DB_PASSWORD="" \
  -e DB_HOST=host.docker.internal \
  mi-app:latest

# O usar docker-compose
docker-compose up --build
```

## Troubleshooting:

**Error: "Can't connect to MySQL server"**
- Verifica las credenciales de BD en Environment Variables
- Asegúrate de que el host de BD sea accesible desde Render

**Error: "No such file or directory: 'deploy/Dockerfile'"**
- Revisa que el `Dockerfile Path` sea: `deploy/Dockerfile`

**Static files no se cargan**
- Las dependencias de `whitenoise` deben estar en `requirements.txt`
- Ejecuta `python manage.py collectstatic --noinput`
