# # """
# # Carro Rig - Sistema para crear rigs de vehículos en Maya
# # """

# # __version__ = "1.0.0"
# # __author__ = "Tu Nombre"

# # # Importar las funciones principales que SÍ existen
# # from .carro_rig_ui import CarroRigUI, mostrar_ui_standalone
# # from .carro_rig_core import CarroRigCore
# # from .RigCarroManager import mostrar_interfaz_principal, inicializar_sistema

# # # Usar funciones que realmente existen
# # __all__ = ["CarroRigUI", "CarroRigCore", "mostrar_interfaz_principal", "mostrar_ui_standalone"]

# """
# Carro Rig - Sistema para crear rigs de vehículos en Maya
# """

# __version__ = "1.0.0"
# __author__ = "Tu Nombre"

# # Importar SOLO las funciones que REALMENTE existen
# from .carro_rig_ui import CarroRigUI, mostrar_ui_standalone
# from .carro_rig_core import CarroRigCoreSimple, crear_rig_carro, limpiar_rig_existente, optimizar_pesos_rig
# from .carro_rig_utils import buscar_objetos_escena_filtrado, NOMBRES_ESTANDAR
# from .RigCarroManager import mostrar_interfaz_principal, inicializar_sistema

# # Usar funciones que realmente existen
# __all__ = [
#     "CarroRigUI", 
#     "CarroRigCoreSimple", 
#     "crear_rig_carro", 
#     "limpiar_rig_existente", 
#     "optimizar_pesos_rig",
#     "buscar_objetos_escena_filtrado", 
#     "NOMBRES_ESTANDAR",
#     "mostrar_interfaz_principal",
#     "mostrar_ui_standalone",
#     "inicializar_sistema"
# ]

"""
Carro Rig - Sistema para crear rigs de vehículos en Maya
"""

__version__ = "1.0.0"
__author__ = "Tu Nombre"

# Importar las funciones optimizadas
from .carro_rig_ui import CarroRigUI, mostrar_ui_standalone
from .carro_rig_core import CarroRigCoreOptimizado, crear_rig_carro, limpiar_rig_existente, optimizar_pesos_rig
from .carro_rig_utils import buscar_objetos_escena_filtrado, NOMBRES_ESTANDAR
from .RigCarroManager import mostrar_interfaz_principal, inicializar_sistema

# Usar funciones optimizadas
__all__ = [
    "CarroRigUI", 
    "CarroRigCoreOptimizado",  # ← ACTUALIZADO
    "crear_rig_carro", 
    "limpiar_rig_existente", 
    "optimizar_pesos_rig",
    "buscar_objetos_escena_filtrado", 
    "NOMBRES_ESTANDAR",
    "mostrar_interfaz_principal",
    "mostrar_ui_standalone",
    "inicializar_sistema"
]