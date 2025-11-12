"""
ChailTail - Sistema de Rig para Colas Dinámicas en Maya
"""

__version__ = "1.0.0"
__author__ = "Tu Nombre"

# Exportar funciones principales para fácil acceso
from .tail_rig_main import open_ui, execute_all_steps_Tail
from .tail_rig_curve import use_existing_joints, make_curve_dynamic
from .tail_rig_ik import create_ik_spline_handle
from .tail_rig_dynamics import configure_nucleus_and_follicle
from .tail_rig_controls import create_dynamic_control
from .tail_rig_geometry import create_poly_tail, create_body_and_head, create_torus_system

__all__ = [
    'open_ui',
    'execute_all_steps_Tail', 
    'use_existing_joints',
    'make_curve_dynamic',
    'create_ik_spline_handle',
    'configure_nucleus_and_follicle',
    'create_dynamic_control',
    'create_poly_tail',
    'create_body_and_head',
    'create_torus_system'
]