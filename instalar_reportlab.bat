@echo off
echo ========================================
echo Instalando reportlab para generacion de PDF
echo ========================================
echo.

REM Intentar diferentes formas de instalar
echo Intentando instalar con pip...
python -m pip install reportlab

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Intentando con pip directamente...
    pip install reportlab
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: No se pudo instalar reportlab automaticamente.
    echo.
    echo Por favor instale manualmente:
    echo   1. Abra una terminal como administrador
    echo   2. Ejecute: pip install reportlab
    echo   3. O descargue desde: https://pypi.org/project/reportlab/
    echo.
) else (
    echo.
    echo ✓ reportlab instalado correctamente!
    echo.
)

pause

