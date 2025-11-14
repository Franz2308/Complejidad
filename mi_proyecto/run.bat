@echo off
cd /d "%~dp0"
echo Iniciando servidor Django...
python manage.py runserver
pause