# **Aplicación de transcripción multimedia**

Equipo de trabajo:

Miguel Contreras; Diego Molina.

---
# **Documentación**
## **Manual técnico**

Éste es el manual de usuario técnico para `Aplicación de transcripción multimedia`.

# **Índice**

1. [Requisitos previos](#1-requisitos-previos)
    1. [Python 1.12.6](#11-python-1126)
    2. [Chocolatey](#12-chocolatey)
    3. [FFmpeg](#13-ffmpeg)
    4. [git (opcional)](#14-git-si-deseas-instalar-usando-git)
    5. [C++ Build Tools](#15-c-build-tools)
2. [Instrucciones](#2-instrucciones)
    1. [Clonar](#21-clonar)
    2. [Instalación local](#22-instalación-local)
        1. [Instalación con uso de git](#221-instalación-con-uso-de-git)
        2. [Instalación sin uso de git](#222-instalación-sin-uso-de-git)
    3. [Ejecución](#23-ejecución)

## **1. Requisitos previos**
Para empezar a proceder con las instrucciones de instalación, primero requiere tener (verificar en orden):

### **1.1. `Python 1.12.6`**
Se puede descargar [aquí](https://www.python.org/downloads/release/python-3126/). Se decargará el instalador y, al abrirlo, habrá que marcar la casilla de privilegios de administrador y la de agregar al "PATH", posteriormente elegir instalación personalizada, indicar que la instalación será para todos los usuarios e instalar.

### **1.2. `Chocolatey`**
Para instalar necesita abrir una línea de comandos en `PowerShell` en modo de **administrador** e ingresar lo siguiente:
```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### **1.3. `FFmpeg`**
Requiere de **Chocolatey**, y que, para instalarse, se necesita **reiniciar** el `PowerShell` (a veces con el PowerShell se requiere reiniciar el computador, ya que aún no reconoce Chocolatey, en ese caso mejor inicia el CMD (Símbolo del sistema)) e ingresar lo siguiente:
```
choco install ffmpeg -y
```

### **1.4. `git`** _(si deseas instalar usando git)_
Se puede descargar [aquí](https://git-scm.com/downloads/win). Se descargará el instalador y, al abrirlo, habrá que avanzar hasta llegar a la selección de componentes, en donde habrá que desmarcar la casilla de integración al explorador de Windows, y en la siguiente pestaña desmarcar el crear una carpeta en el menú de inicio, de ahí avanzar hasta instalar.

### **1.5. `C++ Build Tools`**
Se puede descargar [aquí](https://visualstudio.microsoft.com/visual-cpp-build-tools/). Se descargará `Visual Studio Installer`, y habrá que seleccionar, en "Cargas de trabajo", **"Desarrollo para el escritorio con C++"** y, en "Componentes individuales", seleccionar el `SDK` según el Windows que estes utilizando _(Windows 10 SDK (Última versión disponible) o Windows 11 SDK (Última versión disponible))_, y de ahí instalar.

## **2. Instrucciones**
Ésto es una guía de usuario para poder ejecutar el programa, el cuál se recomienda seguir paso por paso para minimizar los problemas que se puedan generar durante la ejecución.

### **2.1. Clonar**

Primero hay que descargar el repositorio desde la pestaña `<> Code` (de color verde) y seleccionar el `Download ZIP`. Al finalizar la descarga hay que descomprimir el contenido en una carpeta que se llame `Whisper-Transcriptor` y moverlo a la raíz del disco `C:` (esto para evitar problemas de ruta) en la siguiente ruta:
```
C:
```

### **2.2. Instalación local**
Aquí depende de si instalaste `git`, o por si alguna razón el internet no te deja conectarte a `GitHub` (como cuando el Proxy no permite esta conexión).

#### **2.2.1 Instalación con uso de git**

Ya entrando a la carpeta creada al haber descomprimido el `ZIP`, y moverlo a `C:`, tendremos que hacer doble click, o abrir, al archivo `install.bat`, el cuál abrira un `CMD` donde instalará todas las dependencias necesarias para funcionar. Para asegurarse de que estés en la ubicación necesaria, debes fijarte de que la dirección sea:
```
C:\Whisper-Transcriptor
```

#### **2.2.2 Instalación sin uso de git**

Ya entrando a la carpeta creada al haber descomprimido el `ZIP`, y moverlo a `C:`, tendremos que descomprimir nuevamente otro archivo llamado `InstallWOgit.zip` en la misma carpeta reemplazando todo, o en el caso de que se cree otra carpeta, mover su contenido a la raíz del proyecto y reemplazar todo: 
```
C:\Whisper-Transcriptor
```
Luego hacer doble click, o abrir, al archivo `installwogit.bat`, el cuál abrira un `CMD` donde instalará todas las dependencias necesarias para funcionar.

### **2.3 Ejecución**

Para ejecutar este programa debe hacer doble click, o abrir, el archivo `TranscriptorApp.exe`.

¡Puede ser desde cualquier sitio!, por lo que puede mover este ejecutable a donde sea (por ejemplo, el escritorio).

¡Felicidades, ejecutaste el programa!

<pre>Seleccione su archivo, indique como desea que se procese, y ¡a transcribir!</pre>
