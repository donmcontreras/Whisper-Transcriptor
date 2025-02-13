@echo off
echo Instalando uv...
pip install uv

echo Creando entorno virtual...
uv venv

echo Activando entorno virtual...
call .venv\Scripts\activate

echo Instalando dependencias desde requirements.txt...
uv pip install -r requirements.txt

echo Instalando pywhispercpp...
uv pip install git+https://github.com/absadiki/pywhispercpp

echo ¡Instalación completada!
pause