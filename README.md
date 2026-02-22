# 🌿 San Cipriano - Sitio Web Oficial de la Comunidad

Sitio web oficial de la comunidad de San Cipriano, Colombia. Enfocado en turismo comunitario, conservación ambiental y control responsable de visitantes.

## Descripción

San Cipriano es una reserva natural en el Valle del Cauca, Colombia, gestionada por su comunidad. Este sitio web sirve como punto central para:

- Atraer turistas responsables
- Proteger la reserva mediante información controlada
- Centralizar las consultas de visitantes
- Canalizar reservas sin exponer precios públicamente

## Características

- 🌐 **Multiidioma**: Español, Inglés, Francés, Alemán, Italiano, Portugués
- 📱 **Mobile First**: Diseño responsivo optimizado para móviles
- 📋 **Formulario de Consulta**: Captura de datos antes de liberar información detallada
- 📊 **Contador de Visitantes**: Muestra interés público en la reserva
- 📧 **Notificaciones**: Email y WhatsApp automáticos
- 🔒 **Información Protegida**: Precios y rutas solo después del registro

## Stack Tecnológico

### Backend
- Django 4.2
- Django REST Framework
- PostgreSQL 15
- Redis 7
- Celery

### Frontend
- Tailwind CSS (via CDN)
- JavaScript Vanilla

### Infraestructura
- Docker & Docker Compose
- Nginx
- Gunicorn

## Instalación

### Requisitos
- Docker y Docker Compose
- Git

### Desarrollo Local

1. Clonar el repositorio:
```bash
git clone https://github.com/QuickAppraiser/san-cipriano.git
cd san-cipriano
```

2. Copiar variables de entorno:
```bash
cp .env.example .env
```

3. Iniciar los servicios:
```bash
docker-compose up -d
```

4. Aplicar migraciones:
```bash
docker-compose exec web python manage.py migrate
```

5. Crear superusuario:
```bash
docker-compose exec web python manage.py createsuperuser
```

6. Acceder al sitio:
- Sitio: http://localhost:8000
- Admin: http://localhost:8000/admin

### Producción

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Estructura del Proyecto

```
san-cipriano/
├── apps/
│   ├── core/           # Configuración del sitio, utilidades
│   ├── visitors/       # Formulario y contador de visitantes
│   ├── content/        # Páginas estáticas, biodiversidad
│   └── notifications/  # WhatsApp y Email
├── config/
│   ├── settings/       # Configuración Django (base, dev, prod)
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
├── templates/          # Plantillas HTML
├── static/             # Archivos estáticos
├── locale/             # Traducciones
├── requirements/       # Dependencias Python
├── nginx/              # Configuración Nginx
├── docker-compose.yml
└── Dockerfile
```

## Configuración

### Variables de Entorno Importantes

| Variable | Descripción |
|----------|-------------|
| `SECRET_KEY` | Clave secreta de Django |
| `POSTGRES_*` | Configuración de base de datos |
| `WHATSAPP_API_TOKEN` | Token de WhatsApp Business API |
| `RESEND_API_KEY` | API Key para emails |
| `COMMUNITY_WHATSAPP` | Número de WhatsApp de la comunidad |

### WhatsApp Integration

Para configurar WhatsApp Business API:
1. Crear una cuenta en Meta Business
2. Configurar WhatsApp Business API
3. Obtener el token y phone ID
4. Configurar las variables en `.env`

## Desarrollo

### Comandos Útiles

```bash
# Logs
docker-compose logs -f web

# Shell de Django
docker-compose exec web python manage.py shell

# Crear migraciones
docker-compose exec web python manage.py makemigrations

# Tests
docker-compose exec web pytest

# Compilar traducciones
docker-compose exec web python manage.py compilemessages
```

## Contribuir

Este es el sitio oficial de la comunidad de San Cipriano. Para contribuir:

1. Fork el repositorio
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Crear un Pull Request

## Licencia

Propiedad de la Comunidad de San Cipriano, Colombia.

## Contacto

- 📱 WhatsApp: +57 318 838 3917
- 📧 Email: lordmauricio22@gmail.com

---

🌿 **San Cipriano** - Turismo comunitario y conservación ambiental
