@echo off
title Catalogo Libri Musica & Gemini NotebookLM
color 0B
echo ========================================================
echo    Catalogo Libri Musica & Gemini NotebookLM Tracker
echo ========================================================
echo.
echo Avvio del server locale in corso...
cd /d "%~dp0"

start "" python server.py
timeout /t 2 /nobreak >nul

echo Apertura dell'interfaccia nel browser...
start http://localhost:5055

echo.
echo ========================================================
echo  L'applicazione e attiva all'indirizzo:
echo  http://localhost:5055
echo.
echo  Premi un tasto per chiudere questa finestra.
echo  (Il server rimarra attivo in background)
echo ========================================================
pause >nul
