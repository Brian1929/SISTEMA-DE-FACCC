@echo off
title Sistema de Facturacion - SERVIDOR
color 0A
echo ===================================================
echo     INICIANDO SISTEMA DE FACTURACION PRO
echo ===================================================
echo.
echo [1/2] Verificando entorno...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python no encontrado. Instala Python y agregalo al PATH.
    pause
    exit
)
echo Python OK.

echo.
echo [2/2] Arrancando el servidor...
echo.
echo ---------------------------------------------------
echo  TU SISTEMA ESTA ACTIVO EN:
echo  - PC LOCAL: http://localhost:5000
echo  - CELULAR/TABLET: http://192.168.0.186:5000
echo ---------------------------------------------------
echo.
echo NO CIERRES ESTA VENTANA NEGRA mientras uses el sistema.
echo.

python api.py
pause
