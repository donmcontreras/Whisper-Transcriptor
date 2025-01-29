import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='pydub.utils')

import flet as ft
from WhisperSrc.whisper_python import whisperPythonFunction  # Asegúrate de que esta función esté definida correctamente
import time
import asyncio

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

    transcription_done = False  # Variable para saber si la transcripción fue realizada

    


    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

    async def transcribir(e):
        # Obtener el nombre del archivo seleccionado
        nonlocal transcription_result
        file_name = selected_files.value
        selected_model = model_dropdown.value  # Obtener el modelo seleccionado
        try:
            if file_name != "Cancelled!" and file_name is not None:
                # Reset progress bar
                progress_bar.value = 0
                progress_bar.update()

                # Llama a la función de transcripción
                transcription = await asyncio.to_thread(whisperPythonFunction, file_name, update_progress, selected_model)  # Asegúrate de que esta función acepte el nombre del archivo y el callback
                # Muestra la transcripción en la interfaz
                transcription_result = transcription
                transcription_output.value = "Archivo transcrito con éxito."
                try:
                    for segment in transcription["segments"]:
                        start_time_segment = format_time(segment["start"])
                        end_time_segment = format_time(segment["end"])
                        text = segment["text"]
                        lv.controls.append(ft.Text(f"[{start_time_segment} - {end_time_segment}] {text} \n", color=ft.Colors.BLACK))
                        page.update()
                    transcription_done = True  # Actualizamos la variable cuando se termina la transcripción
                    export_button.disabled = False  # Habilitamos el botón Exportar
                    page.update()  # Actualizamos la página para reflejar el cambio
                except:
                    transcription_output.value = "Error: La transcripción no tiene el formato esperado"
                    
            else:
                transcription_output.value = "No se seleccionó un archivo"

        except Exception as e:
            transcription_output.value = f"Error, el archivo seleccionado no es válido: {e}"
        
        page.update()

    def update_progress(value):
        progress_bar.value = value
        progress_bar.update()


    def save_files_result(e: ft.FilePickerResultEvent):
        save_file_rute.value = e.path
        #nonlocal transcription  # Usamos la transcripción obtenida en la función transcribir


        try:
            # Asegurándonos de que transcription esté correctamente disponible
            with open(save_file_rute.value, "w", encoding="utf-8") as f:
                for segment in transcription_result["segments"]:  # Usamos 'transcription' aquí
                    start_time_segment = format_time(segment["start"])
                    end_time_segment = format_time(segment["end"])
                    text = segment["text"].strip()
                    f.write(f"[{start_time_segment} - {end_time_segment}] {text} \n")
                    
            save_file_rute.update()
        except Exception as ex:
            print(f"Error al guardar el archivo: {ex}")

        save_file_rute.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    save_files_dialog = ft.FilePicker(on_result=save_files_result)
    selected_files = ft.Text(color=ft.Colors.BLACK)
    save_file_rute = ft.Text(color=ft.Colors.BLACK)
    transcription_output = ft.Text(color=ft.Colors.BLACK)  # Para mostrar la transcripción
    transcription_result = None  # Para mostrar la transcripción
   
    progress_bar = ft.ProgressBar(width=400, height=20, color=ft.Colors.BLUE)  # Progress bar
    page.overlay.append(pick_files_dialog)
    page.overlay.append(save_files_dialog)
    
    # Configuración de la página
    page.window.width = 500
    page.window.height = 800
    page.window.resizable = False
    page.title = "Whisper"
    page.padding = 0

    # Dropdown para seleccionar el modelo
    model_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("tiny"),
            ft.dropdown.Option("base"),
            ft.dropdown.Option("small"),
            ft.dropdown.Option("medium"),
            ft.dropdown.Option("large"),
            ft.dropdown.Option("turbo"),
        ],
        value="medium",  # Valor por defecto
        label="Seleccionar modelo",
        width=150, # Ancho del dropdown
        height=50, # Alto del dropdown
        color=ft.Colors.BLUE, # Color del dropdown
    )

    # Definir los textos que estarán en los contenedores
    top_r = ft.Column(
        [
            ft.Text(value="Archivo cargado: ", color=ft.Colors.BLACK),
            selected_files,
            ft.ElevatedButton(
                "Cargar archivo",
                icon=ft.Icons.UPLOAD_FILE,
                on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=False,allowed_extensions=['mp4','m4a','mp3','avi','mpeg'])
            ),
            model_dropdown,  # Añadir el dropdown aquí
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    mid = ft.Column([lv])

    export_button = ft.ElevatedButton(
        "Exportar",
        icon=ft.Icons.UPLOAD_FILE,
        disabled=True,  # Inicia como deshabilitado
        on_click=lambda _: save_files_dialog.save_file(allowed_extensions=['txt'])
    )

    bot = ft.Column(
        [
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Transcribir",
                        icon=ft.Icons.UPLOAD_FILE,
                        on_click=lambda e: asyncio.run(transcribir(e))  # Llama a la función de transcripción aquí
                    ),
                    export_button,  # Usamos el botón export_button aquí
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20

            ),
            
            save_file_rute,
            
            progress_bar,
            transcription_output
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )


    #### Contenedores ####

    superior = ft.Container(
        top_r,
        width=450,
        height=200,
        margin=ft.margin.only(top=20),
        border=ft.border.all()
    )
    
    centro = ft.Container(mid, width=450, height=320, margin=ft.margin.only(top=10), border=ft.border.all())
    inferior = ft.Container(bot, width=450, height=150, margin=ft.margin.only(top=10), border=ft.border.all())

    col = ft.Column(
        spacing=10,
        controls=[
            superior,
            centro,
            inferior,
        ]
    )

    contenedor = ft.Container(
        col,
        width=page.window.width,
        height=page.window.height,
        bgcolor=ft.Colors.WHITE,
        alignment=ft.alignment.top_center
    )

    page.add(contenedor)
    page.update()

ft.app(main)