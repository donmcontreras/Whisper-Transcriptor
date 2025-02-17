@echo off
echo Instalando uv...
pip install uv

echo Activando entorno virtual...
call .venv\Scripts\activate

echo Instalando dependencias desde requirements.txt...
uv pip install -r requirements.txt

echo Instalando dependencias de Flet...
uv pip install flet[all]==0.26.0 --upgrade

echo ¡Instalación completada!
pause