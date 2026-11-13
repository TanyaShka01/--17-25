@echo off
chcp 65001 >nul
rem Запуск утилиты depvis: run.bat [путь_к_конфигу]
setlocal
set "CONFIG=%~1"
if "%CONFIG%"=="" set "CONFIG=config.ini"
set "PYTHONPATH=%~dp0src"
python "%~dp0src\depvis\cli.py" --config "%CONFIG%"
endlocal
