import maya.cmds as cmds

class CarroRigUI:
    def __init__(self):
        self.window_name = "carro_rig_ui"
        
        # Callbacks - inicializados como funciones vacías
        self.on_crear_rig = self._callback_no_definido
        self.on_ajustar_rig = self._callback_no_definido
        self.on_limpiar_rig = self._callback_no_definido
        self.on_verificar_escena = self._callback_no_definido
        
        print("🎨 CarroRigUI inicializado")
    
    def _callback_no_definido(self):
        """Callback por defecto cuando no está definido"""
        cmds.confirmDialog(
            title="Función No Disponible", 
            message="❌ Esta función no está configurada\n\nConecta los callbacks usando:\nui.on_crear_rig = mi_funcion",
            button=["OK"]
        )
    
    def mostrar_interfaz_principal(self):
        """Muestra la interfaz principal"""
        # Cerrar ventana existente
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)
        
        # Crear ventana principal
        window = cmds.window(
            self.window_name, 
            title="🚗 Rig de Carro - Sistema Coordinado", 
            width=400, 
            height=500,
            sizeable=False
        )
        
        main_layout = cmds.columnLayout(adj=True, rowSpacing=10)
        
        # ==================== HEADER ====================
        cmds.text(label="SISTEMA COORDINADO DE RIG PARA CARROS", font="boldLabelFont", height=30)
        cmds.separator(h=10, style="in")
        
        # ==================== DIAGNÓSTICO ====================
        cmds.frameLayout(
            label="🔍 DIAGNÓSTICO DE ESCENA", 
            collapse=False,
            marginWidth=10,
            marginHeight=10
        )
        diag_layout = cmds.columnLayout(adj=True, rowSpacing=5)
        
        cmds.button(
            label="VERIFICAR ESTADO DE ESCENA", 
            bgc=(0.2, 0.5, 0.8),
            height=35,
            command=lambda *_: self.on_verificar_escena()
        )
        cmds.text(
            label="Analiza la escena y detecta geometrías", 
            align="center", 
            font="smallPlainLabelFont"
        )
        cmds.setParent("..")
        cmds.setParent("..")
        
        cmds.separator(h=10, style="in")
        
        # ==================== RIG PRINCIPAL ====================
        cmds.frameLayout(
            label="🛠️ RIG PRINCIPAL", 
            collapse=False,
            marginWidth=10,
            marginHeight=10
        )
        rig_layout = cmds.columnLayout(adj=True, rowSpacing=5)
        
        # Botón principal - Crear Rig
        cmds.button(
            label="🎯 CREAR RIG COMPLETO", 
            bgc=(0.3, 0.7, 0.3),
            height=45,
            command=lambda *_: self.on_crear_rig()
        )
        cmds.text(
            label="Crea el sistema completo de doble cadena", 
            align="center", 
            font="smallPlainLabelFont"
        )
        
        cmds.separator(h=5, style="none")
        
        # Botón secundario - Ajustar
        cmds.button(
            label="🔧 AJUSTAR RIG EXISTENTE", 
            bgc=(0.8, 0.6, 0.2),
            height=35,
            command=lambda *_: self.on_ajustar_rig()
        )
        
        # Botón peligroso - Limpiar
        cmds.button(
            label="🗑️ LIMPIAR RIG", 
            bgc=(0.8, 0.3, 0.3),
            height=30,
            command=lambda *_: self.on_limpiar_rig()
        )
        cmds.text(
            label="Elimina todos los elementos del rig", 
            align="center", 
            font="smallPlainLabelFont"
        )
        
        cmds.setParent("..")
        cmds.setParent("..")
        
        cmds.separator(h=10, style="in")
        
        # ==================== INFORMACIÓN ====================
        cmds.frameLayout(
            label="📋 INFORMACIÓN DEL SISTEMA", 
            collapse=True,
            marginWidth=10,
            marginHeight=5
        )
        info_layout = cmds.columnLayout(adj=True, rowSpacing=3)
        
        cmds.text(label="• Busca automáticamente:", align="left", font="smallPlainLabelFont")
        cmds.text(label="  - axioma_carro (chasis)", align="left", font="smallPlainLabelFont")
        cmds.text(label="  - 4 ruedas con nombres estándar", align="left", font="smallPlainLabelFont")
        cmds.text(label="  - Ejes delantero/trasero", align="left", font="smallPlainLabelFont")
        
        cmds.separator(h=5, style="none")
        
        cmds.text(label="• Crea sistema de doble cadena:", align="left", font="smallPlainLabelFont")
        cmds.text(label="  - 10 joints de deformación", align="left", font="smallPlainLabelFont")
        cmds.text(label="  - 11 joints drivers", align="left", font="smallPlainLabelFont")
        cmds.text(label="  - Controles de animación", align="left", font="smallPlainLabelFont")
        
        cmds.setParent("..")
        cmds.setParent("..")
        
        # ==================== FOOTER ====================
        cmds.separator(h=10, style="none")
        cmds.button(
            label="CERRAR", 
            bgc=(0.5, 0.5, 0.5),
            height=25,
            command=lambda *_: cmds.deleteUI(window)
        )
        
        # Mostrar ventana
        cmds.showWindow(window)
        
        # Centrar ventana
        self._centrar_ventana(window)
    
    def _centrar_ventana(self, window):
        """Centra la ventana en la pantalla"""
        try:
            # Obtener dimensiones de la ventana
            width = cmds.window(window, q=True, width=True)
            height = cmds.window(window, q=True, height=True)
            
            # Obtener dimensiones del área de trabajo
            main_window = cmds.window("MayaWindow", q=True, width=True, height=True)
            
            # Calcular posición centrada
            x = (main_window - width) // 2
            y = (main_window - height) // 2
            
            # Posicionar ventana
            cmds.window(window, e=True, topLeftCorner=[x, y])
            
        except Exception:
            pass  # Si falla el centrado, no es crítico
    
    def conectar_callbacks(self, crear_rig=None, ajustar_rig=None, limpiar_rig=None, verificar_escena=None):
        """Conecta las funciones callback a los botones"""
        if crear_rig:
            self.on_crear_rig = crear_rig
        if ajustar_rig:
            self.on_ajustar_rig = ajustar_rig
        if limpiar_rig:
            self.on_limpiar_rig = limpiar_rig
        if verificar_escena:
            self.on_verificar_escena = verificar_escena
        
        print("✅ Callbacks conectados a la UI")
    
    def mostrar_mensaje_estado(self, titulo, mensaje, tipo="info"):
        """Muestra un mensaje de estado en la UI"""
        colores = {
            "info": (0.2, 0.5, 0.8),
            "exito": (0.3, 0.7, 0.3),
            "error": (0.8, 0.3, 0.3),
            "advertencia": (0.8, 0.6, 0.2)
        }
        
        bgc = colores.get(tipo, (0.5, 0.5, 0.5))
        
        cmds.confirmDialog(
            title=titulo,
            message=mensaje,
            button=["OK"],
            backgroundColor=bgc
        )


# ============================================================================
# FUNCIONES DE INTEGRACIÓN CON EL SISTEMA DE RIG
# ============================================================================

def crear_ui_integrada():
    """Crea la UI integrada con el sistema de rig"""
    ui = CarroRigUI()
    
    try:
        # Importar e integrar con el sistema de rig
        from carro_rig import crear_rig_carro, limpiar_rig_existente
        from carro_rig_utils import buscar_objetos_escena_filtrado
        
        # Definir funciones callback
        def verificar_escena():
            """Verifica el estado de la escena"""
            try:
                chasis, ruedas, ejes = buscar_objetos_escena_filtrado()
                
                mensaje = f"""
📊 DIAGNÓSTICO DE ESCENA:

✅ Chasis encontrado: {chasis if chasis else '❌ NO ENCONTRADO'}
✅ Ruedas encontradas: {len(ruedas)}/4
✅ Ejes encontrados: {len(ejes)}/2

📝 Nombres de ruedas:
"""
                for rueda in ruedas:
                    mensaje += f"   - {rueda}\n"
                
                for eje in ejes:
                    mensaje += f"   - {eje}\n"
                
                if not chasis:
                    mensaje += "\n❌ PROBLEMAS:\n- No se encontró el chasis 'axioma_carro'"
                    ui.mostrar_mensaje_estado("Diagnóstico - Problemas", mensaje, "error")
                else:
                    ui.mostrar_mensaje_estado("Diagnóstico - Escena OK", mensaje, "exito")
                    
            except Exception as e:
                ui.mostrar_mensaje_estado("Error en Diagnóstico", f"❌ Error: {str(e)}", "error")
        
        def crear_rig():
            """Crea el rig completo"""
            try:
                resultado = crear_rig_carro()
                if resultado:
                    ui.mostrar_mensaje_estado("✅ Éxito", "Rig creado exitosamente", "exito")
                else:
                    ui.mostrar_mensaje_estado("❌ Error", "Falló la creación del rig", "error")
            except Exception as e:
                ui.mostrar_mensaje_estado("❌ Error Crítico", f"Error: {str(e)}", "error")
        
        def limpiar_rig():
            """Limpia el rig existente"""
            try:
                resultado = limpiar_rig_existente()
                ui.mostrar_mensaje_estado(
                    "🗑️ Limpieza Completada", 
                    f"Se eliminaron {resultado} elementos del rig", 
                    "info"
                )
            except Exception as e:
                ui.mostrar_mensaje_estado("❌ Error", f"Error al limpiar: {str(e)}", "error")
        
        def ajustar_rig():
            """Función para ajustar rig existente (placeholder)"""
            ui.mostrar_mensaje_estado(
                "🔧 Función en Desarrollo", 
                "La función de ajuste de rig está en desarrollo", 
                "advertencia"
            )
        
        # Conectar callbacks
        ui.conectar_callbacks(
            crear_rig=crear_rig,
            ajustar_rig=ajustar_rig,
            limpiar_rig=limpiar_rig,
            verificar_escena=verificar_escena
        )
        
        print("✅ UI integrada con sistema de rig")
        
    except ImportError as e:
        print(f"⚠️ No se pudo integrar con el sistema de rig: {e}")
        ui.mostrar_mensaje_estado(
            "⚠️ Sistema Incompleto", 
            "El sistema de rig no está disponible\n\nUsando UI en modo standalone", 
            "advertencia"
        )
    
    return ui


def mostrar_ui_standalone():
    """Mostrar UI de forma independiente (sin integración)"""
    ui = CarroRigUI()
    ui.mostrar_interfaz_principal()
    return ui


def mostrar_ui_completa():
    """Muestra la UI completa integrada con el sistema de rig"""
    ui = crear_ui_integrada()
    ui.mostrar_interfaz_principal()
    return ui


# ============================================================================
# EJECUCIÓN DIRECTA
# ============================================================================

if __name__ == "__main__":
    # Cuando se ejecuta directamente, usar modo integrado si está disponible
    try:
        mostrar_ui_completa()
    except Exception as e:
        print(f"⚠️ Falló UI integrada, usando standalone: {e}")
        mostrar_ui_standalone()