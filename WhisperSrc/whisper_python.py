import whisper
import torch
import time



def whisperPythonFunction(File_Load):
    start_time = time.time()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")  # cuda:1 es la segunda GPU
    print(f"Utilizando: {device}")

    Selected_Model = "tiny"
    print(f"Cargando modelo: {Selected_Model}")
    model = whisper.load_model(Selected_Model, device=device)

    Local_Audio = File_Load
    print(f"Cargando archivo en {Local_Audio}")

    result = model.transcribe(Local_Audio)

    
    #result_r=result
    def format_time(seconds):
        hours = int(seconds // 3600)
        minutes = int(seconds % 3600 // 60)
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:06.3f}"


    with open("transcripcion_textos.txt","w",encoding="utf-8") as f:
        #List=[]

        for segment in result["segments"]:

            start_time_segment = format_time(segment["start"])
            end_time_segment = format_time(segment["end"])
            text = segment["text"].strip()

            #
            f.write(f"[{start_time_segment} - {end_time_segment}] {text} \n")
         #   List.append(f"[{start_time_segment} - {end_time_segment}] {text} \n")
    end_time = time.time()
            

    #tiempo

    #e_h = (end_time - start_time) //3600
    e_m = (end_time - start_time) % 3600 // 60
    e_s = (end_time - start_time) % 60


    print(f"Ejecutado en {e_m} : {e_s}")
    return result



#whisperPythonFunction("torerom4a.m4a")