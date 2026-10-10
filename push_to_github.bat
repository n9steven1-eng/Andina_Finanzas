@echo off
title Enviar Proyecto a GitHub - Andina Finanzas
color 0A
echo =========================================================================
echo   ENVIANDO PROYECTO A GITHUB: Andina_Finanzas (n9steven1-eng)
echo =========================================================================
echo.

set "PATH=C:\Program Files\Git\cmd;%PATH%"

echo Repositorio Remoto:
git remote -v
echo.
echo Rama actual:
git branch --show-current
echo.

echo Iniciando envio a GitHub...
echo (Si es la primera vez, se abrira una ventana en tu navegador para autorizar).
echo.
git push -u origin main

echo.
if errorlevel 1 (
    color 0C
    echo =========================================================================
    echo [AVISO] Si no pudiste iniciar sesion en el navegador o fallo la clave:
    echo Puedes generar un Personal Access Token (PAT) en GitHub:
    echo 1. Ve a https://github.com/settings/tokens
    echo 2. Genera un token clasico con permisos de 'repo'
    echo 3. Cuando la consola pida contrasena/token, pegalo aqui.
    echo =========================================================================
) else (
    color 0A
    echo =========================================================================
    echo [EXITO] Proyecto enviado exitosamente a tu repositorio en GitHub!
    echo Enlace: https://github.com/n9steven1-eng/Andina_Finanzas
    echo =========================================================================
)

echo.
pause
