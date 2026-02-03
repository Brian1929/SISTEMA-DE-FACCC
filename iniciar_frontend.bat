@echo off
echo ========================================
echo Sistema de Facturacion - Frontend React
echo ========================================
echo.
echo Asegurese de que el backend este corriendo en puerto 5000
echo.
cd frontend
echo Instalando dependencias si es necesario...
call npm install
echo.
echo Iniciando servidor de desarrollo React en puerto 3000...
echo.
call npm run dev
pause

