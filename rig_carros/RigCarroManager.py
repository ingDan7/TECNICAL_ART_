import maya.cmds as cmds
# CAMBIA ESTA IMPORTACIÓN:
from carro_rig_core import CarroRigCoreSimple, crear_rig_carro, limpiar_rig_existente
from carro_rig_ui import CarroRigUI
from carro_rig_utils import buscar_objetos_escena_filtrado

class CarroRigCoordinator:
    def __init__(self):
        self.window_name = "carro_rig_coordinator"
        
        # Inicializar controladores - USA CarroRigCoreSimple
        self.core_controller = CarroRigCoreSimple()
        self.ui_controller = CarroRigUI()
        
        # Conectar eventos
        self._conectar_eventos()
        print("✅ CarroRigCoordinator inicializado con callbacks conectados")
    
    def _conectar_eventos(self):
        """Conectar callbacks entre componentes"""
        self.ui_controller.on_crear_rig = self._crear_rig_desde_ui
        self.ui_controller.on_ajustar_rig = self._ajustar_rig_desde_ui
        self.ui_controller.on_limpiar_rig = self._limpiar_rig_desde_ui
        self.ui_controller.on_verificar_escena = self._verificar_escena_desde_ui
        print("🎯 Callbacks conectados: crear, limpiar, verificar, ajustar")
    
    def _crear_rig_desde_ui(self):
        """Callback para crear rig desde UI"""
        try:
            print("🎯 Iniciando creación de rig desde UI...")
            
            # Usar la función global que SÍ existe
            resultado = crear_rig_carro()
            
            if resultado:
                self.ui_controller.actualizar_estado("rig_creado")
                cmds.confirmDialog(title="Éxito", message="✅ Rig creado correctamente", button=["OK"])
            else:
                cmds.confirmDialog(title="Error", message="❌ Error creando rig", button=["OK"])
                
            return resultado
            
        except Exception as e:
            error_msg = f"❌ Error al crear rig: {str(e)}"
            print(error_msg)
            cmds.confirmDialog(title="Error", message=error_msg, button=["OK"])
            return False
    
    def _ajustar_rig_desde_ui(self):
        """Callback para ajustar rig desde UI"""
        try:
            print("⚙️ Ajustando rig existente...")
            
            # Función de ajuste simplificada
            if cmds.objExists("RIG_CARRO_GRP"):
                cmds.confirmDialog(title="Info", message="✅ Rig ya existe en escena", button=["OK"])
                return True
            else:
                # Si no existe rig, crear uno nuevo
                return self._crear_rig_desde_ui()
                
        except Exception as e:
            error_msg = f"❌ Error al ajustar rig: {str(e)}"
            print(error_msg)
            cmds.confirmDialog(title="Error", message=error_msg, button=["OK"])
            return False
    
    def _limpiar_rig_desde_ui(self):
        """Callback para limpiar rig desde UI"""
        try:
            print("🗑️ Limpiando rig...")
            
            elementos_eliminados = limpiar_rig_existente()
            
            self.ui_controller.actualizar_estado("rig_limpiado")
            
            cmds.confirmDialog(
                title="Limpieza Completa", 
                message=f"✅ {elementos_eliminados} elementos eliminados", 
                button=["OK"]
            )
            
            return elementos_eliminados
            
        except Exception as e:
            error_msg = f"❌ Error al limpiar rig: {str(e)}"
            print(error_msg)
            cmds.confirmDialog(title="Error", message=error_msg, button=["OK"])
            return 0
    
    def _verificar_escena_desde_ui(self):
        """Callback para verificar escena desde UI"""
        try:
            chasis, ruedas, ejes = buscar_objetos_escena_filtrado()
            
            mensaje = "🔍 DIAGNÓSTICO DE ESCENA:\n\n"
            
            # Estado del chasis
            if chasis:
                mensaje += f"✅ CHASIS: {chasis}\n"
            else:
                mensaje += "❌ CHASIS: No encontrado\n"
            
            # Estado de las ruedas
            mensaje += f"✅ RUEDAS: {len(ruedas)} encontradas\n"
            for rueda in ruedas:
                mensaje += f"   - {rueda}\n"
            
            # Estado de los ejes
            mensaje += f"✅ EJES: {len(ejes)} encontrados\n"
            for eje in ejes:
                mensaje += f"   - {eje}\n"
            
            # Estado del rig
            if cmds.objExists("RIG_CARRO_GRP"):
                mensaje += "\n✅ RIG: Presente en escena\n"
            else:
                mensaje += "\n❌ RIG: No existe en escena\n"
            
            if len(ruedas) < 4:
                mensaje += f"\n⚠️ Se recomiendan 4 ruedas (encontradas: {len(ruedas)})"
            
            cmds.confirmDialog(title="Diagnóstico de Escena", message=mensaje, button=["OK"])
            
        except Exception as e:
            cmds.confirmDialog(title="Error", message=f"❌ Error verificando escena: {str(e)}", button=["OK"])
    
    def show_ui(self):
        """Mostrar la interfaz de usuario"""
        self.ui_controller.mostrar_interfaz_principal()

# Instancia global del coordinador
rig_coordinator = None

def inicializar_sistema():
    """Inicializar el sistema completo"""
    global rig_coordinator
    rig_coordinator = CarroRigCoordinator()
    print("🧠 Sistema Rig Carro inicializado")
    return rig_coordinator

def mostrar_interfaz_principal():
    """Mostrar interfaz principal"""
    global rig_coordinator
    if rig_coordinator is None:
        rig_coordinator = inicializar_sistema()
    
    rig_coordinator.show_ui()
    return rig_coordinator

# Comandos rápidos
def crear_rig_rapido():
    """Comando rápido para crear rig"""
    coordinator = inicializar_sistema()
    coordinator._crear_rig_desde_ui()

def ajustar_rig_rapido():
    """Comando rápido para ajustar rig"""
    coordinator = inicializar_sistema()
    coordinator._ajustar_rig_desde_ui()

def limpiar_rig_rapido():
    """Comando rápido para limpiar rig"""
    coordinator = inicializar_sistema()
    coordinator._limpiar_rig_desde_ui()

# Ejecución directa
if __name__ == "__main__":
    mostrar_interfaz_principal()


import maya.cmds as cmds
# ACTUALIZA LA IMPORTACIÓN:
from carro_rig_core import CarroRigCoreOptimizado, crear_rig_carro, limpiar_rig_existente
from carro_rig_ui import CarroRigUI
from carro_rig_utils import buscar_objetos_escena_filtrado

class CarroRigCoordinator:
    def __init__(self):
        self.window_name = "carro_rig_coordinator"
        
        # Inicializar controladores - USA CarroRigCoreOptimizado
        self.core_controller = CarroRigCoreOptimizado()
        self.ui_controller = CarroRigUI()
        
        # Conectar eventos
        self._conectar_eventos()
        print("✅ CarroRigCoordinator inicializado con callbacks conectados")
    
    def _conectar_eventos(self):
        """Conectar callbacks entre componentes"""
        self.ui_controller.on_crear_rig = self._crear_rig_desde_ui
        self.ui_controller.on_ajustar_rig = self._ajustar_rig_desde_ui
        self.ui_controller.on_limpiar_rig = self._limpiar_rig_desde_ui
        self.ui_controller.on_verificar_escena = self._verificar_escena_desde_ui
        print("🎯 Callbacks conectados: crear, limpiar, verificar, ajustar")
    
    def _crear_rig_desde_ui(self):
        """Callback para crear rig desde UI"""
        try:
            print("🎯 Iniciando creación de rig desde UI...")
            
            # Usar la función global optimizada
            resultado = crear_rig_carro()
            
            if resultado:
                self.ui_controller.actualizar_estado("rig_creado")
                cmds.confirmDialog(title="Éxito", message="✅ Rig creado correctamente", button=["OK"])
            else:
                cmds.confirmDialog(title="Error", message="❌ Error creando rig", button=["OK"])
                
            return resultado
            
        except Exception as e:
            error_msg = f"❌ Error al crear rig: {str(e)}"
            print(error_msg)
            cmds.confirmDialog(title="Error", message=error_msg, button=["OK"])
            return False
    
    def _ajustar_rig_desde_ui(self):
        """Callback para ajustar rig desde UI"""
        try:
            print("⚙️ Ajustando rig existente...")
            
            # Verificar si existe rig
            if cmds.objExists("RIG_CARRO_GRP"):
                # Si existe, recrear con nueva geometría
                chasis, ruedas, ejes = buscar_objetos_escena_filtrado()
                if chasis:
                    # Limpiar y recrear
                    self._limpiar_rig_desde_ui()
                    return self._crear_rig_desde_ui()
                else:
                    cmds.confirmDialog(title="Error", message="❌ No se encontró chasis", button=["OK"])
                    return False
            else:
                # Si no existe rig, crear uno nuevo
                cmds.confirmDialog(title="Info", message="🔄 No hay rig existente, creando uno nuevo...", button=["OK"])
                return self._crear_rig_desde_ui()
                
        except Exception as e:
            error_msg = f"❌ Error al ajustar rig: {str(e)}"
            print(error_msg)
            cmds.confirmDialog(title="Error", message=error_msg, button=["OK"])
            return False
    
    def _limpiar_rig_desde_ui(self):
        """Callback para limpiar rig desde UI"""
        try:
            print("🗑️ Limpiando rig...")
            
            elementos_eliminados = limpiar_rig_existente()
            
            self.ui_controller.actualizar_estado("rig_limpiado")
            
            cmds.confirmDialog(
                title="Limpieza Completa", 
                message=f"✅ {elementos_eliminados} elementos eliminados", 
                button=["OK"]
            )
            
            return elementos_eliminados
            
        except Exception as e:
            error_msg = f"❌ Error al limpiar rig: {str(e)}"
            print(error_msg)
            cmds.confirmDialog(title="Error", message=error_msg, button=["OK"])
            return 0
    
    def _verificar_escena_desde_ui(self):
        """Callback para verificar escena desde UI"""
        try:
            chasis, ruedas, ejes = buscar_objetos_escena_filtrado()
            
            mensaje = "🔍 DIAGNÓSTICO DE ESCENA:\n\n"
            
            # Estado del chasis
            if chasis:
                mensaje += f"✅ CHASIS: {chasis}\n"
            else:
                mensaje += "❌ CHASIS: No encontrado\n"
            
            # Estado de las ruedas
            mensaje += f"✅ RUEDAS: {len(ruedas)} encontradas\n"
            for rueda in ruedas:
                mensaje += f"   - {rueda}\n"
            
            # Estado de los ejes
            mensaje += f"✅ EJES: {len(ejes)} encontrados\n"
            for eje in ejes:
                mensaje += f"   - {eje}\n"
            
            # Estado del rig
            rig_existe = cmds.objExists("RIG_CARRO_GRP")
            joints_existen = all(cmds.objExists(f"joint_{i}") for i in range(1, 10))
            controles_existen = all(cmds.objExists(f"ctrl_joint_{i}") for i in range(1, 10))
            
            if rig_existe and joints_existen and controles_existen:
                mensaje += "\n✅ RIG: Completo y funcional\n"
                mensaje += f"   • 9 joints: {'✅' if joints_existen else '❌'}\n"
                mensaje += f"   • 9 controles: {'✅' if controles_existen else '❌'}\n"
                mensaje += f"   • Grupo principal: {'✅' if rig_existe else '❌'}\n"
            else:
                mensaje += "\n❌ RIG: Incompleto o no existe\n"
                if not joints_existen:
                    mensaje += "   • Faltan joints\n"
                if not controles_existen:
                    mensaje += "   • Faltan controles\n"
                if not rig_existe:
                    mensaje += "   • No existe grupo principal\n"
            
            # Recomendaciones
            if len(ruedas) < 4:
                mensaje += f"\n⚠️ Se recomiendan 4 ruedas (encontradas: {len(ruedas)})"
            
            if not chasis:
                mensaje += f"\n⚠️ Crear carro con EMERGER antes de crear rig"
            
            cmds.confirmDialog(title="Diagnóstico de Escena", message=mensaje, button=["OK"])
            
        except Exception as e:
            cmds.confirmDialog(title="Error", message=f"❌ Error verificando escena: {str(e)}", button=["OK"])
    
    def show_ui(self):
        """Mostrar la interfaz de usuario"""
        self.ui_controller.mostrar_interfaz_principal()

# Instancia global del coordinador
rig_coordinator = None

def inicializar_sistema():
    """Inicializar el sistema completo"""
    global rig_coordinator
    rig_coordinator = CarroRigCoordinator()
    print("🧠 Sistema Rig Carro inicializado")
    return rig_coordinator

def mostrar_interfaz_principal():
    """Mostrar interfaz principal"""
    global rig_coordinator
    if rig_coordinator is None:
        rig_coordinator = inicializar_sistema()
    
    rig_coordinator.show_ui()
    return rig_coordinator

# Comandos rápidos
def crear_rig_rapido():
    """Comando rápido para crear rig"""
    coordinator = inicializar_sistema()
    coordinator._crear_rig_desde_ui()

def ajustar_rig_rapido():
    """Comando rápido para ajustar rig"""
    coordinator = inicializar_sistema()
    coordinator._ajustar_rig_desde_ui()

def limpiar_rig_rapido():
    """Comando rápido para limpiar rig"""
    coordinator = inicializar_sistema()
    coordinator._limpiar_rig_desde_ui()

# Ejecución directa
if __name__ == "__main__":
    mostrar_interfaz_principal()