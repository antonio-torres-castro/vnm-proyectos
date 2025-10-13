from app.core.database import Base
from app.models.dispositivo_historico import DispositivoHistorico

# Importar todos los modelos del sistema de Monitoreo
from app.models.dispositivos import Dispositivos

# Importar todos los modelos del sistema IAM
from app.models.estado import Estado
from app.models.interface_historico import InterfaceHistorico
from app.models.interfaces import Interfaces
from app.models.menu import Menu, MenuGrupo
from app.models.permiso import Permiso
from app.models.rol import Rol
from app.models.rol_menu import RolMenu
from app.models.rol_permiso import RolPermiso
from app.models.usuario import Usuario
from app.models.usuario_historia import UsuarioHistoria

# Lista de todos los modelos para fácil acceso
__all__ = [
    "Base",
    # Modelos IAM
    "Estado",
    "Permiso",
    "Rol",
    "Usuario",
    "Menu",
    "MenuGrupo",
    "RolPermiso",
    "RolMenu",
    "UsuarioHistoria",
    # Modelos Monitoreo
    "Dispositivos",
    "Interfaces",
    "InterfaceHistorico",
    "DispositivoHistorico",
]
