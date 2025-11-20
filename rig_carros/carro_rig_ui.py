import maya.cmds as cmds

class CarroRigUI:
    def __init__(self):
        self.window_name = "carro_rig_ui"
        
        # Callbacks
        self.on_crear_rig = None
        self.on_ajustar_rig = None
        self.on_limpiar_rig = None
        self.on_verificar_escena = None
        
        print("🎨 CarroRigUI inicializado")
    
    def mostrar_interfaz_principal(self):
        """Muestra la interfaz principal"""
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)
        
        window = cmds.window(self.window_name, title="🚗 Rig de Carro - Sistema Coordinado", widthHeight=(400, 500))
        main_layout = cmds.columnLayout(adj=True, rowSpacing=10)
        
        # Header
        cmds.text(label="SISTEMA COORDINADO DE RIG PARA CARROS", font="boldLabelFont", height=30)
        cmds.separator(h=10, style="in")
        
        # Sección: Diagnóstico
        cmds.frameLayout(label="🔍 DIAGNÓSTICO", collapse=False)
        cmds.button(
            label="VER ESTADO DE ESCENA", 
            bgc=(0.2, 0.5, 0.8),
            height=35,
            command=lambda *_: self._ejecutar_callback(self.on_verificar_escena)
        )
        cmds.setParent("..")
        
        cmds.separator(h=10, style="in")
        
        # Sección: Rig Principal
        cmds.frameLayout(label="🛠️ RIG PRINCIPAL", collapse=False)
        cmds.button(
            label="CREAR RIG COMPLETO", 
            bgc=(0.3, 0.7, 0.3),
            height=40,
            command=lambda *_: self._ejecutar_callback(self.on_crear_rig)
        )
        cmds.button(
            label="AJUSTAR RIG EXISTENTE", 
            bgc=(0.8, 0.6, 0.2),
            height=35,
            command=lambda *_: self._ejecutar_callback(self.on_ajustar_rig)
        )
        cmds.button(
            label="LIMPIAR RIG", 
            bgc=(0.8, 0.3, 0.3),
            height=30,
            command=lambda *_: self._ejecutar_callback(self.on_limpiar_rig)
        )
        cmds.setParent("..")
        
        cmds.separator(h=10, style="in")
        
        # Información
        cmds.text(label="Sistema automático que busca:", align="center")
        cmds.text(label="- axioma_carro (chasis)", align="center")
        cmds.text(label="- 4 ruedas", align="center")
        cmds.text(label="- ejes (opcional)", align="center")
        
        cmds.separator(h=10, style="none")
        cmds.button(label="CERRAR", command=lambda *_: cmds.deleteUI(window))
        
        cmds.showWindow(window)
    
    def _ejecutar_callback(self, callback):
        """Ejecuta un callback si está definido"""
        if callback:
            callback()
        else:
            cmds.confirmDialog(title="Error", message="❌ Callback no definido", button=["OK"])
    
    def actualizar_estado(self, estado):
        """Actualiza el estado en la UI"""
        print(f"🔄 UI actualizada - Estado: {estado}")

# Función independiente para compatibilidad
def mostrar_ui_standalone():
    """Mostrar UI de forma independiente"""
    ui = CarroRigUI()
    ui.mostrar_interfaz_principal()

if __name__ == "__main__":
    mostrar_ui_standalone()