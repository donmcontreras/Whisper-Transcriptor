import flet as ft
from WhisperSrc.whisper_python import whisperPythonFunction  # Asegúrate de que esta función esté definida correctamente

def main(page: ft.Page):

    page.window.width = 800
    page.window.height = 600
    page.window.resizable = False
    page.title = "Whisper"

    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

    def transcribir(e):
        # Obtener el nombre del archivo seleccionado
        print("ejecutando")
        file_name = selected_files.value
        if file_name != "Cancelled!":
            # Llama a la función de transcripción
            transcription = whisperPythonFunction(file_name)  # Asegúrate de que esta función acepte el nombre del archivo
            # Muestra la transcripción en la interfaz
            transcription_output.value = "Archivo transcrito con éxito"
            transcription_output.update()
        else:
            print("No se ha seleccionado ningún archivo.")

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text(color=ft.Colors.BLACK)
    transcription_output = ft.Text()  # Para mostrar la transcripción

    page.overlay.append(pick_files_dialog)

    page.window.width = 500
    page.window.height = 800
    page.window.resizable = True
    page.title = "Whisper"
    page.padding = 0

    # Definir los textos que estarán en los contenedores
    top = ft.Row(
            [
                ft.Text(value="Archivo cargado: ",color=ft.Colors.BLACK),
                selected_files
            ]
        )

    # Botón para elegir archivos
    top_button = ft.ElevatedButton(
                    "Pick files",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=True
                    ),
                )
    
    mid = ft.Text(value="Mid")
    bot = ft.Row(
            [
                ft.ElevatedButton(
                    "Transcribir",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=transcribir  # Llama a la función de transcripción aquí
                ),
                transcription_output,  # Muestra la salida de la transcripción
            ]
        )

    # Crear los contenedores para cada parte
    superior = ft.Container(
        ft.Column([top, top_button]),  # Asegúrate de que top_button esté en el contenedor superior
        width=450, 
        height=100, 
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
