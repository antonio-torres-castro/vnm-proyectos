# backend/app/models/__init__.py
from app.core.database import Base

# Importar solo los modelos esenciales para empezar
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.permiso import Permiso
from app.models.estado import Estado

# Comentar temporalmente los modelos que no son críticos para el inicio
# from app.models.menu import Menu, MenuGrupo
# from app.models.rol_permiso import RolPermiso
# from app.models.rol_menu import RolMenu