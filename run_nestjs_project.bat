@echo off

set "PROJECT_NAME=%~1"
echo Nombre del proyecto: %PROJECT_NAME%

REM --- Definir directorio de destino ---
set "TARGET_DIR=.\nestjs"
echo Directorio de destino: %TARGET_DIR%

REM --- Cambiar al directorio destino ---
echo Cambiando al directorio: %TARGET_DIR%...
cd /d "%TARGET_DIR%"
if errorlevel 1 (
    echo Error al acceder al directorio %TARGET_DIR%.
    exit /b 1
)

REM --- Navegar al directorio del proyecto ---
echo Navegando al directorio del proyecto %PROJECT_NAME%...
cd /d "%PROJECT_NAME%"
if errorlevel 1 (
    echo Error al acceder al directorio del proyecto.
    exit /b 1
)

echo Ejecutando Prisma DB Pull...
call npx prisma db pull

echo Ejecutando Prisma Reset...
call npx prisma migrate reset

echo Ejecutando Prisma Migrate...
call npx prisma migrate dev --name init

echo Ejecutando ESLint Fix...
call npx eslint --fix

echo Ejecutando Linter...
call npm run lint

echo Iniciando servidor en modo desarrollo...
npm run start:dev
