# Pre-Build Check for Social Image Generator Docker Container
# ============================================================

param(
    [switch]$FixIssues,
    [switch]$Verbose
)

Write-Host "🔍 Pre-Build Check for Social Image Generator Docker Container" -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan

# Function to print status
function Write-Status {
    param(
        [string]$Status,
        [string]$Message
    )

    switch ($Status) {
        "success" {
            Write-Host "✅ $Message" -ForegroundColor Green
        }
        "warning" {
            Write-Host "⚠️  $Message" -ForegroundColor Yellow
        }
        "error" {
            Write-Host "❌ $Message" -ForegroundColor Red
            if ($Status -eq "error") {
                exit 1
            }
        }
        default {
            Write-Host "ℹ️  $Message" -ForegroundColor Blue
        }
    }
}

# Check if Docker is installed and running
Write-Status "info" "Checking Docker installation..."
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Status "success" "Docker is installed"
        $dockerVersion -match 'Docker version ([0-9]+\.[0-9]+\.[0-9]+)' | Out-Null
        Write-Status "info" "Docker version: $($matches[1])"
    } else {
        throw "Docker not found"
    }
} catch {
    Write-Status "error" "Docker is not installed"
    Write-Host "💡 Install Docker Desktop from: https://docs.docker.com/get-docker/" -ForegroundColor Cyan
    exit 1
}

# Check if Docker daemon is running
try {
    docker info >$null 2>&1
    Write-Status "success" "Docker daemon is running"
} catch {
    Write-Status "error" "Docker daemon is not running"
    Write-Host "💡 Start Docker Desktop and try again" -ForegroundColor Cyan
    exit 1
}

# Check required files
Write-Status "info" "Checking required files..."

$requiredFiles = @(
    "Dockerfile",
    "requirements.txt",
    "social_image_api.py",
    "src\enhanced_social_generator.py",
    "docker-compose.yml"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (!(Test-Path $file)) {
        $missingFiles += $file
    }
}

if ($missingFiles.Count -eq 0) {
    Write-Status "success" "All required files present"
} else {
    Write-Status "error" "Missing required files: $($missingFiles -join ', ')"
    exit 1
}

# Check directory structure
Write-Status "info" "Checking directory structure..."

$requiredDirs = @(
    "assets\fonts",
    "uploads\main",
    "uploads\watermark",
    "uploads\background",
    "generated",
    "output"
)

foreach ($dir in $requiredDirs) {
    if (!(Test-Path $dir)) {
        Write-Status "warning" "Directory missing: $dir - creating it..."
        try {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Status "success" "Created directory: $dir"
        } catch {
            Write-Status "error" "Failed to create directory: $dir"
            exit 1
        }
    } else {
        Write-Status "success" "Directory exists: $dir"
    }
}

# Check font files
Write-Status "info" "Checking font files..."
$fontFiles = @(
    "assets\fonts\IRANYekanBoldFaNum.ttf",
    "assets\fonts\IRANYekanMediumFaNum.ttf",
    "assets\fonts\IRANYekanRegularFaNum.ttf",
    "assets\fonts\NotoSans-Bold.ttf",
    "assets\fonts\NotoSans-Regular.ttf",
    "assets\fonts\NotoSansArabic-Bold.ttf",
    "assets\fonts\NotoSansArabic-Regular.ttf"
)

$missingFonts = 0
foreach ($font in $fontFiles) {
    if (!(Test-Path $font)) {
        Write-Status "warning" "Font file missing: $font"
        $missingFonts++
    }
}

if ($missingFonts -eq 0) {
    Write-Status "success" "All font files present"
} else {
    Write-Status "warning" "$missingFonts font files missing - text rendering may be limited"
}

# Check Python syntax
Write-Status "info" "Checking Python syntax..."
$pythonFiles = @(
    "social_image_api.py",
    "src\enhanced_social_generator.py"
)

foreach ($pyfile in $pythonFiles) {
    try {
        python -m py_compile $pyfile 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Status "success" "Python syntax OK: $pyfile"
        } else {
            throw "Syntax error"
        }
    } catch {
        Write-Status "error" "Python syntax error in: $pyfile"
        exit 1
    }
}

# Check if ports are available
Write-Status "info" "Checking if port 5000 is available..."
try {
    $connections = Get-NetTCPConnection -LocalPort 5000 -ErrorAction Stop
    if ($connections) {
        Write-Status "warning" "Port 5000 is already in use"
        Write-Host "💡 The Docker container may fail to start if port 5000 is not available" -ForegroundColor Cyan
    } else {
        Write-Status "success" "Port 5000 is available"
    }
} catch {
    # Get-NetTCPConnection not available or port is free
    Write-Status "success" "Port 5000 appears to be available"
}

# Check disk space
Write-Status "info" "Checking available disk space..."
try {
    $drive = Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='C:'"
    $freeSpaceGB = [math]::Round($drive.FreeSpace / 1GB, 2)

    if ($freeSpaceGB -lt 5) {
        Write-Status "warning" "Low disk space: ${freeSpaceGB}GB available"
        Write-Host "💡 Docker build requires at least 5GB free space" -ForegroundColor Cyan
    } else {
        Write-Status "success" "Sufficient disk space: ${freeSpaceGB}GB available"
    }
} catch {
    Write-Status "warning" "Could not check disk space"
}

# Check memory
Write-Status "info" "Checking available memory..."
try {
    $memory = Get-WmiObject -Class Win32_ComputerSystem
    $totalMemoryGB = [math]::Round($memory.TotalPhysicalMemory / 1GB, 2)

    if ($totalMemoryGB -lt 4) {
        Write-Status "warning" "Low memory: ${totalMemoryGB}GB available"
        Write-Host "💡 Docker build and container may require more memory" -ForegroundColor Cyan
    } else {
        Write-Status "success" "Sufficient memory: ${totalMemoryGB}GB available"
    }
} catch {
    Write-Status "warning" "Could not check memory"
}

# Clean up old containers/images if any
Write-Status "info" "Cleaning up old Docker resources..."
try {
    docker rm -f social-image-generator social-image-generator-dev social-image-generator-test 2>$null | Out-Null
    docker rmi -f social-image-generator:latest 2>$null | Out-Null
    Write-Status "success" "Cleanup completed"
} catch {
    Write-Status "warning" "Some cleanup operations failed"
}

# Check for common Docker issues
Write-Status "info" "Checking for common Docker issues..."

# Check if .dockerignore exists and is properly configured
if (Test-Path ".dockerignore") {
    Write-Status "success" ".dockerignore file exists"
} else {
    Write-Status "warning" ".dockerignore file missing - consider creating one"
}

# Check if requirements.txt has valid content
if (Test-Path "requirements.txt") {
    $reqContent = Get-Content "requirements.txt" -Raw
    if ($reqContent -and $reqContent.Trim().Length -gt 0) {
        Write-Status "success" "requirements.txt appears to have content"
    } else {
        Write-Status "error" "requirements.txt is empty"
    }
}

# Final status
Write-Host ""
Write-Status "success" "Pre-build check completed successfully!"
Write-Host ""
Write-Host "🚀 Ready to build Docker container" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Build commands:" -ForegroundColor Cyan
Write-Host "   docker-compose build" -ForegroundColor White
Write-Host "   docker-compose build --no-cache    # Force fresh build" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Alternative commands:" -ForegroundColor Cyan
Write-Host "   .\test_docker.ps1                   # Build and test automatically" -ForegroundColor White
Write-Host "   docker build -t social-image-generator .  # Direct Docker build" -ForegroundColor White
Write-Host ""

exit 0
