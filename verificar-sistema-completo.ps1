#!/usr/bin/env pwsh

Write-Host "=== VERIFICACION COMPLETA DEL SISTEMA ===" -ForegroundColor Green
Write-Host "Verificando estado despues de reinicializacion..." -ForegroundColor Cyan
Write-Host ""

# 1. Verificar contenedores
Write-Host "1. VERIFICANDO CONTENEDORES" -ForegroundColor Yellow
Write-Host "=============================="
docker-compose -f docker-compose.debug.yml ps
Write-Host ""

# 2. Verificar logs de PostgreSQL
Write-Host "2. VERIFICANDO LOGS DE POSTGRESQL" -ForegroundColor Yellow
Write-Host "=================================="
Write-Host "Ultimos 10 logs de PostgreSQL:"
docker logs vnm_postgres_debug --tail 10
Write-Host ""

# 3. Verificar conectividad a BD
Write-Host "3. VERIFICANDO CONECTIVIDAD A BD" -ForegroundColor Yellow
Write-Host "================================="
$psql_test = docker exec vnm_postgres_debug psql -U monitoreo_user -d monitoreo_dev -c "\dt seguridad.*" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host " Conexion a BD exitosa" -ForegroundColor Green
    Write-Host "Tablas en esquema seguridad:"
    Write-Host $psql_test
}
else {
    Write-Host " Error conectando a BD:" -ForegroundColor Red
    Write-Host $psql_test
}
Write-Host ""

# 4. Verificar datos del usuario admin
Write-Host "4. VERIFICANDO DATOS DE USUARIO ADMIN" -ForegroundColor Yellow
Write-Host "======================================"
$user_data = docker exec vnm_postgres_debug psql -U monitoreo_user -d monitoreo_dev -c "SELECT email, nombre, LEFT(clave_hash, 20) || '...' as hash_preview FROM seguridad.usuario WHERE email = 'admin@monitoreo.cl';" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host " Datos del usuario admin encontrados:" -ForegroundColor Green
    Write-Host $user_data
}
else {
    Write-Host " Error consultando usuario admin:" -ForegroundColor Red
    Write-Host $user_data
}
Write-Host ""

# 5. Verificar backend
Write-Host "5. VERIFICANDO BACKEND API" -ForegroundColor Yellow
Write-Host "=========================="
Write-Host "Verificando logs del backend:"
docker logs vnm_backend_debug --tail 5
Write-Host ""

Write-Host "Probando endpoint de health del backend:"
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 10
    Write-Host " Backend responde correctamente:" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json)
}
catch {
    Write-Host " Backend no responde:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
Write-Host ""

# 6. Probar login
Write-Host "6. PROBANDO LOGIN CON CREDENCIALES" -ForegroundColor Yellow
Write-Host "==================================="
Write-Host "Probando login con admin@monitoreo.cl / admin123:"

$loginData = @{
    email    = "admin@monitoreo.cl"
    password = "admin123"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" -Method Post -Body $loginData -ContentType "application/json" -TimeoutSec 10
    Write-Host " LOGIN EXITOSO" -ForegroundColor Green
    Write-Host "Token recibido: $($loginResponse.access_token.Substring(0, 20))..."
    Write-Host "Usuario: $($loginResponse.user_info.nombre) ($($loginResponse.user_info.email))"
}
catch {
    Write-Host " ERROR EN LOGIN:" -ForegroundColor Red
    Write-Host $_.Exception.Message

    # Informacion adicional para debugging
    if ($_.Exception.Response) {
        $responseStream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($responseStream)
        $responseBody = $reader.ReadToEnd()
        Write-Host "Detalle del error: $responseBody" -ForegroundColor Red
    }
}
Write-Host ""

# 7. Verificar frontend
Write-Host "7. VERIFICANDO FRONTEND" -ForegroundColor Yellow
Write-Host "======================"
Write-Host "Verificando logs del frontend:"
docker logs vnm_frontend_debug --tail 5
Write-Host ""

Write-Host "Probando acceso al frontend:"
try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:3000" -Method Get -TimeoutSec 10 -UseBasicParsing
    Write-Host " Frontend responde correctamente (Status: $($frontendResponse.StatusCode))" -ForegroundColor Green
}
catch {
    Write-Host " Frontend no responde:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
Write-Host ""

Write-Host "=== RESUMEN DE VERIFICACION ===" -ForegroundColor Green
Write-Host "Si todo esta ok, el sistema esta listo para usar"
Write-Host "URLs de acceso:"
Write-Host "- Frontend: http://localhost:3000"
Write-Host "- Backend API: http://localhost:8000"
Write-Host "- Documentacion API: http://localhost:8000/docs"
Write-Host ""
Write-Host "Credenciales de login:"
Write-Host "- Email: admin@monitoreo.cl"
Write-Host "- Password: admin123"
