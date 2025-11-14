@echo off
echo ====================================
echo  Setup de RoomFrom
echo ====================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado
    echo Por favor instala Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Python detectado correctamente
echo.

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo [2/4] Creando entorno virtual...
    python -m venv venv
    echo [OK] Entorno virtual creado
) else (
    echo [2/4] Entorno virtual ya existe
)
echo.

REM Activar entorno virtual e instalar dependencias
echo [3/4] Instalando dependencias...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo [OK] Dependencias instaladas
echo.

REM Configurar base de datos
echo [4/4] Configurando base de datos...
cd mi_proyecto
python manage.py makemigrations
python manage.py migrate
cd ..
echo [OK] Base de datos configurada
echo.

echo ====================================
echo  Setup completado exitosamente!
echo ====================================
echo.
echo Para ejecutar el proyecto usa: run.bat
echo.
pause