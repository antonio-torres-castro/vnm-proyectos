from app.core.database import Base

# Solo modelos esenciales que existen
from app.models.estado import Estado
from app.models.rol import Rol
from app.models.permiso import Permiso
from app.models.usuario import Usuario

# Comentar temporalmente modelos que causan error
# from app.models.menu import Menu, MenuGrupo
# from app.models.rol_permiso import RolPermiso
# from app.models.rol_menu import RolMenu