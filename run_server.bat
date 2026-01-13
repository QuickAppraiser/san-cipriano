@echo off
echo ========================================
echo   San Cipriano - Iniciando Servidor
echo ========================================
echo.

if not exist "venv" (
    echo ERROR: No se encontro el entorno virtual.
    echo Ejecuta primero: setup_local.bat
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo Servidor iniciando...
echo.
echo Abre en tu navegador:
echo   http://localhost:8000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python manage.py runserver
