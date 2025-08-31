# Test Docker Setup for Social Image Generator
Write-Host "🧪 Testing Docker Setup for Social Image Generator" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Check if Docker is available
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker is available: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Check Docker Compose
$dockerComposeCmd = $null
try {
    $version = docker-compose --version 2>$null
    $dockerComposeCmd = "docker-compose"
    Write-Host "✅ Docker Compose available: $version" -ForegroundColor Green
} catch {
    try {
        $version = docker compose version 2>$null
        $dockerComposeCmd = "docker compose"
        Write-Host "✅ Docker Compose (new syntax) available: $version" -ForegroundColor Green
    } catch {
        Write-Host "❌ Docker Compose is not available" -ForegroundColor Red
        exit 1
    }
}

# Clean up existing containers
Write-Host "🧹 Cleaning up existing containers..." -ForegroundColor Yellow
try {
    & $dockerComposeCmd down --remove-orphans 2>$null
    docker rm -f social-image-generator social-image-generator-dev social-image-generator-test 2>$null
    Write-Host "✅ Cleanup completed" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Cleanup completed with warnings" -ForegroundColor Yellow
}

# Build Docker image
Write-Host "🏗️ Building Docker image..." -ForegroundColor Yellow
try {
    $buildResult = & $dockerComposeCmd build
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker image built successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to build Docker image" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Build failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Start container
Write-Host "🚀 Starting Docker container..." -ForegroundColor Yellow
try {
    $startResult = & $dockerComposeCmd up -d
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker container started" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to start Docker container" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Start failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Wait for container to be healthy
Write-Host "⏳ Waiting for container to be healthy..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 1
$healthy = $false

while ($attempt -le $maxAttempts) {
    try {
        $containerStatus = docker ps --filter "name=social-image-generator" --format "{{.Status}}"
        if ($containerStatus -and $containerStatus.Contains("healthy")) {
            Write-Host "✅ Container is healthy" -ForegroundColor Green
            $healthy = $true
            break
        }
    } catch {
        # Ignore errors
    }

    Write-Host "   Attempt $attempt/$maxAttempts`: Waiting for container to be healthy..."
    Start-Sleep -Seconds 5
    $attempt++
}

if (-not $healthy) {
    Write-Host "⚠️ Container health check timed out, but continuing..." -ForegroundColor Yellow
}

# Test API endpoints
Write-Host "🧪 Testing API endpoints..." -ForegroundColor Yellow

# Test health endpoint
try {
    $healthResponse = Invoke-WebRequest -Uri "http://localhost:5000/health" -TimeoutSec 10
    if ($healthResponse.StatusCode -eq 200) {
        Write-Host "✅ Health endpoint is responding" -ForegroundColor Green
    } else {
        Write-Host "❌ Health endpoint returned status $($healthResponse.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Health endpoint is not responding: $($_.Exception.Message)" -ForegroundColor Red
}

# Test gradient info endpoint
try {
    $infoResponse = Invoke-WebRequest -Uri "http://localhost:5000/gradient_info" -TimeoutSec 10
    if ($infoResponse.StatusCode -eq 200) {
        Write-Host "✅ Gradient info endpoint is working" -ForegroundColor Green
    } else {
        Write-Host "❌ Gradient info endpoint returned status $($infoResponse.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "⚠️ Gradient info endpoint is not responding: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Test gradient generation
Write-Host "🎨 Testing gradient generation..." -ForegroundColor Yellow

$testPayload = @{
    width = 1080
    height = 1350
    colors = @("#FF6B6B", "#FFD93D", "#6BCB77")
    gradient_type = "linear"
    direction = "vertical"
    use_hsl_interpolation = $true
} | ConvertTo-Json

try {
    $gradientResponse = Invoke-WebRequest -Uri "http://localhost:5000/generate_gradient" `
                                         -Method POST `
                                         -Body $testPayload `
                                         -ContentType "application/json" `
                                         -TimeoutSec 30

    if ($gradientResponse.StatusCode -eq 200) {
        $responseData = $gradientResponse.Content | ConvertFrom-Json
        if ($responseData.success) {
            Write-Host "✅ Gradient generation is working" -ForegroundColor Green
            Write-Host "   Generated file: $($responseData.filename)" -ForegroundColor Green
            Write-Host "   Download URL: $($responseData.download_url)" -ForegroundColor Green
        } else {
            Write-Host "❌ Gradient generation failed: $($responseData.error)" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ Gradient generation returned status $($gradientResponse.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Gradient generation failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Check volume mounts
Write-Host "📁 Checking volume mounts..." -ForegroundColor Yellow

if (Test-Path "./generated") {
    $generatedFiles = Get-ChildItem "./generated" -File -ErrorAction SilentlyContinue
    if ($generatedFiles) {
        Write-Host "✅ Generated directory has $($generatedFiles.Count) files" -ForegroundColor Green
        Write-Host "   Files: $($generatedFiles | ForEach-Object { $_.Name })" -ForegroundColor Gray
    } else {
        Write-Host "⚠️ Generated directory exists but is empty" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Generated directory not found" -ForegroundColor Red
}

if (Test-Path "./uploads") {
    Write-Host "✅ Uploads directory is mounted correctly" -ForegroundColor Green
} else {
    Write-Host "❌ Uploads directory is not mounted" -ForegroundColor Red
}

# Show container logs
Write-Host "📋 Recent container logs:" -ForegroundColor Yellow
try {
    & $dockerComposeCmd logs --tail=10
} catch {
    Write-Host "⚠️ Could not retrieve logs: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host "DOCKER TEST SUMMARY" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Count running containers
$runningContainers = docker ps --filter "name=social-image-generator" --format "{{.Names}}" | Measure-Object | Select-Object -ExpandProperty Count
Write-Host "Running Containers: $runningContainers" -ForegroundColor White

# Check API health
try {
    $health = Invoke-WebRequest -Uri "http://localhost:5000/health" -TimeoutSec 5
    Write-Host "API Health: Working" -ForegroundColor Green
} catch {
    Write-Host "API Health: Not responding" -ForegroundColor Red
}

# Count generated files
$genFileCount = 0
if (Test-Path "./generated") {
    $genFileCount = (Get-ChildItem "./generated" -File -ErrorAction SilentlyContinue | Measure-Object).Count
}
Write-Host "Generated Files: $genFileCount" -ForegroundColor White

Write-Host ""
Write-Host "Management Commands:" -ForegroundColor Yellow
Write-Host "   Stop container: $dockerComposeCmd down" -ForegroundColor Gray
Write-Host "   View logs: $dockerComposeCmd logs -f" -ForegroundColor Gray
Write-Host "   Restart: $dockerComposeCmd restart" -ForegroundColor Gray
Write-Host "   Rebuild: $dockerComposeCmd build --no-cache" -ForegroundColor Gray

Write-Host ""
Write-Host "Docker test completed!" -ForegroundColor Green
