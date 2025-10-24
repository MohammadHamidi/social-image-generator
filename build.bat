@echo off
REM Build script for Social Image Generator Docker image (Windows)
REM This script reads configuration from .env file and builds the Docker image

echo ==========================================
echo Social Image Generator - Docker Build
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

echo Building Docker image...
echo Image name: %IMAGE_NAME%:%IMAGE_TAG%
echo.

REM Build the Docker image
docker build -t "%IMAGE_NAME%:%IMAGE_TAG%" -f Dockerfile .

if %ERRORLEVEL% equ 0 (
    echo.
    echo ==========================================
    echo Build completed successfully!
    echo ==========================================
    echo Image: %IMAGE_NAME%:%IMAGE_TAG%
    echo.
    echo To run the container, execute: run.bat
) else (
    echo.
    echo ==========================================
    echo Build failed!
    echo ==========================================
    exit /b 1
)
