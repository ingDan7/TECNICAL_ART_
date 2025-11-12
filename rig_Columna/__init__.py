# import sys
# print(">> sys.path en init:", sys.path)



"""
Rig Columna - Sistema de rig para columna vertebral
"""

__version__ = "1.0.0"
__author__ = "Tu Nombre"

# Exportar la función que ya existe en rig_Columna.ui
from .ui import open_spine_ui

__all__ = ["open_spine_ui"]
