import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='pydub.utils')
warnings.filterwarnings("ignore", category=FutureWarning, module='whisper')  # Si hay actualización de whisper, revisar

import whisper
import torch
from pydub import AudioSegment
import sys
import os

### FUNCION PRINCIPAL DE WHISPER ###
def whisperPythonFunction(file_load, model="medium", device="cpu", output_path="storage/temp/transcripcion_temp.txt"):
    device = get_device(device)
    print(f"Utilizando: {device}")

    model = load_model(model, device)

    result = transcribe_audio(model, file_load)
    save_transcription(result, output_path)
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
    return whisper.load_model(model, device=device)

### OBTENER DURACIÓN DE AUDIO ###
def get_audio_duration(file_path):
    audio = AudioSegment.from_file(file_path)
    duration_ms = len(audio)
    duration_s = duration_ms / 1000
    hours = int(duration_s // 3600)
    minutes = int(duration_s % 3600 // 60)
    seconds = duration_s % 60
    formatted_duration = f"{hours:02}:{minutes:02}:{seconds:06.3f}"
    return formatted_duration, duration_s

### INSTRUCCIONES PARA TRANSCRIBIR AUDIO ###
def transcribe_audio(model, file_load):
    print(f"Cargando archivo en {file_load}")
    print("Transcribiendo en Español")
    audio_duration = get_audio_duration(file_load)
    print(f"Duración de audio: {audio_duration}")
    return model.transcribe(file_load, language="es", verbose=False)

### GUARDAR TRANSCRIPCIÓN ###
def save_transcription(result, output_path):
    def format_time(seconds):
        hours = int(seconds // 3600)
        minutes = int(seconds % 3600 // 60)
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:06.3f}"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start_time_segment = format_time(segment["start"])
            end_time_segment = format_time(segment["end"])
            text = segment["text"].strip()
            f.write(f"[{start_time_segment} - {end_time_segment}] {text} \n")

### EJECUCIÓN DE WHISPER ###
if __name__ == "__main__":
    try:
        file_load = sys.argv[1]
        model = sys.argv[2]
        device = sys.argv[3]
        output_path = "storage/temp/transcripcion_temp.txt"
        whisperPythonFunction(file_load, model, device, output_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)