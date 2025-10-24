@echo off
REM Run script for Social Image Generator Docker container (Windows)
REM This script reads configuration from .env file and runs the Docker container

echo ==========================================
echo Social Image Generator - Docker Run
echo ==========================================

REM Check if .env file exists
if not exist .env (
    echo Error: .env file not found
    echo Please create a .env file
    exit /b 1
)

REM Load environment variables from .env file
for /f "tokens=*" %%a in ('type .env ^| findstr /v "^#"') do set %%a

REM Set default values if not specified in .env
if not defined IMAGE_NAME set IMAGE_NAME=social-image-generator
if not defined IMAGE_TAG set IMAGE_TAG=latest
if not defined CONTAINER_NAME set CONTAINER_NAME=social-image-generator
if not defined PORT set PORT=5000
if not defined RESTART_POLICY set RESTART_POLICY=unless-stopped
if not defined UPLOADS_DIR set UPLOADS_DIR=./uploads
if not defined OUTPUT_DIR set OUTPUT_DIR=./output
if not defined GENERATED_DIR set GENERATED_DIR=./generated
if not defined CONFIG_DIR set CONFIG_DIR=./config
if not defined FLASK_ENV set FLASK_ENV=production

echo Container configuration:
echo   Image: %IMAGE_NAME%:%IMAGE_TAG%
echo   Container name: %CONTAINER_NAME%
echo   Port: %PORT%
echo   Restart policy: %RESTART_POLICY%
echo.

REM Create necessary directories if they don't exist
echo Creating necessary directories...
if not exist "%UPLOADS_DIR%\main" mkdir "%UPLOADS_DIR%\main"
if not exist "%UPLOADS_DIR%\background" mkdir "%UPLOADS_DIR%\background"
if not exist "%UPLOADS_DIR%\watermark" mkdir "%UPLOADS_DIR%\watermark"
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"
if not exist "%GENERATED_DIR%" mkdir "%GENERATED_DIR%"
if not exist "%CONFIG_DIR%" mkdir "%CONFIG_DIR%"

REM Stop and remove existing container if it exists
docker ps -aq -f name=%CONTAINER_NAME% >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo Stopping and removing existing container...
    docker stop %CONTAINER_NAME% >nul 2>&1
    docker rm %CONTAINER_NAME% >nul 2>&1
)

echo Starting container...

REM Get current directory
set CURRENT_DIR=%CD%

REM Run the container
docker run -d ^
    --name %CONTAINER_NAME% ^
    --restart %RESTART_POLICY% ^
    -p %PORT%:5000 ^
    -v "%CURRENT_DIR%/%UPLOADS_DIR%:/app/uploads" ^
    -v "%CURRENT_DIR%/%OUTPUT_DIR%:/app/output" ^
    -v "%CURRENT_DIR%/%GENERATED_DIR%:/app/generated" ^
    -e FLASK_ENV=%FLASK_ENV% ^
    -e PYTHONPATH=/app/src ^
    -e PYTHONDONTWRITEBYTECODE=1 ^
    -e PORT=5000 ^
    %IMAGE_NAME%:%IMAGE_TAG%

if %ERRORLEVEL% equ 0 (
    echo.
    echo ==========================================
    echo Container started successfully!
    echo ==========================================
    echo Container name: %CONTAINER_NAME%
    echo API available at: http://localhost:%PORT%
    echo.
    echo Useful commands:
    echo   View logs:        docker logs -f %CONTAINER_NAME%
    echo   Stop container:   docker stop %CONTAINER_NAME%
    echo   Start container:  docker start %CONTAINER_NAME%
    echo   Remove container: docker rm -f %CONTAINER_NAME%
    echo.
    echo Checking container status...
    timeout /t 2 /nobreak >nul
    docker ps -f name=%CONTAINER_NAME%
) else (
    echo.
    echo ==========================================
    echo Failed to start container!
    echo ==========================================
    exit /b 1
)
