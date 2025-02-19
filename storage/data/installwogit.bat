@echo off
echo Instalando uv...
pip install uv

echo Activando entorno virtual...
call .venv\Scripts\activate

echo Instalando dependencias desde requirements.txt...
uv pip install -r requirements.txt

echo Instalando dependencias de Flet...
uv pip install flet[all]==0.26.0 --upgrade

echo Instalando torch...
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

echo ¡Instalación completada!
pause