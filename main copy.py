import flet as ft
import torch, asyncio, subprocess, os

def main(page: ft.Page):

    ### SELECCIONAR ARCHIVO ###
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "Cancelado"
        )
        selected_files.update()

    ### TRANSCRIBIR ARCHIVO ###
    async def transcribir(e):
        file_name = selected_files.value
        selected_model = model_dropdown.value
        selected_device = (device_dropdown.value).lower()
        selected_time = timestmp.value
        if script_dropdown.value == "C++":
            selected_script = "whispercppy.py"
        else:
            selected_script = "whisperpy.py"
        transcribe_button.disabled = True
        result_con.controls.clear()
        transcription_done.value = ""
        save_file_rute.value = ""
        page.update()
        try:
            if file_name != "Cancelado" and file_name is not None:
                whisper_path = os.path.abspath(f"src/{selected_script}")
                commandtxt.value = f'python "{whisper_path}" "{file_name}" {selected_model} {selected_device} {selected_time}'
                run_con(commandtxt.value)
            else:
                transcription_done.value = "No se seleccionó un archivo"
                page.update()
        except Exception as e:
            transcription_done.value = f"Error, el archivo seleccionado no es válido: {e}"
            page.update()
        finally:
            transcribe_button.disabled = False
            page.update()

    ### EJECUTAR COMANDO ###
    def run_con(cmd):
        # Ruta al script de activación del entorno virtual
        venv_activate = os.path.abspath(".venv/Scripts/activate")  # Ajusta la ruta según sea necesario
        if not os.path.exists(venv_activate):
            result_con.controls.append(ft.Text("No se encontró el entorno virtual", color="red"))
            page.update()

        # Comando para activar el entorno virtual y ejecutar el comando
        full_cmd = f'cmd.exe /c "{venv_activate} && {cmd}"'

        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8"
        )

        result_con.controls.append(ft.Text(cmd, color="black"))
        page.update()
        result_con.auto_scroll = True

        for line in process.stdout:
            result_con.controls.append(ft.Text(line, color="black"))
            page.update()
            result_con.auto_scroll = True

        process.stdout.close()
        process.wait()
        commandtxt.value = ""
        page.update()
        result_con.auto_scroll = True

        try:
            with open("storage/temp/transcripcion_temp.txt", "r", encoding="utf-8") as f:
                transcription_done.value = f.read()
                export_button.disabled = False
        except UnicodeDecodeError:
            try:
                with open("storage/temp/transcripcion_temp.txt", "r", encoding="utf-8", errors="ignore") as f:
                    transcription_done.value = f.read()
                    export_button.disabled = False
            except Exception as e:
                transcription_done.value = f"Error al leer el archivo de transcripción: {e}"
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
            timestmp.value = False
            timestmp.disabled = True
        else:
            device_dropdown.options = [ft.dropdown.Option("CPU")]
            if torch.cuda.is_available():
                device_dropdown.options.append(ft.dropdown.Option("CUDA"))
                device_dropdown.disabled = False
            device_dropdown.value = "CPU"
            timestmp.disabled = False
        device_dropdown.update()
        timestmp.update()

    ### CONFIGURACIÓN DE LA PÁGINA ###
    page.window.width = 1200
    page.window.height = 800
    page.window.resizable = False
    page.window.maximizable = False
    page.title = "Transcriptor Multimedia"
    page.padding = 0

    ### ELEMENTOS DE LA INTERFAZ ###
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    save_file_dialog = ft.FilePicker(on_result=export_transcription)
    selected_files = ft.Text(color=ft.Colors.BLACK)
    save_file_rute = ft.Text(color=ft.Colors.BLACK)
    transcription_done = ft.Text(color=ft.Colors.BLACK, expand=1)
    commandtxt = ft.TextField(color="black", cursor_color="black", on_submit=lambda e: run_con(commandtxt.value))
    result_con = ft.ListView(expand=1, spacing=5, padding=5, auto_scroll=True)
    terminal_ct = ft.Column([result_con])
    timestmp = ft.Checkbox(label="Agregar marcas\nde tiempo", value=False)

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
        color=ft.Colors.BLUE,
    )

    script_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("Python"),
            ft.dropdown.Option("C++")
        ],
        value="Python",
        label="Seleccionar script",
        width=100,
        height=50,
        color=ft.Colors.BLUE,
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
        color=ft.Colors.BLUE,
        disabled=device_disabled
    )

    export_button = ft.ElevatedButton(
        "Exportar",
        icon=ft.Icons.DOWNLOAD,
        disabled=True,
        on_click=lambda e: save_file_dialog.save_file(allowed_extensions=['txt'])
    )

    transcribe_button = ft.ElevatedButton(
        "Transcribir",
        icon=ft.Icons.PLAY_ARROW,
        on_click=lambda e: asyncio.run(transcribir(e))
    )

    ### DISEÑO DE LA INTERFAZ ###
    top_r = ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Seleccione archivo: ", size=20, color=ft.Colors.BLACK),
                    ft.ElevatedButton("Seleccionar archivo", icon=ft.Icons.UPLOAD_FILE, on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=False, allowed_extensions=['mp4', 'm4a', 'mp3', 'mpeg', 'mpga', 'wav', 'webm']))
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            selected_files,
            ft.Row(
                [
                    script_dropdown,
                    model_dropdown,
                    device_dropdown,
                    transcribe_button,
                    timestmp
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    lv = ft.ListView(expand=1, spacing=5, padding=10, auto_scroll=False, controls=[transcription_done])
    textscroll = ft.Container(lv, width=750, height=260)
    command = ft.Container(terminal_ct, width=750, height=100, margin=ft.margin.only(top=10), border=ft.border.all())

    bot = ft.Column(
        [
            ft.Row([textscroll], alignment=ft.MainAxisAlignment.CENTER),
            export_button,
            save_file_rute
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )

    textoDerecha = ft.Text(
        "Esta es una ",
        size=15,
        color=ft.Colors.BLACK,
        text_align=ft.TextAlign.JUSTIFY,
        spans=[
            ft.TextSpan("herramienta", ft.TextStyle(weight=ft.FontWeight.BOLD)),
            ft.TextSpan(" para la transcripción de audios que, en general, tiene una precisión del 88%, por lo que tiene margen de error y se "),
            ft.TextSpan("recomienda verificar y corregir los textos entregados", ft.TextStyle(weight=ft.FontWeight.BOLD)),
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
    superior = ft.Container(top_r, width=750, height=200, margin=ft.margin.only(top=20), border=ft.border.all())

    ### CONTENEDOR MEDIO ###
    midterm = ft.Column(spacing=10, controls=[command])

    ### CONTENEDOR INFERIOR ###
    inferior = ft.Container(bot, width=750, height=380, margin=ft.margin.only(top=10), border=ft.border.all())

    ### COLUMNA IZQUIERDA ###
    colIzq = ft.Column(spacing=10, controls=[superior, midterm, inferior])

    ### CONTENEDOR DERECHA ###
    derecha = ft.Container(textoDerecha, width=380, height=650, margin=ft.margin.only(left=10), border=ft.border.all(), padding=10)

    ### COLUMNA DERECHA ###
    colDer = ft.Column(spacing=10, controls=[derecha], alignment=ft.MainAxisAlignment.CENTER)

    ### CONTENEDOR COLUMNAS ###
    contCol = ft.Row([colIzq, colDer], alignment=ft.MainAxisAlignment.CENTER)

    ### CONTENEDOR GENERAL ###
    contenedor = ft.Container(contCol, width=page.window.width, height=page.window.height, bgcolor=ft.Colors.WHITE, alignment=ft.alignment.top_center)

    page.overlay.extend([pick_files_dialog, save_file_dialog])
    page.add(contenedor)
    page.update()

ft.app(main)