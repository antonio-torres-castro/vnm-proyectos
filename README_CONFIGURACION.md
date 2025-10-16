# Guia de Configuracion - Ambiente de Desarrollo Fullstack

## Requisitos Previos

1. **Python 3.11+** instalado
2. **Node.js 18+** con npm instalado  
3. **Docker Desktop** instalado y ejecutandose
4. **VS Code** instalado
5. **Git** instalado

## Paso 1: Configurar Ambiente Virtual de Python

### 1.1 Crear ambiente virtual en la raiz del proyecto

```bash
# Navegar a la raiz del proyecto
cd C:\vnm-proyectos

# Crear ambiente virtual
python -m venv .venv

# Activar ambiente virtual
.venv\Scripts\activate

# Actualizar pip
python -m pip install --upgrade pip
```

### 1.2 Instalar dependencias de Python

```bash
# Instalar dependencias del backend
pip install -r backend\requirements.txt

# Verificar instalacion
pip list
```

### 1.3 Verificar Python

```bash
# Verificar version
python --version

# Verificar que FastAPI se instalo
python -c "import fastapi; print('FastAPI OK')"
```

## Paso 2: Configurar Node.js y Frontend

### 2.1 Verificar Node.js

```bash
# Verificar version de Node.js
node --version

# Verificar npm (si no funciona, reinstalar Node.js)
npm --version
```

### 2.2 Si npm no funciona:

1. Desinstalar Node.js desde Panel de Control
2. Descargar Node.js LTS desde https://nodejs.org
3. Instalar con opcion "Add to PATH" marcada
4. Reiniciar terminal y verificar: `npm --version`

### 2.3 Instalar dependencias del frontend

```bash
# Navegar al frontend
cd frontend

# Instalar dependencias
npm install

# Verificar instalacion
npm list

# Regresar a raiz
cd ..
```

## Paso 3: Configurar VS Code

### 3.1 Abrir proyecto en VS Code

```bash
# Desde la raiz del proyecto
code .
```

### 3.2 Instalar extensiones recomendadas

Cuando VS Code abra, instalar estas extensiones:

1. **Python** (Microsoft)
2. **Python Debugger** (Microsoft) 
3. **ES7+ React/Redux/React-Native snippets**
4. **TypeScript and JavaScript Language Features**
5. **Docker** (Microsoft)
6. **PostgreSQL** (Microsoft)

### 3.3 Configurar interprete de Python

1. Presionar `Ctrl+Shift+P`
2. Escribir "Python: Select Interpreter"
3. Seleccionar: `.venv\Scripts\python.exe`

## Paso 4: Configurar Base de Datos con Docker

### 4.1 Iniciar containers

```bash
# Usar el script simplificado
python docker_manager.py start

# O manualmente
docker-compose up -d
```

### 4.2 Verificar que containers esten ejecutandose

```bash
# Ver estado
python docker_manager.py status

# Ver URLs de acceso
python docker_manager.py urls
```

### 4.3 Probar acceso a servicios

- **pgAdmin**: http://localhost:8081
  - Email: admin@monitoreo.cl
  - Password: admin123
- **PostgreSQL**: localhost:5432
  - DB: monitoreo_dev
  - User: monitoreo_user
  - Password: monitoreo_pass

## Paso 5: Configurar Depuracion Fullstack

### 5.1 Para Backend (FastAPI)

1. En VS Code, ir a archivo `backend/main.py`
2. Poner breakpoint en alguna linea
3. Presionar `F5` o ir a Run -> Start Debugging
4. Seleccionar "Python: FastAPI" si se solicita

### 5.2 Para Frontend (React)

1. En terminal, desde raiz del proyecto:
```bash
cd frontend
npm run dev
```
2. Abrir http://localhost:3000
3. Usar DevTools del navegador para depurar

### 5.3 Para depuracion con containers

```bash
# Iniciar en modo debug
python docker_manager.py start-debug

# Backend estara disponible en puerto 5678 para debugger
# Frontend en puerto 3000 con hot reload
```

## Paso 6: Flujo de Desarrollo Diario

### 6.1 Iniciar desarrollo

```bash
# 1. Activar ambiente virtual
.venv\Scripts\activate

# 2. Iniciar containers
python docker_manager.py start

# 3. Abrir VS Code
code .

# 4. Para frontend (en terminal separada)
cd frontend
npm run dev
```

### 6.2 Durante desarrollo

- **Backend**: Modificar archivos en `backend/`, VS Code auto-detectara cambios
- **Frontend**: Modificar archivos en `frontend/`, hot reload automatico
- **Base de datos**: Usar pgAdmin en http://localhost:8081

### 6.3 Finalizar desarrollo

```bash
# Detener containers
python docker_manager.py stop

# Desactivar ambiente virtual
deactivate
```

## Comandos Utiles

### Docker
```bash
# Ver logs de todos los servicios
python docker_manager.py logs

# Ver logs de un servicio especifico
python docker_manager.py logs backend

# Reiniciar containers
python docker_manager.py restart

# Limpiar todo
python docker_manager.py clean
```

### Python
```bash
# Activar ambiente
.venv\Scripts\activate

# Instalar nuevo paquete
pip install nombre_paquete

# Actualizar requirements
pip freeze > backend\requirements.txt
```

### Frontend
```bash
cd frontend

# Instalar nuevo paquete
npm install nombre_paquete

# Ejecutar en modo desarrollo
npm run dev

# Construir para produccion
npm run build
```

## Solucion de Problemas

### Error "npm no encontrado"
- Reinstalar Node.js con opcion "Add to PATH"
- Reiniciar terminal/VS Code

### Error de compilacion Python (Rust/Cargo)
- Ya solucionado usando `psycopg2-binary` en lugar de `psycopg2`

### Containers no inician
```bash
# Verificar Docker
docker --version

# Ver logs de error
docker-compose logs

# Limpiar y reiniciar
python docker_manager.py clean
python docker_manager.py start
```

### Puerto ocupado
```bash
# Ver que esta usando el puerto
netstat -an | findstr :8000

# Matar proceso si es necesario
taskkill /F /PID [numero_de_proceso]
```

### VS Code no detecta ambiente virtual
1. `Ctrl+Shift+P`
2. "Python: Select Interpreter"  
3. Seleccionar `.venv\Scripts\python.exe`
4. Reiniciar VS Code

## Estructura Final del Proyecto

```
vnm-proyectos/
├── .venv/                    # Ambiente virtual Python (raiz)
├── backend/                  # Codigo FastAPI
├── frontend/                 # Codigo React
├── database/                 # Scripts y datos DB
├── docker-compose.yml        # Configuracion Docker
├── docker_manager.py         # Script simplificado Docker
└── README_CONFIGURACION.md   # Esta guia
```