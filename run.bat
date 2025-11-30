@echo off


cd /d "%~dp0"
if not exist "venv" (
    echo Error: El entorno virtual no existe.
    echo Por favor ejecuta setup.bat primero para configurar el proyecto.
    pause
    exit /b 1
)else (
    echo Entorno virtual encontrado.
    call venv\Scripts\activate.bat
    echo entorno virtual activado
)

if exist "mi_proyecto\manage.py" (
    cd mi_proyecto
    echo Servidor Django iniciando...


    python manage.py runserver
) else (
    echo Error: No se encuentra manage.py
    echo Asegurate de estar en la carpeta correcta
    pause
)
pause