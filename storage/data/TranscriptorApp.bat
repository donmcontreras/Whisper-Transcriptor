@echo off
cd /d "C:\Program Files\Whisper-Transcriptor"
flet main.py
timeout /t 5 && exit