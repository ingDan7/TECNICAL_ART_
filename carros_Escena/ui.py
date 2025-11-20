"""
🏙️ Módulo UI - Interfaz minimalista para ciudad futurista
"""

import maya.cmds as cmds
from .Escena import CiudadFuturista

ciudad = CiudadFuturista()

class CiudadUI:
    """Interfaz minimalista con solo el botón Emerge"""
    
    def __init__(self):
        self.ventana_nombre = "ciudadFuturistaUI"
    
    def crear_interfaz(self):
        """Crea la interfaz de usuario minimalista"""
        # Cerrar ventana si existe
        if cmds.window(self.ventana_nombre, exists=True):
            cmds.deleteUI(self.ventana_nombre)
        
        # Crear ventana minimalista
        ventana = cmds.window(
            self.ventana_nombre,
            title="🌌 Ciudad Futurista",
            width=200,
            height=100
        )
        
        # Layout principal simple
        cmds.columnLayout(adjustableColumn=True, rowSpacing=10)
        
        cmds.button(
            label="🌀 EMERGE CIUDAD",
            height=60,
            backgroundColor=(0.1, 0.5, 0.8),
            command=self._emerge_ciudad
        )

        cmds.button(
            label="🧹 Limpiar Escena",
            height=35,
            bgc=(0.8, 0.2, 0.2),
            command=self.limpiar_ciudad
        )

                
        # Mostrar ventana
        cmds.showWindow(ventana)
        return ventana
    
    def _emerge_ciudad(self, *args):
        """Genera una nueva ciudad usando la configuración por defecto de core"""
        try:    
            resultado = ciudad.generar()
            
            if resultado:
                cmds.inViewMessage(
                    amg='<span style="color:#00FFFF">🌌 Ciudad Emergida</span>',
                    pos='midCenter',
                    fade=True
                )
                print("✅ Ciudad emergida exitosamente!")
            else:
                cmds.warning("❌ Error al emerger ciudad")
            
        except Exception as e:
            cmds.warning(f"❌ Error: {e}")

    def limpiar_ciudad(self, *args):
        """Limpia la escena usando el método de CiudadFuturista"""
        try:
            ciudad._limpiar_escena()
            cmds.inViewMessage(
                amg='<span style="color:#FF4444">🔥 Ciudad eliminada</span>',
                pos='midCenter',
                fade=True
            )
            print("🔥 Ciudad eliminada")
        except Exception as e:
            cmds.warning(f"❌ Error al limpiar ciudad: {e}")


def mostrar_ui():
    """Función conveniente para mostrar la UI minimalista"""
    ui = CiudadUI()
    return ui.crear_interfaz()

