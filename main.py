import flet as ft
import torch
import asyncio
import subprocess
from pydub import AudioSegment
from pathlib import Path

def main(page: ft.Page):

    ### SELECCIONAR ARCHIVO ###
    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            selected_files.value = file_path
            audio = AudioSegment.from_file(file_path)
            duration = len(audio) / 1000  # Duración en segundos
            progress_bar.value = 1.0  # Llenar la barra de progreso al 100%
            duration_text.value = f"Duración: {format_time(duration)}"
        else:
            selected_files.value = "Cancelado"
            duration_text.value = ""
        selected_files.update()
        progress_bar.update()
        duration_text.update()

    def transcribeDialog(archivo):
        if archivo is None or archivo == "Cancelado":
            page.open(transcribe_alert)
            return
        else:
            page.open(transcribe_modal)
            return

    ### TRANSCRIBIR ARCHIVO ###
    async def transcribir(e):
        global transcription_canceled
        transcription_canceled = False
        file_name = selected_files.value
        selected_model = model_dropdown.value
        selected_device = (device_dropdown.value).lower()
        selected_time = timestmp.value
        selected_script = "whispercppy.py" if script_dropdown.value == "C++" else "whisperpy.py"
        transcribe_button.disabled = True
        export_button.disabled = True
        cancel_button.disabled = False
        result_con.controls.clear()
        transcription_done.value = ""
        save_file_rute.value = ""
        page.update()
        try:
            whisper_path = Path(f"src/{selected_script}").resolve()
            commandtxt.value = f'python "{whisper_path}" "{file_name}" {selected_model} {selected_device} {selected_time}'
            run_con(commandtxt.value)
        except Exception as e:
            if not transcription_canceled:
                transcription_done.value = f"Error, el archivo seleccionado no es válido: {e}"
                page.update()
            else:
                result_con.controls.append(ft.Text("Transcripción cancelada por el usuario.", color="red"))
                page.update()
        finally:
            transcribe_button.disabled = False
            cancel_button.disabled = True
            page.update()

    ### EJECUTAR COMANDO ###
    def run_con(cmd):
        global process, transcription_canceled
        # Ruta al script de activación del entorno virtual
        venv_activate = Path(".venv/Scripts/activate").resolve()
        if not venv_activate.exists():
            result_con.controls.append(ft.Text("No se encontró el entorno virtual", color="red"))
            page.update()
            return

        # Comando para activar el entorno virtual y ejecutar el comando
        full_cmd = f'cmd.exe /c "{venv_activate} && {cmd}"'

        process = subprocess.Popen(
            full_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8"
        )

        result_con.controls.append(ft.Text(cmd, color=ft.Colors.BLACK if page.theme_mode == ft.ThemeMode.LIGHT else ft.Colors.WHITE, selectable=True))
        page.update()
        result_con.auto_scroll = True

        for line in iter(lambda: process.stdout.readline(), ""):
            result_con.controls.append(ft.Text(line.strip(), color=ft.Colors.BLACK if page.theme_mode == ft.ThemeMode.LIGHT else ft.Colors.WHITE, selectable=True))
            page.update()
            result_con.auto_scroll = True

        process.stdout.close()
        process.wait()
        if process.returncode != 0:
            result_con.controls.append(ft.Text(f"Error al ejecutar el comando: {cmd}", color="red", selectable=True))

        commandtxt.value = ""
        page.update()
        result_con.auto_scroll = True

        try:
            with open("storage/temp/transcripcion_temp.txt", "r", encoding="utf-8", errors="replace") as f:
                transcription_done.value = f.read()
                if not transcription_canceled:
                    export_button.disabled = False
                else:
                    export_button.disabled = True
        except Exception as e:
            transcription_done.value = f"Error al leer el archivo de transcripción: {e}"
        page.update()
        transcribe_button.disabled = False

    ### EXPORTAR TRANSCRIPCIÓN ###
    def export_transcription(e: ft.FilePickerResultEvent):
        if e.path:
            if not e.path.endswith(".txt"):
                e.path += ".txt"
            try:
                with open(e.path, "w", encoding="utf-8") as f:
                    f.write(transcription_done.value)
                save_file_rute.value = f"Transcripción exportada a {e.path}"
            except Exception as e:
                save_file_rute.value = f"Error al exportar la transcripción: {e}"
        else:
            save_file_rute.value = "Exportación cancelada"
        page.update()

    ### CONTROLADOR DE EVENTOS PARA CAMBIO DE SELECCIÓN DEL SCRIPT ###
    def script_changed(e):
        if script_dropdown.value == "C++":
            device_dropdown.options = [ft.dropdown.Option("CPU")]
            device_dropdown.value = "CPU"
            device_dropdown.disabled = True
            timestmp.disabled = False
        else:
            device_dropdown.options = [ft.dropdown.Option("CPU")]
            if torch.cuda.is_available():
                device_dropdown.options.append(ft.dropdown.Option("CUDA"))
                device_dropdown.disabled = False
            device_dropdown.value = "CPU"
            timestmp.disabled = False
        device_dropdown.update()
        timestmp.update()

    ### AGRANDAR TEXTO ###
    def agrandar_texto(e):
        transcription_done.size += 1
        transcription_done.update()

    ### ACHICAR TEXTO ###
    def achicar_texto(e):
        transcription_done.size -= 1
        transcription_done.update()

    ### ALINEAR TEXTO ###
    alignments = [ft.TextAlign.LEFT, ft.TextAlign.CENTER, ft.TextAlign.RIGHT, ft.TextAlign.JUSTIFY]
    current_alignment_index = 0

    def alinear_texto(e):
        nonlocal current_alignment_index
        current_alignment_index = (current_alignment_index + 1) % len(alignments)
        transcription_done.text_align = alignments[current_alignment_index]
        transcription_done.update()

    ### ALTERNAR TEMA ###
    def alternar_tema(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            cambiar_colores(ft.Colors.WHITE, ft.Colors.SURFACE_CONTAINER_HIGHEST, ft.Colors.SURFACE_CONTAINER_HIGHEST)
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            cambiar_colores(ft.Colors.BLACK, ft.Colors.ON_INVERSE_SURFACE, ft.Colors.LIGHT_BLUE_50)
        page.update()

    def cambiar_colores(text_color, bg_color, container_color):
        text_elements = [selected_files, save_file_rute, transcription_done, commandtxt, textoDerecha, select_file_text, model_dropdown, script_dropdown, device_dropdown, duration_text]
        for element in text_elements:
            element.color = text_color
        bg_elements = [select_file, transcribe_button, export_button, agrandar, achicar, alinear, alternar_tema_button, model_dropdown, script_dropdown, device_dropdown, help_button, cancel_button]
        for element in bg_elements:
            element.bgcolor = bg_color
        selectedAudio.bgcolor = container_color
        for control in result_con.controls:
            if isinstance(control, ft.Text):
                control.color = text_color
        page.update()

    ### FORMATEAR TIEMPO ###
    def format_time(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:06.3f}"
    
    ### CANCELAR TRANSCRIPCIÓN ###
    def cancelar_transcripcion():
        global process, transcription_canceled
        transcription_canceled = True
        if process:
            process.terminate()
            process = None
        try:
            transcription_done.value = "Transcripción cancelada por el usuario. Esta acción puede tardar un poco."
        except Exception as e:
            transcription_done.value = f"Error al cancelar la transcripción: {e}"
        page.update()

    ### CONFIGURACIÓN DE LA PÁGINA ###
    page.window.width = 1200
    page.window.height = 800
    page.window.resizable = False
    page.window.maximizable = False
    page.title = "Transcriptor Multimedia"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    ### ELEMENTOS DE LA INTERFAZ ###
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    save_file_dialog = ft.FilePicker(on_result=export_transcription)
    selected_files = ft.Text(color=ft.Colors.BLACK, height=50)
    progress_bar = ft.ProgressBar(width=600, height=10, color=ft.Colors.BLUE)
    duration_text = ft.Text(color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER)
    selectedAudio = ft.Container(
        ft.Column(
            [
                selected_files,
                progress_bar,
                duration_text
            ],
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=5,
        width=700,
        height=100,
        bgcolor=ft.Colors.LIGHT_BLUE_50,
        shadow=ft.BoxShadow(blur_radius=2, offset=(0, 3)),
        margin=ft.margin.only(bottom=10)
    )
    save_file_rute = ft.Text(color=ft.Colors.BLACK)
    transcription_done = ft.Text(color=ft.Colors.BLACK, expand=1, size=15, text_align="left", selectable=True)
    commandtxt = ft.TextField(color="black", cursor_color="black", on_submit=lambda e: run_con(commandtxt.value))
    result_con = ft.ListView(expand=1, spacing=5, padding=5, auto_scroll=True)
    terminal_ct = ft.Column([result_con])
    timestmp = ft.Checkbox(label="Agregar marcas\nde tiempo", value=False, disabled=False)
    help = ft.AlertDialog(
        title=ft.Text("Ayuda"),
        content=ft.Text(
            "- El Script es el lenguaje de computadora que se utilizará para transcribir, puede seleccionar entre C++ y Python, siendo el de C++ más eficiente (recomendado). Si este falla, cambiar al de Python.\n"
            "- El Modelo es el encargado de transcribir el audio, puede seleccionar entre Pequeño y Mediano, siendo el Pequeño más eficiente y el Mediano más eficaz.\n"
            "- El Dispositivo es el hardware que se utilizará para transcribir, puede seleccionar entre CPU (procesador) y CUDA (tarjeta gráfica), siendo la CPU más lenta, debido a que se procesa junto a lo que hace en el computador, y la CUDA más rápida, ya que se procesa en otro entorno especializado (no está disponible en C++, y si no posee tarjeta gráfica).\n"
            "- Agregar marcas de tiempo es la opción de agregar marcas de tiempo a la transcripción, lo que permite saber cuándo se dijo algo en el audio.\n"
            "- El botón de Exportar permite guardar la transcripción en un archivo de texto donde usted indique.\n"
            "- El botón de Cancelar permite detener la transcripción en cualquier momento, eso sí, hay ocasiones en las que puede demorar.",
            width=600,
            size=18,
            text_align=ft.TextAlign.JUSTIFY
        ),
        actions_alignment=ft.MainAxisAlignment.END,
        actions=[ft.TextButton("Cerrar", on_click=lambda e: page.close(help))]
    )

    help_button = ft.ElevatedButton(
        "Ayuda",
        icon=ft.Icons.HELP,
        on_click=lambda e: page.open(help)
    )

    transcribe_alert = ft.AlertDialog(
        title=ft.Text("Error"),
        content=ft.Text("No ha seleccionado un archivo."),
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    model_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("Pequeño"),
            ft.dropdown.Option("Mediano"),
            #ft.dropdown.Option("Grande"),
            #ft.dropdown.Option("Turbo"),
        ],
        value="Pequeño",
        label="Seleccionar modelo",
        width=100,
        height=50,
        color=ft.Colors.BLACK,
    )

    script_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("C++"),
            ft.dropdown.Option("Python"),
        ],
        value="C++",
        label="Seleccionar script",
        width=100,
        height=50,
        color=ft.Colors.BLACK,
        on_change=script_changed  # Asignar el controlador de eventos aquí
    )

    CUDA_available = torch.cuda.is_available()
    device_options = [ft.dropdown.Option("CPU")]
    device_disabled = True
    if CUDA_available:
        device_options.append(ft.dropdown.Option("CUDA"))
        device_disabled = False

    device_dropdown = ft.Dropdown(
        options=device_options,
        value="CPU",
        label="Seleccionar dispositivo",
        width=100,
        height=50,
        color=ft.Colors.BLACK,
        disabled=True if script_dropdown.value == "C++" else device_disabled
    )

    export_button = ft.ElevatedButton(
        "Exportar",
        icon=ft.Icons.DOWNLOAD,
        disabled=True,
        on_click=lambda e: save_file_dialog.save_file(allowed_extensions=['txt']),
        width=130,
        height=40
    )

    transcribe_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar"),
        content=ft.Text("¿Está seguro de transcribir el audio?"),
        actions=[
            ft.TextButton("Sí", on_click=lambda e: (page.close(transcribe_modal), asyncio.run(transcribir(e)))),
            ft.TextButton("No", on_click=lambda e: page.close(transcribe_modal)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    transcribe_button = ft.ElevatedButton(
        "Transcribir",
        icon=ft.Icons.PLAY_ARROW,
        on_click=lambda e: transcribeDialog(selected_files.value),
        width=110
    )

    cancel_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cancelar"),
        content=ft.Text("¿Está seguro de cancelar la transcripción?"),
        actions=[
            ft.TextButton("Sí", on_click=lambda e: (page.close(cancel_modal), cancelar_transcripcion())),
            ft.TextButton("No", on_click=lambda e: page.close(cancel_modal)),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    cancel_button = ft.ElevatedButton(
        "Cancelar",
        icon=ft.Icons.CANCEL,
        on_click=lambda e: page.open(cancel_modal),
        disabled=True,
        width=110
    )

    agrandar = ft.ElevatedButton(
        "Incrementar\ntamaño",
        icon=ft.Icons.ZOOM_IN,
        on_click=agrandar_texto,
        width=130,
        height=40
    )

    achicar = ft.ElevatedButton(
        "Disminuir\ntamaño",
        icon=ft.Icons.ZOOM_OUT,
        on_click=achicar_texto,
        width=130,
        height=40
    )

    alinear = ft.ElevatedButton(
        "Cambiar\nalineación",
        icon=ft.Icons.FORMAT_ALIGN_LEFT,
        on_click=alinear_texto,
        width=130,
        height=40
    )

    alternar_tema_button = ft.ElevatedButton(
        "Alternar\ntema",
        icon=ft.Icons.BRIGHTNESS_6,
        on_click=alternar_tema
    )

    select_file_text = ft.Text("Seleccione archivo: ", size=20, color=ft.Colors.BLACK, style=ft.TextStyle(weight=ft.FontWeight.BOLD))
    select_file = ft.ElevatedButton("Seleccionar archivo", icon=ft.Icons.UPLOAD_FILE, on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=False, allowed_extensions=['mp4', 'm4a', 'mp3', 'mpeg', 'mpga', 'wav', 'webm']))

    ### DISEÑO DE LA INTERFAZ ###
    top_r = ft.Column(
        [
            ft.Row(
                [
                    alternar_tema_button,
                    help_button,
                    select_file_text,
                    select_file
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            selectedAudio,
            ft.Row(
                [
                    script_dropdown,
                    model_dropdown,
                    device_dropdown,
                    timestmp,
                    ft.Column([transcribe_button, cancel_button], alignment=ft.MainAxisAlignment.CENTER)
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    textTools = ft.Column([agrandar, achicar, alinear, export_button], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=25)
    lv = ft.ListView(expand=1, spacing=5, padding=10, auto_scroll=False, controls=[transcription_done])
    textScroll = ft.Container(lv, width=800, height=280, margin=ft.margin.only(top=2), border=ft.border.all())
    command = ft.Container(terminal_ct, width=750, height=80, margin=ft.margin.only(top=10), border=ft.border.all())

    bot = ft.Column(
        [
            ft.Row([textTools, textScroll], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            save_file_rute
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5
    )

    textoDerecha = ft.Text(
        "Esta es una ",
        size=15,
        color=ft.Colors.BLACK,
        text_align=ft.TextAlign.JUSTIFY,
        spans=[
            ft.TextSpan("herramienta", ft.TextStyle(weight=ft.FontWeight.BOLD)),
            ft.TextSpan(" para la transcripción de audios que, en general, tiene una precisión del 88%, por lo que tiene margen de error y"),
            ft.TextSpan(" se recomienda verificar y corregir los textos entregados", ft.TextStyle(weight=ft.FontWeight.BOLD)),
            ft.TextSpan(" (puede exportar el resultado y corregir dentro del ''.txt'' que hizo)."),
            ft.TextSpan(" Dependiendo del modelo seleccionado, y de los recursos del computador, el tiempo de transcripción puede variar, estando cerca de la misma duración del audio.\n"),
            ft.TextSpan("\nErrores comunes:"),
            ft.TextSpan("\n1. ", ft.TextStyle(weight=ft.FontWeight.BOLD)),
            ft.TextSpan("En ciertos casos los números no se detectan bien y entorpecen la transcripción."),
            ft.TextSpan("\n2. ", ft.TextStyle(weight=ft.FontWeight.BOLD)),
            ft.TextSpan("Los nombres y los apellidos no se transcriben correctamente."),
            ft.TextSpan("\n3. ", ft.TextStyle(weight=ft.FontWeight.BOLD)),
            ft.TextSpan("Los acrónimos (como RUT) no se transcriben correctamente."),
        ],
    )

    ### CONTENEDOR SUPERIOR ###
    superior = ft.Container(top_r, width=750, height=280, margin=ft.margin.only(top=10), border=ft.border.all())

    ### CONTENEDOR MEDIO ###
    midterm = ft.Column(spacing=10, controls=[command])

    ### CONTENEDOR INFERIOR ###
    inferior = ft.Container(bot, width=1000, height=330, margin=ft.margin.only(top=10), border=ft.border.all())

    ### COLUMNA IZQUIERDA ###
    colIzq = ft.Column(spacing=10, controls=[superior, midterm])

    ### CONTENEDOR DERECHA ###
    derecha = ft.Container(textoDerecha, width=380, height=380, margin=ft.margin.only(left=10), border=ft.border.all(), padding=10)

    ### COLUMNA DERECHA ###
    colDer = ft.Column(spacing=10, controls=[derecha], alignment=ft.MainAxisAlignment.CENTER)

    ### CONTENEDOR COLUMNAS ###
    contCol = ft.Row([colIzq, colDer], alignment=ft.MainAxisAlignment.CENTER)

    ### CONTENEDOR GENERAL ###
    contenedor = ft.Container(contCol, width=page.window.width, height=400, alignment=ft.alignment.top_center)
    columnaAbajo = ft.Column(spacing=10, controls=[inferior])
    contenedorAbajo = ft.Container(columnaAbajo, width=page.window.width, height=page.window.height, alignment=ft.alignment.top_center)

    page.overlay.extend([pick_files_dialog, save_file_dialog])
    page.add(contenedor, contenedorAbajo)
    page.update()

ft.app(main)