import whisper
import torch
import time
from pydub import AudioSegment

def whisperPythonFunction(File_Load, model="medium", device="cpu"):
    start_time = time.time()

    device = torch.device(device if torch.cuda.is_available() else "cpu")  # cuda:1 es la segunda GPU
    print(f"Utilizando: {device}")

    ### CARGAR MODELO ###
    Selected_Model = model
    print(f"Cargando modelo: {Selected_Model}")
    model = whisper.load_model(Selected_Model, device=device)

    ### CARGAR AUDIO ###
    Local_Audio = File_Load
    print(f"Cargando archivo en {Local_Audio}")

    ### OBTENER DURACION DE AUDIO ###
    audioDuration = getAudioDuration(Local_Audio)
    print(f"Duracion de audio: {audioDuration}")

    ### TRANSCRIBIR AUDIO ###
    lenguaje = "es"
    if lenguaje == "es":
        idioma = "Español"
    print(f"Transcribiendo en {idioma}")
    result = model.transcribe(Local_Audio, language=lenguaje, verbose=False)

    def format_time(seconds):
        hours = int(seconds // 3600)
        minutes = int(seconds % 3600 // 60)
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:06.3f}"

    ### GUARDAR TRANSCRIPCION ###
    with open("transcripcion_temp.txt", "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start_time_segment = format_time(segment["start"])
            end_time_segment = format_time(segment["end"])
            text = segment["text"].strip()
            f.write(f"[{start_time_segment} - {end_time_segment}] {text} \n")
         #   List.append(f"[{start_time_segment} - {end_time_segment}] {text} \n")
    end_time = time.time()

    #tiempo
    #e_h = (end_time - start_time) //3600
    e_m = (end_time - start_time) % 3600 // 60
    e_s = (end_time - start_time) % 60

    ### IMPRIMIR RESULTADOS ###
    print(f"Ejecutado en {e_m} : {e_s}")
    return result

def getAudioDuration(file_path):
    audio = AudioSegment.from_file(file_path)
    duration_ms = len(audio)
    duration_s = duration_ms / 1000
    hours = int(duration_s // 3600)
    minutes = int(duration_s % 3600 // 60)
    seconds = duration_s % 60
    formatted_duration = f"{hours:02}:{minutes:02}:{seconds:06.3f}"
    return formatted_duration, duration_s