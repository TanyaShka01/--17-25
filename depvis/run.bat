@echo off
rem Запуск утилиты depvis: run.bat [путь_к_конфигу]
setlocal
set "CONFIG=%~1"
if "%CONFIG%"=="" set "CONFIG=config.ini"
set "PYTHONPATH=%PYTHONPATH%;%~dp0src"
python -m depvis.cli --config "%CONFIG%"
endlocal
