@echo off
echo Creando entorno virtual...
python -m venv .venv

echo Activando entorno virtual...
call .venv\Scripts\activate

echo Instalando dependencias desde requirements.txt...
pip install -r requirements.txt

echo Instalando PyTorch con soporte de CUDA...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

echo Instalando pywhispercpp...
pip install git+https://github.com/absadiki/pywhispercpp

echo ¡Instalación completada!
pause