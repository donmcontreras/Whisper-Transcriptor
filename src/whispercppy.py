import sys
import time
from pathlib import Path
from pywhispercpp.model import Model
from tqdm import tqdm

### FUNCION PRINCIPAL DE WHISPERCPP ###
def whisperPythonFunction(file_load, model="medium", output_path="storage/temp/transcripcion_temp.txt", timestmp=True):
    print("Utilizando: cpu")

    model = load_model(model)

    start_time = time.time()  # Iniciar el temporizador
    result = transcribe_audio(model, file_load)
    end_time = time.time()  # Detener el temporizador

    save_transcription(result, output_path, timestmp)

    elapsed_time = end_time - start_time
    formatted_time = format_time(elapsed_time)
    print(f"Tiempo de transcripción: {formatted_time}\n¡Transcripción completada!")

    return result

### CARGAR MODELO ###
def load_model(model):
    print(f"Cargando modelo: {model}")
    model = Model(model)
    return model

### INSTRUCCIONES PARA TRANSCRIBIR AUDIO ###
def transcribe_audio(model, file_load):
    print(f"Cargando archivo en {file_load}")
    print("Transcribiendo en Español")

    # Create a progress bar
    with tqdm(total=100, desc="Transcribiendo", unit="frames", ncols=85) as pbar:
        def progress_callback(progress):
            pbar.update(progress - pbar.n)
            pbar.refresh()  # Ensure the progress bar is updated in real time
        
        result = model.transcribe(file_load, language="es", progress_callback=progress_callback)
    
    return result

### GUARDAR TRANSCRIPCIÓN ###
def save_transcription(result, output_path, timestmp):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for segment in result:
            if timestmp:
                start_time = format_time(segment.t0 / 100)  # Convertir milisegundos a segundos
                end_time = format_time(segment.t1 / 100)    # Convertir milisegundos a segundos
                f.write(f"[{start_time} - {end_time}] {segment.text}\n")
            else:
                f.write(segment.text)
                f.write("\n")

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
        timestmp = sys.argv[4].lower() == 'true'
        if model == "Pequeño":
            model = "small"
        elif model == "Mediano":
            model = "medium"
        #elif model == "Grande":
        #    model = "large-v3"
        #elif model == "Turbo":
        #    model = "large-v3-turbo"
        else:
            model = "medium"
        output_path = "storage/temp/transcripcion_temp.txt"
        whisperPythonFunction(file_load, model, output_path, timestmp)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)