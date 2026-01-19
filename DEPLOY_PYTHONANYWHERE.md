# Guia de Despliegue en PythonAnywhere

Esta guia te ayudara a desplegar San Cipriano en PythonAnywhere (gratis) y verificarlo en Google Search Console.

## Paso 1: Crear cuenta en PythonAnywhere

1. Ve a https://www.pythonanywhere.com/registration/register/beginner/
2. Crea una cuenta gratuita (Beginner)
3. Tu sitio sera: `tuusuario.pythonanywhere.com`

## Paso 2: Subir el codigo

### Opcion A: Usando Git (Recomendada)

1. En PythonAnywhere, abre una **Bash console**
2. Clona tu repositorio:
```bash
cd ~
git clone https://github.com/TU_USUARIO/san-cipriano.git
```

### Opcion B: Subir archivos manualmente

1. Ve a la pestana **Files**
2. Sube un archivo ZIP de tu proyecto
3. Descomprime con: `unzip san-cipriano.zip`

## Paso 3: Configurar el entorno virtual

En la consola Bash de PythonAnywhere:

```bash
cd ~/san-cipriano

# Crear entorno virtual
mkvirtualenv --python=/usr/bin/python3.11 sancipriano

# Activar entorno (se activa automaticamente al crearlo)
workon sancipriano

# Instalar dependencias
pip install -r requirements/pythonanywhere.txt
```

## Paso 4: Configurar variables de entorno

1. Crea el archivo `.env` en ~/san-cipriano/:

```bash
nano ~/san-cipriano/.env
```

2. Agrega las siguientes variables:

```env
DEBUG=False
SECRET_KEY=genera-una-clave-secreta-aqui-muy-larga-y-segura
ALLOWED_HOSTS=tuusuario.pythonanywhere.com
DJANGO_SETTINGS_MODULE=config.settings.pythonanywhere
```

Para generar una SECRET_KEY:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Paso 5: Configurar la base de datos

```bash
cd ~/san-cipriano
workon sancipriano

# Crear tablas
python manage.py migrate --settings=config.settings.pythonanywhere

# Crear cache table
python manage.py createcachetable --settings=config.settings.pythonanywhere

# Cargar datos iniciales
python manage.py setup_initial_data --settings=config.settings.pythonanywhere

# Crear superusuario
python manage.py createsuperuser --settings=config.settings.pythonanywhere

# Recopilar archivos estaticos
python manage.py collectstatic --noinput --settings=config.settings.pythonanywhere
```

## Paso 6: Configurar la Web App

1. Ve a la pestana **Web** en PythonAnywhere
2. Click en **Add a new web app**
3. Selecciona **Manual configuration**
4. Selecciona **Python 3.11**

### Configurar rutas:

**Source code:** `/home/tuusuario/san-cipriano`

**Working directory:** `/home/tuusuario/san-cipriano`

**Virtualenv:** `/home/tuusuario/.virtualenvs/sancipriano`

### Configurar WSGI:

Click en el enlace del archivo WSGI y reemplaza TODO el contenido con:

```python
import os
import sys

# Agregar el directorio del proyecto al path
path = '/home/tuusuario/san-cipriano'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.pythonanywhere'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**IMPORTANTE:** Cambia `tuusuario` por tu nombre de usuario real.

### Configurar archivos estaticos:

En la seccion "Static files", agrega:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/tuusuario/san-cipriano/staticfiles` |
| `/media/` | `/home/tuusuario/san-cipriano/media` |

## Paso 7: Actualizar settings de PythonAnywhere

Edita el archivo `config/settings/pythonanywhere.py`:

```bash
nano ~/san-cipriano/config/settings/pythonanywhere.py
```

Cambia `tuusuario` por tu usuario real de PythonAnywhere:

```python
ALLOWED_HOSTS = [
    'tuusuario.pythonanywhere.com',
]

CORS_ALLOWED_ORIGINS = [
    'https://tuusuario.pythonanywhere.com',
]
```

## Paso 8: Recargar la aplicacion

1. En la pestana **Web**, click en **Reload**
2. Visita `https://tuusuario.pythonanywhere.com`

## Paso 9: Verificar en Google Search Console

### 9.1. Ir a Google Search Console

1. Ve a https://search.google.com/search-console/welcome
2. Inicia sesion con tu cuenta de Google

### 9.2. Agregar propiedad

1. Selecciona **URL prefix**
2. Ingresa: `https://tuusuario.pythonanywhere.com`
3. Click en **Continue**

### 9.3. Verificar propiedad

Google te dara varias opciones. La mas facil es **HTML file**:

1. Google te dara un nombre de archivo como: `googleXXXXXXXXXXXXXXXX.html`
2. Tu sitio ya esta preparado para esto! Solo visita:
   `https://tuusuario.pythonanywhere.com/googleXXXXXXXXXXXXXXXX.html`
3. Click en **Verify** en Google Search Console

Alternativa con meta tag:
Si prefieres usar meta tag, edita `base.html` y agrega en el `<head>`:
```html
<meta name="google-site-verification" content="TU_CODIGO_DE_GOOGLE" />
```

### 9.4. Enviar Sitemap

1. En Search Console, ve a **Sitemaps** (menu izquierdo)
2. Agrega: `sitemap.xml`
3. Click en **Submit**

Tu sitemap esta en: `https://tuusuario.pythonanywhere.com/sitemap.xml`

## Paso 10: Verificar SEO

Visita estas URLs para verificar que todo funciona:

- **Sitio:** https://tuusuario.pythonanywhere.com
- **Sitemap:** https://tuusuario.pythonanywhere.com/sitemap.xml
- **Robots.txt:** https://tuusuario.pythonanywhere.com/robots.txt
- **Admin:** https://tuusuario.pythonanywhere.com/admin/

## Mantenimiento

### Actualizar codigo:

```bash
cd ~/san-cipriano
git pull
workon sancipriano
pip install -r requirements/pythonanywhere.txt
python manage.py migrate --settings=config.settings.pythonanywhere
python manage.py collectstatic --noinput --settings=config.settings.pythonanywhere
```

Luego recarga la app en la pestana Web.

### Ver logs de errores:

En la pestana Web, hay enlaces a los logs:
- **Error log:** Para ver errores de la aplicacion
- **Server log:** Para ver requests HTTP

## Limitaciones del plan gratuito

- CPU limitada (puede ser lento)
- Sin tareas programadas (Celery)
- Sin Redis/cache en memoria
- 512MB de almacenamiento
- El sitio se suspende si no lo visitas en 3 meses

## Migrar a dominio propio (futuro)

Cuando compres tu dominio (ej: `sancipriano.co`):

1. En PythonAnywhere (plan de pago requerido), agrega el dominio personalizado
2. Configura los DNS en tu registrador
3. Agrega el nuevo dominio a Google Search Console
4. Actualiza ALLOWED_HOSTS en settings

---

## Soporte

Si tienes problemas:
1. Revisa los logs de error en PythonAnywhere
2. Verifica que el virtualenv este activado
3. Asegurate de que las rutas en WSGI sean correctas
