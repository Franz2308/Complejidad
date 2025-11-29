@echo off
venv\Scripts\activate
echo entorno virtual activado
pause
cd /d "%~dp0"
if exist "mi_proyecto\manage.py" (
    cd mi_proyecto
    echo ✓ Servidor Django iniciando...
    venv\Scripts\activate
    python manage.py runserver
) else (
    echo ✗ Error: No se encuentra manage.py
    echo Asegurate de estar en la carpeta correcta
    pause
)
pause