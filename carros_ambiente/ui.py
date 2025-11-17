# ============================================================
# 🏙️ CIUDAD EMERGENTE v11 - MÓDULO DE INTERFAZ
# ============================================================

import maya.cmds as cmds
from .Escenario import generar_ciudad, emerge_ciudad

def crear_panel_control():
    """Crea un panel de control avanzado para la ciudad."""
    if cmds.window("ciudadControlPanel", exists=True):
        cmds.deleteUI("ciudadControlPanel")
    
    window = cmds.window("ciudadControlPanel", title="🏙️ Control de Ciudad - v11", widthHeight=(350, 400))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8)
    
    # Header
    cmds.separator(height=10, style='none')
    cmds.text(label="CONTROL DE CIUDAD EMERGENTE", font="boldLabelFont", align='center')
    cmds.separator(height=10, style='in')
    
    # Configuración de edificios
    cmds.frameLayout(label="Configuración de Edificios", collapsable=True, collapse=False)
    cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(160, 30))
    
    cmds.text(label="Mínimo de Edificios:")
    min_buildings = cmds.intField(value=3, minValue=1, maxValue=20)
    
    cmds.text(label="Máximo de Edificios:")
    max_buildings = cmds.intField(value=10, minValue=3, maxValue=30)
    
    cmds.setParent('..')
    cmds.setParent('..')
    
    # Área de generación
    cmds.frameLayout(label="Área de Generación", collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.text(label="Tamaño del Área:")
    area_size = cmds.floatField(value=8.0, minValue=5.0, maxValue=50.0)
    
    cmds.setParent('..')
    cmds.setParent('..')
    
    # Controles principales
    cmds.frameLayout(label="Acciones Principales", collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    
    cmds.button(label="🧱 GENERAR CIUDAD INICIAL", 
                height=40, 
                bgc=(0.2, 0.5, 0.8),
                command=lambda *_: generar_ciudad(
                    cmds.intField(min_buildings, query=True, value=True),
                    cmds.intField(max_buildings, query=True, value=True)
                ))
    
    cmds.button(label="✨ EMERGE (NUEVA CIUDAD)", 
                height=40, 
                bgc=(0.8, 0.6, 0.2),
                command=emerge_ciudad)
    
    cmds.separator(height=5, style='none')
    
    cmds.button(label="📊 ESTADÍSTICAS", 
                height=30,
                bgc=(0.3, 0.7, 0.4),
                command=lambda *_: mostrar_estadisticas())
    
    cmds.setParent('..')
    cmds.setParent('..')
    
    # Footer
    cmds.separator(height=10, style='in')
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(175, 175))
    
    cmds.button(label="🧹 Limpiar Escena", 
                height=25,
                bgc=(0.9, 0.3, 0.3),
                command=lambda *_: limpiar_escena())
    
    cmds.button(label="❌ Cerrar", 
                height=25,
                command=lambda *_: cmds.deleteUI(window))
    
    cmds.setParent('..')
    
    cmds.showWindow(window)
    
    return window

def mostrar_estadisticas():
    """Muestra estadísticas de la ciudad actual."""
    if cmds.objExists("ciudad_procedural_grp"):
        edificios = cmds.listRelatives("ciudad_procedural_grp", children=True) or []
        cmds.confirmDialog(
            title="📊 Estadísticas de Ciudad",
            message=f"Edificios en escena: {len(edificios)}",
            button=["OK"]
        )
    else:
        cmds.confirmDialog(
            title="📊 Estadísticas de Ciudad",
            message="No hay ciudad generada actualmente",
            button=["OK"]
        )

def limpiar_escena():
    """Limpia toda la ciudad de la escena."""
    if cmds.objExists("ciudad_procedural_grp"):
        cmds.delete("ciudad_procedural_grp")
        print("🧹 Ciudad limpiada de la escena")
    else:
        cmds.confirmDialog(
            title="Limpieza",
            message="No hay ciudad para limpiar",
            button=["OK"]
        )

def ciudad_ui():
    """Interfaz principal - abre el panel de control avanzado."""
    crear_panel_control()