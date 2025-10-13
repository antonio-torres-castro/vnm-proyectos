# 🌐 Sistema Web de Monitoreo de Red IP

## 📋 Descripción del Proyecto

Sistema web responsivo para visualización, análisis y exploración de datos de monitoreo de interfaces de red IP. Desarrollado con arquitectura moderna backend-frontend, proporciona una interfaz intuitiva para el monitoreo de dispositivos de red en tiempo real e histórico.

### 🎯 Características Principales

- ✅ **Solo lectura** de datos de monitoreo existentes
- ✅ **Gestión interna** de usuarios, roles, permisos y menús
- ✅ **Visualización responsiva** para dispositivos móviles y escritorio
- ✅ **Autenticación JWT** con sistema de roles jerárquico
- ✅ **Gráficos históricos** interactivos con múltiples períodos
- ✅ **Mapas de topología** integrados con Google Maps
- ✅ **Filtros avanzados** en tablas de dispositivos e interfaces

## 🏗️ Arquitectura Técnica

### Stack Tecnológico

#### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Base de Datos:** PostgreSQL 16 + PostGIS 3.4
- **ORM:** SQLAlchemy 2.0
- **Autenticación:** JWT (9 horas expiración)
- **API:** REST + WebSocket

#### Frontend
- **Framework:** React 18 + TypeScript
- **Build Tool:** Vite
- **Estilos:** TailwindCSS
- **Gráficos:** Chart.js / ECharts
- **Mapas:** Google Maps JavaScript SDK

#### Infraestructura
- **Contenedores:** Docker + Docker Compose
- **Reverse Proxy:** Nginx
- **SSL:** Let's Encrypt
- **Sistema Operativo:** Ubuntu 24.04.3 LTS (Producción)

## 📊 Módulos Funcionales

### 1. Módulo Interfaces
- Catálogo de dispositivos con filtros avanzados
- Tabla responsive con paginación servidor-side
- Filtros por: Id, IP, Tipo, Vendor, Modelo, HR, Agregador, Comuna, Región
- Botón "Ver Histórico" en cada fila

### 2. Vista Histórico Monitoreo
- Gráfico 90 días historia
- Gráfico último 30 días historia
- Gráfico último día historia
- Selector desplegable de período

### 3. Módulo Topología
- Vista topología general de Chile en Google Maps
- Vista con centro en región específica
- Vista con centro en comuna específica
- Vista con centro en interfaz (latitud/longitud)

### 4. Sistema de Autenticación
- Roles: Administrador, Supervisor, Ejecutor
- Permisos: Lectura, Creación, Modificación, Exportación
- Gestión de menús dinámicos por rol
- Auditoría de cambios de usuarios

## 🗃️ Modelo de Datos

### Esquema "sistema" (Autenticación)
- `usuarios`, `roles`, `permisos`, `rol_permisos`
- `menus`, `menu_grupo`, `rol_menus`
- `estados`, `usuario_historia`

### Esquema "monitoreo" (Datos de Red)
- `dispositivos` - Catálogo de dispositivos de red
- `interfaces` - Interfaces con métricas en tiempo real
- `interface_historico` - Series de tiempo de métricas
- `dispositivo_historico` - Historial de estados de dispositivos

## 🚀 Instalación y Desarrollo

### Prerrequisitos
- Docker Desktop 4.25+ con WSL 2
- Windows 11 (Desarrollo) / Ubuntu 24.04 (Producción)
- 8GB RAM mínimo (16GB recomendado)

### Inicio Rápido

```bash
# Clonar repositorio
git clone https://github.com/antonio-torres-castro/vnm-proyectos.git
cd vnm-proyectos

# Iniciar servicios con el script de gestión
cd database/scripts
.\manage-db.ps1 start
```

### Servicios Docker

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| PostgreSQL | 5432 | Base de datos con PostGIS |
| PgAdmin | 8081 | Interfaz web de administración BD |
| Backend | 8000 | API FastAPI |
| Frontend | 3000 | Aplicación React |

### Scripts de Automatización

```powershell
# Sistema de gestión principal
.\manage-db.ps1 start           # Iniciar todos los servicios
.\manage-db.ps1 safe-shutdown   # Apagar con backup automático
.\manage-db.ps1 restart         # Reiniciar servicios
.\manage-db.ps1 backup          # Crear backup manual
.\manage-db.ps1 restore         # Restaurar último backup
.\manage-db.ps1 status          # Estado del sistema
```

## 📅 Plan de Desarrollo

### Sprint 1: Autenticación y Estructura Base (20-26 Oct 2025)
- Configuración backend FastAPI + PostgreSQL
- APIs autenticación JWT + modelos usuarios
- Frontend React + TypeScript + TailwindCSS
- **Despliegue Preproductivo: 26 Oct 2025**

### Sprint 2: Módulo Interfaces - Tabla Principal (27 Oct - 2 Nov 2025)
- Componente tabla interfaces con todas las columnas
- Sistema filtros avanzado + paginación
- **Despliegue Preproductivo: 2 Nov 2025**

### Sprint 3: Vista Histórico Monitoreo (3-9 Nov 2025)
- Gráficos de series de tiempo (90d, 30d, 1d)
- Selector período + métricas completas
- **Despliegue Preproductivo: 9 Nov 2025**

### Sprint 4: Topología - Mapa General Chile (10-16 Nov 2025)
- Integración Google Maps SDK
- Vistas por región, comuna, interfaz
- **Despliegue Preproductivo: 16 Nov 2025**

### Sprint 5: Integración Completa (17-23 Nov 2025)
- Navegación entre módulos + optimizaciones
- **Despliegue Preproductivo: 23 Nov 2025**

### Sprint 6: Preparación Producción (24-30 Nov 2025)
- CI/CD pipeline + security hardening
- **Despliegue Preproductivo Final: 30 Nov 2025**

### 🎯 Despliegue Producción: 15 Diciembre 2025

## 🔧 Desarrollo

### Estructura del Proyecto

```
vnm-proyectos/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints
│   │   ├── models/         # Modelos SQLAlchemy
│   │   └── schemas/        # Esquemas Pydantic
│   └── requirements.txt
├── frontend/               # Aplicación React
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── pages/          # Vistas
│   │   └── services/       # Servicios API
│   └── package.json
├── database/               # Configuración BD
│   ├── scripts/            # Scripts automatización
│   ├── init.sql            # Inicialización BD
│   └── backups/            # Backups automáticos
└── docker-compose.yml      # Orquestación servicios
```

### Credenciales de Desarrollo

```
PostgreSQL:
- Usuario: monitoreo_user
- Password: monitoreo_pass
- Base de datos: monitoreo_dev

PgAdmin:
- URL: http://localhost:8081
- Email: admin@monitoreo.cl
- Password: admin123
```

## 🎨 Especificaciones UI/UX

### Paleta de Colores
- **Primario:** Rojo `#E2001A`
- **Secundario:** Azul oscuro `#0033A0`
- **Acento:** Azul claro `#00A9E0`
- **Texto:** Negro `#333333`, Gris `#666666`
- **Fondo:** Blanco `#FFFFFF`, Gris claro `#F5F5F5`

### Características de Interfaz
- **Idioma:** Español
- **Diseño:** Responsive (mobile-first)
- **Paginación:** 100 registros por página en tablas

## 🐞 Debugging y Desarrollo

### Configuración de VS Code
El proyecto incluye configuraciones completas de debugging para VS Code con Docker:

#### 🚀 Instalación Automática
```bash
# Windows
.\setup-vscode-debug.ps1

# Linux/Mac
bash setup-vscode-debug.sh
```

#### 📁 Configuraciones Disponibles
- **🚀 Full Stack Debug** - Debuggea backend + frontend simultáneamente
- **🐍 Backend Debug** - FastAPI en Docker (puerto 5678)
- **⚛️ Frontend Debug** - React en Chrome (puerto 3000)
- **🧪 Tests Debug** - Ejecución de tests con debugging

#### 📖 Documentación Completa
- <filepath>vscode-config/README_CONFIGURACION_DEBUG.md</filepath> - Guía detallada
- <filepath>DEBUG_SETUP.md</filepath> - Setup completo paso a paso

### Fix del Login del Administrador
```bash
# Arreglar password del admin (admin@monitoreo.cl / admin123)
curl -X POST http://localhost:8000/api/v1/auth/fix-admin-password
```

## 🔐 Seguridad

- Autenticación JWT con expiración de 9 horas
- Contraseñas con hash bcrypt
- Roles y permisos jerárquicos
- CORS configurado para desarrollo
- Validación de entrada con Pydantic

## 📞 Soporte y Contacto

**Desarrollador:** Antonio Torres Castro  
**Repositorio:** [https://github.com/antonio-torres-castro/vnm-proyectos](https://github.com/antonio-torres-castro/vnm-proyectos)

## 📄 Licencia

Este proyecto es de uso interno para monitoreo de redes.

---

**Estado del Proyecto:** 🟢 **Desarrollo Activo**  
**Última Actualización:** Octubre 2025  
**Próximo Hito:** Sprint 1 - Autenticación y Estructura Base
