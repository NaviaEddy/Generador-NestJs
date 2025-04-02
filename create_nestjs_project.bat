@echo off
REM --- Validación del nombre del proyecto ---
echo Verificando si se proporciono el nombre del proyecto...
if "%~1"=="" (
    echo Error: Debes proporcionar un nombre para el proyecto.
    exit /b 1
)
set "PROJECT_NAME=%~1"
echo Nombre del proyecto: %PROJECT_NAME%

REM --- Definir directorio de destino ---
set "TARGET_DIR=.\nestjs"
echo Directorio de destino: %TARGET_DIR%

REM --- Crear el directorio TARGET_DIR si no existe ---
if not exist "%TARGET_DIR%" (
    echo Creando el directorio %TARGET_DIR%...
    mkdir "%TARGET_DIR%"
    echo Directorio creado.
) else (
    echo El directorio %TARGET_DIR% ya existe.
)

REM --- Verificar si el CLI de NestJS está instalado ---
echo Verificando si el CLI de NestJS esta instalado...
where nest >nul 2>&1
if errorlevel 1 (
    echo NestJS CLI no encontrado, instalandolo...
    npm install -g @nestjs/cli
    if errorlevel 1 (
        echo Error al instalar NestJS CLI.
        exit /b 1
    )
) else (
    echo NestJS CLI ya esta instalado.
)

REM --- Cambiar al directorio destino ---
echo Cambiando al directorio: %TARGET_DIR%...
cd /d "%TARGET_DIR%"
if errorlevel 1 (
    echo Error al acceder al directorio %TARGET_DIR%.
    exit /b 1
)

REM --- Crear el proyecto en NestJS ---
echo Creando el proyecto en NestJS...
call nest new "%PROJECT_NAME%" --package-manager npm
if errorlevel 1 (
    echo Error al crear el proyecto con NestJS.
    exit /b 1
)

REM --- Navegar al directorio del proyecto ---
echo Navegando al directorio del proyecto %PROJECT_NAME%...
cd /d "%PROJECT_NAME%"
if errorlevel 1 (
    echo Error al acceder al directorio del proyecto.
    exit /b 1
)

REM --- Instalar dependencias ---
echo Instalando dependencia: prisma --save-dev...
call npm install prisma --save-dev
if errorlevel 1 (
    echo Error al instalar prisma.
    exit /b 1
)

echo Instalando dependencia: @prisma/client...
call npm install @prisma/client
if errorlevel 1 (
    echo Error al instalar @prisma/client.
    exit /b 1
)

echo Instalando dependencia: @nestjs/jwt
npm install @nestjs/jwt
if errorlevel 1 (
    echo Error al instalar @nestjs/jwt.
    exit /b 1
)

echo Proceso completado exitosamente.
