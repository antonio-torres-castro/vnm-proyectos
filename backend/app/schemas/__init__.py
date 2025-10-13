# backend/app/schemas/__init__.py

# Importar todos los schemas
from app.schemas.dispositivo_historico import (
    DispositivoDisponibilidad,
    DispositivoEstadisticasPeriodo,
    DispositivoEvento,
    DispositivoHistoricoBase,
    DispositivoHistoricoDetallado,
    DispositivoHistoricoFiltros,
    DispositivoHistoricoListResponse,
    DispositivoHistoricoResponse,
    DispositivoSerieEstado,
    DispositivoUbicacion,
)

# Schemas de Monitoreo
from app.schemas.dispositivos import (
    DispositivosBase,
    DispositivosDetallado,
    DispositivosEstadisticas,
    DispositivosFiltros,
    DispositivosListResponse,
    DispositivosResponse,
)
from app.schemas.estado import EstadoBase, EstadoCreate, EstadoResponse, EstadoUpdate
from app.schemas.interface_historico import (
    InterfaceHistoricoAgregado,
    InterfaceHistoricoBase,
    InterfaceHistoricoDetallado,
    InterfaceHistoricoFiltros,
    InterfaceHistoricoListResponse,
    InterfaceHistoricoResponse,
    InterfaceTendencias,
    SerieTemporalRequest,
    SerieTemporalResponse,
)
from app.schemas.interfaces import (
    InterfacesBase,
    InterfacesDetallado,
    InterfacesFiltros,
    InterfacesListResponse,
    InterfacesMetricas,
    InterfacesResponse,
)
from app.schemas.menu import (
    MenuBase,
    MenuConGrupo,
    MenuCreate,
    MenuGrupoBase,
    MenuGrupoConMenus,
    MenuGrupoCreate,
    MenuGrupoResponse,
    MenuGrupoUpdate,
    MenuResponse,
    MenuUpdate,
    RolMenuCreate,
    RolMenuResponse,
)
from app.schemas.permiso import (
    PermisoBase,
    PermisoCreate,
    PermisoResponse,
    PermisoUpdate,
)
from app.schemas.rol import (
    RolBase,
    RolConPermisos,
    RolCreate,
    RolPermisoCreate,
    RolPermisoResponse,
    RolResponse,
    RolUpdate,
)
from app.schemas.token import Token, TokenData
from app.schemas.usuario import (
    UsuarioBase,
    UsuarioChangePassword,
    UsuarioCreate,
    UsuarioDetallado,
    UsuarioListResponse,
    UsuarioLogin,
    UsuarioResponse,
    UsuarioUpdate,
)
from app.schemas.usuario_historia import (
    UsuarioHistoriaBase,
    UsuarioHistoriaCreate,
    UsuarioHistoriaDetallada,
    UsuarioHistoriaResponse,
)

__all__ = [
    # Token
    "Token",
    "TokenData",
    # Usuario
    "UsuarioBase",
    "UsuarioCreate",
    "UsuarioUpdate",
    "UsuarioChangePassword",
    "UsuarioResponse",
    "UsuarioDetallado",
    "UsuarioLogin",
    "UsuarioListResponse",
    # Estado
    "EstadoBase",
    "EstadoCreate",
    "EstadoUpdate",
    "EstadoResponse",
    # Permiso
    "PermisoBase",
    "PermisoCreate",
    "PermisoUpdate",
    "PermisoResponse",
    # Rol
    "RolBase",
    "RolCreate",
    "RolUpdate",
    "RolResponse",
    "RolConPermisos",
    "RolPermisoCreate",
    "RolPermisoResponse",
    # Menu
    "MenuGrupoBase",
    "MenuGrupoCreate",
    "MenuGrupoUpdate",
    "MenuGrupoResponse",
    "MenuGrupoConMenus",
    "MenuBase",
    "MenuCreate",
    "MenuUpdate",
    "MenuResponse",
    "MenuConGrupo",
    "RolMenuCreate",
    "RolMenuResponse",
    # Usuario Historia
    "UsuarioHistoriaBase",
    "UsuarioHistoriaCreate",
    "UsuarioHistoriaResponse",
    "UsuarioHistoriaDetallada",
    # Monitoreo - Dispositivos
    "DispositivosBase",
    "DispositivosResponse",
    "DispositivosDetallado",
    "DispositivosFiltros",
    "DispositivosListResponse",
    "DispositivosEstadisticas",
    # Monitoreo - Interfaces
    "InterfacesBase",
    "InterfacesResponse",
    "InterfacesDetallado",
    "InterfacesFiltros",
    "InterfacesListResponse",
    "InterfacesMetricas",
    # Monitoreo - Interface Hist�rico
    "InterfaceHistoricoBase",
    "InterfaceHistoricoResponse",
    "InterfaceHistoricoDetallado",
    "InterfaceHistoricoFiltros",
    "SerieTemporalRequest",
    "SerieTemporalResponse",
    "InterfaceHistoricoAgregado",
    "InterfaceTendencias",
    "InterfaceHistoricoListResponse",
    # Monitoreo - Dispositivo Hist�rico
    "DispositivoHistoricoBase",
    "DispositivoHistoricoResponse",
    "DispositivoHistoricoDetallado",
    "DispositivoHistoricoFiltros",
    "DispositivoDisponibilidad",
    "DispositivoEvento",
    "DispositivoUbicacion",
    "DispositivoSerieEstado",
    "DispositivoEstadisticasPeriodo",
    "DispositivoHistoricoListResponse",
]
