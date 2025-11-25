"""
Carro Rig - Sistema para crear rigs de vehículos en Maya
"""

__version__ = "1.0.0"
__author__ = "Tu Nombre"

# Importar SOLO las funciones que realmente existen
from .carro_rig_ui import CarroRigUI, mostrar_ui_standalone
from .carro_rig_core import CarroRigCore

# NO importar funciones que no existen en RigCarroManager
# En su lugar, definir funciones básicas aquí mismo

def mostrar_interfaz_principal():
    """Función básica para mostrar la interfaz - definida localmente"""
    try:
        from .carro_rig_ui import mostrar_ui_standalone
        mostrar_ui_standalone()
        return True
    except Exception as e:
        print(f"❌ Error mostrando interfaz: {e}")
        return False

def inicializar_sistema():
    """Función básica para inicializar el sistema - definida localmente"""
    try:
        print("🚗 Sistema Rig Carro inicializado")
        return True
    except Exception as e:
        print(f"❌ Error inicializando sistema: {e}")
        return False

# Solo exportar lo que realmente existe
__all__ = [
    "CarroRigUI", 
    "CarroRigCore", 
    "mostrar_ui_standalone",
    "mostrar_interfaz_principal",  # Ahora existe localmente
    "inicializar_sistema"          # Ahora existe localmente
]