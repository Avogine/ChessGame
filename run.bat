@echo off
call venv\Scripts\activate.bat
echo Activated python 3.10 environment.

start "" venv\Scripts\pythonw.exe src\main.pyw
echo Starting game...

echo Closing console...