from app.core.database import Base

# Importar todos los modelos del sistema IAM
from app.models.estado import Estado
from app.models.permiso import Permiso
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.menu import Menu, MenuGrupo
from app.models.rol_permiso import RolPermiso
from app.models.rol_menu import RolMenu
from app.models.usuario_historia import UsuarioHistoria

# Lista de todos los modelos para fácil acceso
__all__ = [
    "Base",
    "Estado",
    "Permiso", 
    "Rol",
    "Usuario",
    "Menu",
    "MenuGrupo",
    "RolPermiso",
    "RolMenu",
    "UsuarioHistoria"
]