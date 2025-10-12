# Script de Testing Completo - Sistema VNM Monitoreo
# Ejecuta pruebas automatizadas de infraestructura, backend y frontend

param(
    [string]$phase = "all"
)

function Write-TestHeader {
    param([string]$title)
    Write-Host "`n" + "="*60 -ForegroundColor Cyan
    Write-Host " $title" -ForegroundColor Yellow
    Write-Host "="*60 -ForegroundColor Cyan
}

function Write-TestResult {
    param([string]$test, [bool]$result, [string]$details = "")
    $status = if($result) { "✅ PASS" } else { "❌ FAIL" }
    Write-Host "[$status] $test" -ForegroundColor $(if($result) { "Green" } else { "Red" })
    if($details) { Write-Host "    $details" -ForegroundColor Gray }
}

function Test-Infrastructure {
    Write-TestHeader "FASE 1: TESTING DE INFRAESTRUCTURA"
    
    # Test 1: Docker containers running
    Write-Host "`n🔍 Verificando contenedores Docker..." -ForegroundColor Cyan
    $containers = docker ps --format "{{.Names}} {{.Status}}"
    
    $postgresRunning = $containers | Select-String "monitoreo_postgres.*Up"
    $pgadminRunning = $containers | Select-String "monitoreo_pgadmin.*Up"
    $backendRunning = $containers | Select-String "monitoreo_backend.*Up"
    $frontendRunning = $containers | Select-String "monitoreo_frontend.*Up"
    
    Write-TestResult "PostgreSQL Container" ($null -ne $postgresRunning) $postgresRunning
    Write-TestResult "pgAdmin Container" ($null -ne $pgadminRunning) $pgadminRunning
    Write-TestResult "Backend Container" ($null -ne $backendRunning) $backendRunning
    Write-TestResult "Frontend Container" ($null -ne $frontendRunning) $frontendRunning
    
    # Test 2: Database connectivity
    Write-Host "`n🔍 Verificando conectividad de base de datos..." -ForegroundColor Cyan
    try {
        $dbTest = docker exec monitoreo_postgres psql -U monitoreo_user -d monitoreo_dev -c "SELECT 1;" 2>$null
        $dbConnected = $LASTEXITCODE -eq 0
        Write-TestResult "Database Connection" $dbConnected
        
        if($dbConnected) {
            $userCount = docker exec monitoreo_postgres psql -U monitoreo_user -d monitoreo_dev -t -c "SELECT COUNT(*) FROM seguridad.usuario;" 2>$null
            $hasUsers = $userCount -match '\d+' -and [int]$userCount.Trim() -gt 0
            Write-TestResult "Auth Users Exist" $hasUsers "Users count: $($userCount.Trim())"
        }
    }
    catch {
        Write-TestResult "Database Connection" $false $_.Exception.Message
    }
    
    # Test 3: pgAdmin accessibility
    Write-Host "`n🔍 Verificando accesibilidad de pgAdmin..." -ForegroundColor Cyan
    try {
        $pgadminTest = Invoke-WebRequest -Uri "http://localhost:8081/login" -Method Get -TimeoutSec 10 -UseBasicParsing
        $pgadminAccessible = $pgadminTest.StatusCode -eq 200
        Write-TestResult "pgAdmin Web Interface" $pgadminAccessible "Status: $($pgadminTest.StatusCode)"
    }
    catch {
        Write-TestResult "pgAdmin Web Interface" $false $_.Exception.Message
    }
    
    return @{
        containers = @{
            postgres = ($null -ne $postgresRunning)
            pgadmin = ($null -ne $pgadminRunning)
            backend = ($null -ne $backendRunning)
            frontend = ($null -ne $frontendRunning)
        }
        database = $dbConnected
        pgadmin = $pgadminAccessible
    }
}

function Test-Backend {
    Write-TestHeader "FASE 2: TESTING DE BACKEND API"
    
    # Test 1: Backend health check
    Write-Host "`n🔍 Verificando health del backend..." -ForegroundColor Cyan
    try {
        $healthCheck = Invoke-WebRequest -Uri "http://localhost:8000/" -Method Get -TimeoutSec 10 -UseBasicParsing
        $backendHealth = $healthCheck.StatusCode -eq 200
        Write-TestResult "Backend Health Check" $backendHealth "Status: $($healthCheck.StatusCode)"
    }
    catch {
        Write-TestResult "Backend Health Check" $false $_.Exception.Message
        return @{ health = $false }
    }
    
    # Test 2: API Documentation endpoint
    Write-Host "`n🔍 Verificando documentación API..." -ForegroundColor Cyan
    try {
        $docsCheck = Invoke-WebRequest -Uri "http://localhost:8000/docs" -Method Get -TimeoutSec 10 -UseBasicParsing
        $docsAvailable = $docsCheck.StatusCode -eq 200
        Write-TestResult "API Documentation" $docsAvailable "Status: $($docsCheck.StatusCode)"
    }
    catch {
        Write-TestResult "API Documentation" $false $_.Exception.Message
    }
    
    # Test 3: Login endpoint with valid credentials
    Write-Host "`n🔍 Testing login endpoint..." -ForegroundColor Cyan
    try {
        $loginData = @{
            email = "admin@monitoreo.cl"
            password = "admin123"
        } | ConvertTo-Json
        
        $loginResponse = Invoke-WebRequest -Uri "http://localhost:8000/auth/login" -Method Post -Body $loginData -ContentType "application/json" -TimeoutSec 10 -UseBasicParsing
        $loginSuccess = $loginResponse.StatusCode -eq 200
        
        if($loginSuccess) {
            $responseData = $loginResponse.Content | ConvertFrom-Json
            $hasToken = $null -ne $responseData.access_token
            Write-TestResult "Login with Valid Credentials" $loginSuccess "Token received: $hasToken"
            
            if($hasToken) {
                # Test 4: Protected endpoint with token
                Write-Host "`n🔍 Testing protected endpoint..." -ForegroundColor Cyan
                $headers = @{ Authorization = "Bearer $($responseData.access_token)" }
                try {
                    $protectedTest = Invoke-WebRequest -Uri "http://localhost:8000/auth/verify" -Method Get -Headers $headers -TimeoutSec 10 -UseBasicParsing
                    $protectedAccess = $protectedTest.StatusCode -eq 200
                    Write-TestResult "Protected Endpoint Access" $protectedAccess "Status: $($protectedTest.StatusCode)"
                }
                catch {
                    Write-TestResult "Protected Endpoint Access" $false $_.Exception.Message
                }
            }
        } else {
            Write-TestResult "Login with Valid Credentials" $false "Status: $($loginResponse.StatusCode)"
        }
    }
    catch {
        Write-TestResult "Login with Valid Credentials" $false $_.Exception.Message
    }
    
    # Test 5: Login with invalid credentials
    Write-Host "`n🔍 Testing login with invalid credentials..." -ForegroundColor Cyan
    try {
        $invalidLoginData = @{
            email = "invalid@test.com"
            password = "wrongpassword"
        } | ConvertTo-Json
        
        $invalidLoginResponse = Invoke-WebRequest -Uri "http://localhost:8000/auth/login" -Method Post -Body $invalidLoginData -ContentType "application/json" -TimeoutSec 10 -UseBasicParsing -ErrorAction SilentlyContinue
        $invalidLoginRejected = $invalidLoginResponse.StatusCode -eq 401
        Write-TestResult "Login Rejection (Invalid Credentials)" $invalidLoginRejected "Status: $($invalidLoginResponse.StatusCode)"
    }
    catch {
        # Si da error 401, es lo esperado
        $invalidLoginRejected = $_.Exception.Message -match "401"
        Write-TestResult "Login Rejection (Invalid Credentials)" $invalidLoginRejected "Properly rejected invalid credentials"
    }
    
    return @{
        health = $backendHealth
        docs = $docsAvailable
        login = $loginSuccess
        protected = $protectedAccess
        rejection = $invalidLoginRejected
    }
}

function Test-Frontend {
    Write-TestHeader "FASE 3: TESTING DE FRONTEND"
    
    # Test 1: Frontend accessibility
    Write-Host "`n🔍 Verificando accesibilidad del frontend..." -ForegroundColor Cyan
    try {
        $frontendTest = Invoke-WebRequest -Uri "http://localhost:3000" -Method Get -TimeoutSec 15 -UseBasicParsing
        $frontendAccessible = $frontendTest.StatusCode -eq 200
        Write-TestResult "Frontend Web Interface" $frontendAccessible "Status: $($frontendTest.StatusCode)"
        
        if($frontendAccessible) {
            $hasReactContent = $frontendTest.Content -match "react|vite|root"
            Write-TestResult "React App Loading" $hasReactContent "React content detected"
        }
    }
    catch {
        Write-TestResult "Frontend Web Interface" $false $_.Exception.Message
    }
    
    # Test 2: Static assets
    Write-Host "`n🔍 Verificando recursos estáticos..." -ForegroundColor Cyan
    try {
        # Test common static paths
        $assetsTest = Invoke-WebRequest -Uri "http://localhost:3000/vite.svg" -Method Get -TimeoutSec 10 -UseBasicParsing -ErrorAction SilentlyContinue
        $assetsAvailable = $assetsTest.StatusCode -eq 200
        Write-TestResult "Static Assets" $assetsAvailable "Vite assets loading"
    }
    catch {
        Write-TestResult "Static Assets" $false "Some assets may not be available"
    }
    
    return @{
        accessible = $frontendAccessible
        react = $hasReactContent
        assets = $assetsAvailable
    }
}

function Test-Integration {
    Write-TestHeader "FASE 4: TESTING DE INTEGRACIÓN"
    
    Write-Host "`n🔍 Verificando integración completa..." -ForegroundColor Cyan
    Write-Host "⚠️  Los tests de integración completa requieren pruebas manuales en el navegador" -ForegroundColor Yellow
    Write-Host "📋 Checklist manual requerido:" -ForegroundColor Cyan
    Write-Host "   1. Abrir http://localhost:3000" -ForegroundColor White
    Write-Host "   2. Verificar redirección a login" -ForegroundColor White
    Write-Host "   3. Login con admin@monitoreo.cl / admin123" -ForegroundColor White
    Write-Host "   4. Verificar redirección a dashboard" -ForegroundColor White
    Write-Host "   5. Verificar persistencia en recarga" -ForegroundColor White
    Write-Host "   6. Probar logout" -ForegroundColor White
    
    return @{ manual_required = $true }
}

function Show-Summary {
    param($results)
    
    Write-TestHeader "RESUMEN DE TESTING"
    
    Write-Host "`n📊 Resultados por Fase:" -ForegroundColor Cyan
    
    # Infrastructure summary
    $infraPassed = ($results.infrastructure.containers.postgres -and 
                   $results.infrastructure.containers.pgadmin -and
                   $results.infrastructure.containers.backend -and
                   $results.infrastructure.containers.frontend -and
                   $results.infrastructure.database)
    Write-TestResult "Infraestructura" $infraPassed
    
    # Backend summary
    $backendPassed = ($results.backend.health -and $results.backend.login)
    Write-TestResult "Backend API" $backendPassed
    
    # Frontend summary
    $frontendPassed = $results.frontend.accessible
    Write-TestResult "Frontend" $frontendPassed
    
    Write-Host "`n🎯 Próximos Pasos:" -ForegroundColor Cyan
    if($infraPassed -and $backendPassed -and $frontendPassed) {
        Write-Host "✅ Sistema base funcionando correctamente" -ForegroundColor Green
        Write-Host "➡️  Continuar con testing manual de integración" -ForegroundColor Yellow
        Write-Host "➡️  Implementar módulo de monitoreo en tiempo real" -ForegroundColor Yellow
    } else {
        Write-Host "❌ Errores encontrados que requieren corrección" -ForegroundColor Red
        Write-Host "➡️  Revisar logs: docker-compose logs" -ForegroundColor Yellow
        Write-Host "➡️  Verificar configuración y dependencias" -ForegroundColor Yellow
    }
}

# EJECUCIÓN PRINCIPAL
$results = @{}

switch ($phase) {
    "infrastructure" { $results.infrastructure = Test-Infrastructure }
    "backend" { $results.backend = Test-Backend }
    "frontend" { $results.frontend = Test-Frontend }
    "integration" { $results.integration = Test-Integration }
    "all" {
        $results.infrastructure = Test-Infrastructure
        $results.backend = Test-Backend
        $results.frontend = Test-Frontend
        $results.integration = Test-Integration
    }
    default {
        Write-Host "Uso: .\test-system.ps1 [infrastructure|backend|frontend|integration|all]" -ForegroundColor Yellow
        exit
    }
}

if($phase -eq "all") {
    Show-Summary $results
}
