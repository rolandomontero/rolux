@echo off
setlocal enabledelayedexpansion

set /A modelo_seleccionado=-1

:menu_modelo
cls
echo Seleccione el modelo a utilizar:
echo.
echo [0] gemma4:31b-cloud
echo [1] qwen3:0.6b-local
echo [2] minimax-m3:cloud
echo.
set /P entrada=Ingrese el numero del modelo (0, 1 o 2) o presione Enter para salir: 

REM Verificar si la entrada es un número válido (0, 1, o 2)
for %%i in (0 1 2) do (
    if /I "%entrada%"=="%%i" set /A modelo_seleccionado=%%i
)

REM Si no se seleccionó un número válido o se presionó Enter sin valor
if !modelo_seleccionado!==-1 (
    if "%entrada%"=="" (
        echo.
        echo Saliendo...
        timeout /t 2 /nobreak >nul
        exit /b 0
    ) else (
        echo.
        echo Error: Opción inválida. Por favor, ingrese 0, 1 o 2.
        timeout /t 2 /nobreak >nul
        goto menu_modelo
    )
)

REM Asignar el nombre del modelo basado en la selección
set "nombre_modelo="
if !modelo_seleccionado!==0 set "nombre_modelo=gemma4:31b-cloud"
if !modelo_seleccionado!==1 set "nombre_modelo=qwen3:0.6b"
if !modelo_seleccionado!==2 set "nombre_modelo=minimax-m3:cloud"

echo.
color 06
echo Modelo seleccionado: !nombre_modelo!
color 07
REM Activar el entorno virtual y ejecutar Python pasando el argumento --modelo
call "D:\AppServ\www\rolux\utp\Scripts\activate.bat" && (
    start "Python App - Modelo !nombre_modelo!" /B "d:\AppServ\www\rolux\utp\Scripts\python.exe" "d:\AppServ\www\rolux\start.py" modelo=!modelo_seleccionado!
)

if errorlevel 1 (
    echo.
    echo Error: No se pudo activar el entorno virtual o ejecutar Python.
    pause
)

endlocal