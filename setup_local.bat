@echo off
echo ========================================
echo   San Cipriano - Setup Local
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo.
    echo Por favor:
    echo 1. Descarga Python desde https://python.org/downloads
    echo 2. Durante la instalacion, MARCA "Add Python to PATH"
    echo 3. Reinicia la terminal y ejecuta este script de nuevo
    echo.
    pause
    exit /b 1
)

echo [1/6] Creando entorno virtual...
if not exist "venv" (
    python -m venv venv
)

echo [2/6] Activando entorno virtual...
call venv\Scripts\activate.bat

echo [3/6] Instalando dependencias...
pip install -r requirements\local.txt

echo [4/6] Aplicando migraciones...
python manage.py migrate

echo [5/6] Creando datos iniciales (biodiversidad, FAQs, experiencias)...
python manage.py setup_initial_data

echo [6/6] Creando superusuario...
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@sancipriano.co', 'admin123') | python manage.py shell

echo.
echo ========================================
echo   Setup completado exitosamente!
echo ========================================
echo.
echo Para iniciar el servidor ejecuta:
echo   run_server.bat
echo.
echo O manualmente:
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Accede a:
echo   Sitio: http://localhost:8000
echo   Admin: http://localhost:8000/admin
echo   Usuario: admin
echo   Password: admin123
echo.
pause
