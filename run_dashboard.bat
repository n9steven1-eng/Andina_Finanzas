@echo off
title Dashboard Financiero - Distribuciones Andina Comercial S.A.S.
echo =========================================================================
echo   INICIANDO DASHBOARD FINANCIERO EJECUTIVO - ANDINA COMERCIAL S.A.S.
echo =========================================================================
echo.

set "PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python311"
set "PATH=%PYTHON_PATH%;%PYTHON_PATH%\Scripts;%PATH%"

echo Verificando Python...
python --version
if errorlevel 1 (
    echo [ERROR] No se pudo encontrar Python en %PYTHON_PATH%.
    pause
    exit /b 1
)

echo.
echo Iniciando servidor Streamlit en puerto 8501...
echo Abriendo aplicacion en el navegador web...
echo.
streamlit run app.py --server.port 8501 --server.headless false

pause
