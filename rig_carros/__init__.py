"""
Carro Rig - Sistema para crear rigs de vehículos en Maya
"""

__version__ = "1.0.0"
__author__ = "Tu Nombre"

# Importar todos los módulos disponibles
from . import cadena_joints
from . import curvas_control
from . import jerarquia
from . import skinning
from . import carro_rig_utils
from .carro_rig_ui import CarroRigUI, mostrar_ui_standalone
from .carro_rig_core import CarroRigCore

# Funciones básicas del sistema
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
        print("📦 Módulos disponibles:")
        print(f"   • cadena_joints: {hasattr(cadena_joints, 'crear_cadena_joints')}")
        print(f"   • curvas_control: {hasattr(curvas_control, 'crear_control_rueda')}")
        print(f"   • jerarquia: {hasattr(jerarquia, 'organizar_jerarquia')}")
        print(f"   • skinning: {hasattr(skinning, 'aplicar_skin')}")
        print(f"   • utils: {hasattr(carro_rig_utils, 'validar_escena')}")
        return True
    except Exception as e:
        print(f"❌ Error inicializando sistema: {e}")
        return False

def crear_rig_vehiculo_completo(nombre_vehiculo="vehiculo_rig"):
    """Función principal para crear un rig completo de vehículo"""
    try:
        from .carro_rig_core import CarroRigCore
        rig_core = CarroRigCore()
        return rig_core.crear_rig_completo(nombre_vehiculo)
    except Exception as e:
        print(f"❌ Error creando rig completo: {e}")
        return None

# Solo exportar lo que realmente existe
__all__ = [
    # Módulos
    "cadena_joints",
    "curvas_control", 
    "jerarquia",
    "skinning",
    "carro_rig_utils",
    
    # Clases principales
    "CarroRigUI", 
    "CarroRigCore", 
    
    "mostrar_ui_standalone",
    "mostrar_interfaz_principal",  # Ahora existe localmente
    "inicializar_sistema"          # Ahora existe localmente
]