import sys, os
from pydub import AudioSegment
from pywhispercpp.model import Model

### FUNCION PRINCIPAL DE WHISPERCPP ###
def whisperPythonFunction(file_load, model="medium", output_path="storage/temp/transcripcion_temp.txt"):
    print(f"Utilizando: cpu")

    model = load_model(model)

    result = transcribe_audio(model, file_load)
    save_transcription(result, output_path)
    return result

### CARGAR MODELO ###
def load_model(model):
    print(f"Cargando modelo: {model}")
    model = Model(model)
    return model

### OBTENER DURACIÓN DE AUDIO ###
def get_audio_duration(file_path):
    audio = AudioSegment.from_file(file_path)
    duration_ms = len(audio)
    duration_s = duration_ms / 1000
    hours = int(duration_s // 3600)
    minutes = int(duration_s % 3600 // 60)
    seconds = duration_s % 60
    formatted_duration = f"{hours:02}:{minutes:02}:{seconds:06.3f}"
    return formatted_duration

### INSTRUCCIONES PARA TRANSCRIBIR AUDIO ###
def transcribe_audio(model, file_load):
    print(f"Cargando archivo en {file_load}")
    print("Transcribiendo en Español")
    audio_duration = get_audio_duration(file_load)
    print(f"Duración de audio: {audio_duration}")
    result = model.transcribe(file_load, language="es", print_realtime=True)
    return result

### GUARDAR TRANSCRIPCIÓN ###
def save_transcription(result, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for segment in result:
            f.write(segment.text)
            f.write("\n")

### EJECUCIÓN DE WHISPER ###
if __name__ == "__main__":
    try:
        file_load = sys.argv[1]
        model = sys.argv[2]
        output_path = "storage/temp/transcripcion_temp.txt"
        whisperPythonFunction(file_load, model, output_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)