import flet as ft
from WhisperSrc.whisper_python import whisperPythonFunction  # Asegúrate de que esta función esté definida correctamente
import time

def main(page: ft.Page):

    page.window.width = 800
    page.window.height = 600
    page.window.resizable = False
    page.title = "Whisper"

    def format_time(seconds):
        hours = int(seconds // 3600)
        minutes = int(seconds % 3600 // 60)
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:06.3f}"
    


    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

    def transcribir(e):
        # Obtener el nombre del archivo seleccionado
        #print("ejecutando")
      
        file_name = selected_files.value
        try:
            if file_name != "Cancelled!" and file_name != None:
                # Llama a la función de transcripción
                transcription = whisperPythonFunction(file_name)  # Asegúrate de que esta función acepte el nombre del archivo
                # Muestra la transcripción en la interfaz
                transcription_result.value= transcription
                transcription_output.value = "Archivo transcrito con éxito"
                try:
                    for segment in transcription["segments"]:
                        
                        start_time_segment = format_time(segment["start"])
                        end_time_segment = format_time(segment["end"])
                        text = segment["text"]
                        lv.controls.append(ft.Text(f"[{start_time_segment} - {end_time_segment}] {text} \n",color=ft.Colors.BLACK))
                        page.update()
                except:
                    print("error")
                transcription_output.update()
                
            else:
                
                #print("No se ha seleccionado ningún archivo.")
                #Error=True
                transcription_output.value = "No se selecciono un archivo"
                


        except:
            transcription_output.value="Error, el archivo seleccionado no es valido"

        
        page.update()
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text(color=ft.Colors.BLACK)
    transcription_output = ft.Text(color=ft.Colors.BLACK)  # Para mostrar la transcripción
    transcription_result = ft.Text(color=ft.Colors.BLACK)  # Para mostrar la transcripción
    page.overlay.append(pick_files_dialog)

    page.window.width = 500
    page.window.height = 800
    page.window.resizable = True
    page.title = "Whisper"
    page.padding = 0

    # Definir los textos que estarán en los contenedores

    top_r = ft.Column(
        [
            ft.Text(value="Archivo cargado: ",color=ft.Colors.BLACK),
            selected_files,
            ft.ElevatedButton(
                    "Pick files",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=True
                    )),


        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Centra los elementos verticalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centra los elementos horizontalmente
        spacing=20  # Espacio entre los elementos (puedes ajustarlo como desees)
    )

    


    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

  #  count = 1

   
   # for i in range(0, 60):
    #    lv.controls.append(ft.Text(f"Line {count}",color=ft.Colors.BLACK))
     #   count += 1

    #page.add(lv)
    mid = ft.Column([
        
        lv
        #transcription_result



    ],
  
    )



    bot = ft.Column(
        [
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Transcribir",
                        icon=ft.Icons.UPLOAD_FILE,
                        on_click=transcribir  # Llama a la función de transcripción aquí
                    ),
                    ft.ElevatedButton(
                        "Exportar",
                        icon=ft.Icons.UPLOAD_FILE,
                        on_click=transcribir  # Llama a la función de transcripción aquí
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Centra los botones horizontalmente en el Row
                spacing=20  # Espacio entre los botones
            ),

            transcription_output,  # Muestra la salida de la transcripción
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Centra los elementos verticalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centra todo dentro de la columna
        spacing=20  # Espacio entre los elementos
    )
    # Crear los contenedores para cada parte
    superior = ft.Container(
        top_r,  # Asegúrate de que top_button esté en el contenedor superior
        width=450, 
        height=150, 
        margin=ft.margin.only(top=130), 
        border=ft.border.all()
    )
    
    centro = ft.Container(mid, width=450, height=200, margin=ft.margin.only(top=20), border=ft.border.all())
    inferior = ft.Container(bot, width=450, height=100, margin=ft.margin.only(top=20), border=ft.border.all())

    # Usar una lista para asegurar el orden
    col = ft.Column(
        spacing=20,  # Espaciado entre los contenedores
        controls=[
            superior,   # Superior estará arriba
            centro,     # Centro estará en medio
            inferior,   # Inferior estará abajo
        ]
    )

    # Crear el contenedor principal que contiene la columna
    contenedor = ft.Container(
        col, 
        width=page.window.width, 
        height=page.window.height, 
        bgcolor=ft.Colors.WHITE, 
        alignment=ft.alignment.top_center
    )

    # Agregar el contenedor a la página
    page.add(contenedor)
    page.update()

ft.app(main)
