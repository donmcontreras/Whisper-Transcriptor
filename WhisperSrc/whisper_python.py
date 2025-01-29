import whisper
import torch
import time
from pydub import AudioSegment

def whisperPythonFunction(File_Load, progress_callback=None, model="medium"):

    start_time = time.time()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # cuda:1 es la segunda GPU

    print(f"Utilizando: {device}")

    ### CARGAR MODELO ###
    Selected_Model = model
    print(f"Cargando modelo: {Selected_Model}")
    model = whisper.load_model(Selected_Model, device=device)

    ### CARGAR AUDIO ###
    Local_Audio = File_Load
    print(f"Cargando archivo en {Local_Audio}")

    ### OBTENER DURACION DE AUDIO ###
    audioDuration, audioDuration_seconds = get_audio_duration(Local_Audio)
    print(f"Duracion de audio: {audioDuration}")

    ### TRANSCRIBIR AUDIO ###
    result = model.transcribe(Local_Audio)
    result_r = result

    ### DEFINIR LENGUAJE ###
    result = model.transcribe(Local_Audio, language="es")
    if result["language"] == "es":
        lenguaje = "Español"
    result_r=result
    print(f"Transcribiendo en {lenguaje}")

    def format_time(seconds):
        hours = int(seconds // 3600)
        minutes = int(seconds % 3600 // 60)
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:06.3f}"

    ### GUARDAR TRANSCRIPCION ###
    base_name = Local_Audio.split("/")[-1]
    file_name, _ = base_name.split(".")  # Eliminar la extensión del archivo
    output_file_name = f"Transcripcion_{file_name}_{Selected_Model}.txt"
    with open(output_file_name, "w", encoding="utf-8") as f:
        processed_duration = 0
        for segment in result["segments"]:
            start_time_segment = format_time(segment["start"])
            end_time_segment = format_time(segment["end"])
            text = segment["text"].strip()
            f.write(f"[{start_time_segment} - {end_time_segment}] {text} \n")
            processed_duration += segment["end"] - segment["start"]
            if progress_callback:
                progress_callback(processed_duration / audioDuration_seconds)

    end_time = time.time()

    # tiempo
    e_m = (end_time - start_time) % 3600 // 60
    e_s = (end_time - start_time) % 60

    ### IMPRIMIR RESULTADOS ###
    print(f"Ejecutado en {e_m} : {e_s}")
    return result_r

def get_audio_duration(file_path):
    audio = AudioSegment.from_file(file_path)
    duration_ms = len(audio)
    duration_seconds = duration_ms / 1000
    hours = int(duration_seconds // 3600)
    minutes = int(duration_seconds % 3600 // 60)
    seconds = duration_seconds % 60
    formatted_duration = f"{hours:02}:{minutes:02}:{seconds:06.3f}"
    return formatted_duration, duration_seconds