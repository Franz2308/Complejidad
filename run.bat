@echo off
cd /d "%~dp0"/mi_proyecto
echo Iniciando servidor Django...
python manage.py runserver
pause