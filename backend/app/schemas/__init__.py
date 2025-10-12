# backend/app/schemas/__init__.py

# Importar todos los schemas
from app.schemas.token import Token, TokenData
from app.schemas.usuario import (
    UsuarioBase, UsuarioCreate, UsuarioUpdate, UsuarioChangePassword,
    UsuarioResponse, UsuarioDetallado, UsuarioLogin, UsuarioListResponse
)
from app.schemas.estado import EstadoBase, EstadoCreate, EstadoUpdate, EstadoResponse
from app.schemas.permiso import PermisoBase, PermisoCreate, PermisoUpdate, PermisoResponse
from app.schemas.rol import (
    RolBase, RolCreate, RolUpdate, RolResponse, RolConPermisos,
    RolPermisoCreate, RolPermisoResponse
)
from app.schemas.menu import (
    MenuGrupoBase, MenuGrupoCreate, MenuGrupoUpdate, MenuGrupoResponse, MenuGrupoConMenus,
    MenuBase, MenuCreate, MenuUpdate, MenuResponse, MenuConGrupo,
    RolMenuCreate, RolMenuResponse
)
from app.schemas.usuario_historia import (
    UsuarioHistoriaBase, UsuarioHistoriaCreate, UsuarioHistoriaResponse, UsuarioHistoriaDetallada
)

__all__ = [
    # Token
    "Token", "TokenData",
    
    # Usuario
    "UsuarioBase", "UsuarioCreate", "UsuarioUpdate", "UsuarioChangePassword",
    "UsuarioResponse", "UsuarioDetallado", "UsuarioLogin", "UsuarioListResponse",
    
    # Estado
    "EstadoBase", "EstadoCreate", "EstadoUpdate", "EstadoResponse",
    
    # Permiso
    "PermisoBase", "PermisoCreate", "PermisoUpdate", "PermisoResponse",
    
    # Rol
    "RolBase", "RolCreate", "RolUpdate", "RolResponse", "RolConPermisos",
    "RolPermisoCreate", "RolPermisoResponse",
    
    # Menu
    "MenuGrupoBase", "MenuGrupoCreate", "MenuGrupoUpdate", "MenuGrupoResponse", "MenuGrupoConMenus",
    "MenuBase", "MenuCreate", "MenuUpdate", "MenuResponse", "MenuConGrupo",
    "RolMenuCreate", "RolMenuResponse",
    
    # Usuario Historia
    "UsuarioHistoriaBase", "UsuarioHistoriaCreate", "UsuarioHistoriaResponse", "UsuarioHistoriaDetallada"
]