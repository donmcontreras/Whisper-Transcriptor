@echo off
title Transcriptor App
cd /d "C:\Whisper-Transcriptor"
call .venv\Scripts\activate
flet main.py
timeout /t 1 && exit