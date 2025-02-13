@echo off
echo Instalando uv...
pip install uv

echo Activando entorno virtual...
call .venv\Scripts\activate

echo Instalando dependencias desde requirements.txt...
uv pip install -r requirements.txt

echo ¡Instalación completada!
pause