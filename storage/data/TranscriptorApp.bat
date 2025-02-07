@echo off
cd /d "C:\Whisper-Transcriptor"
call .venv\Scripts\activate
flet main.py
timeout /t 5 && exit