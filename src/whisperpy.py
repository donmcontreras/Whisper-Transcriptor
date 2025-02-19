import whisper
import torch
import sys
import warnings
import time
from pathlib import Path

warnings.filterwarnings("ignore", category=FutureWarning, module='whisper')  # Si hay actualización de whisper, revisar
warnings.filterwarnings("ignore", message="Performing inference on CPU when CUDA is available")
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

### FUNCION PRINCIPAL DE WHISPER ###
def whisperPythonFunction(file_load, model="medium", device="cpu", output_path="storage/temp/transcripcion_temp.txt", timestmp=True):
    device = get_device(device)
    print(f"Utilizando: {device}")

    model = load_model(model, device)

    start_time = time.time()  # Iniciar el temporizador
    result = transcribe_audio(model, file_load)
    end_time = time.time()  # Detener el temporizador

    elapsed_time = end_time - start_time
    formatted_time = format_time(elapsed_time)
    print(f"Tiempo de transcripción: {formatted_time}\n¡Transcripción completada!")
    
    save_transcription(result, output_path, timestmp)
    return result

### OBTENER DISPOSITIVO ###
def get_device(device):
    valid_devices = ["cpu", "cuda"]
    if device not in valid_devices:
        raise ValueError(f"Dispositivo no válido: {device}. Los dispositivos válidos son: {', '.join(valid_devices)}")
    return torch.device(device if torch.cuda.is_available() else "cpu")

### CARGAR MODELO ###
def load_model(model, device):
    print(f"Cargando modelo: {model}")
    return whisper.load_model(model, device=device, download_root="storage/models")

### INSTRUCCIONES PARA TRANSCRIBIR AUDIO ###
def transcribe_audio(model, file_load):
    print(f"Cargando archivo en {file_load}")
    print("Transcribiendo en Español")
    return model.transcribe(file_load, language="es", verbose=False)

### GUARDAR TRANSCRIPCIÓN ###
def save_transcription(result, output_path, timestmp2):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            text = segment["text"].strip()
            if timestmp2:
                start_time_segment = format_time(segment["start"])
                end_time_segment = format_time(segment["end"])
                f.write(f"[{start_time_segment} - {end_time_segment}] {text} \n")
            else:
                f.write(f"{text} \n")

### FORMATEAR TIEMPO ###
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:06.3f}"

### EJECUCIÓN DE WHISPER ###
if __name__ == "__main__":
    try:
        file_load = sys.argv[1]
        model = sys.argv[2]
        device = sys.argv[3]
        timestmp = sys.argv[4].lower() == 'true'
        output_path = "storage/temp/transcripcion_temp.txt"
        if model == "Pequeño":
            model = "small"
        elif model == "Mediano":
            model = "medium"
        #elif model == "Grande":
        #    model = "large"
        #elif model == "Turbo":
        #    model = "turbo"
        else:
            model = "medium"
        whisperPythonFunction(file_load, model, device, output_path, timestmp)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)