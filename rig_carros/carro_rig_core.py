import maya.cmds as cmds
from . import cadena_joints, curvas_control, jerarquia, skinning
from carro_rig_utils import buscar_objetos_escena_filtrado

class CarroRigCore:
    """Núcleo principal del sistema de rig - Maneja limpieza y pipeline completo"""
    
    def __init__(self):
        print("🔧 CarroRigCore inicializado")
        self.joints_deform = {}
        self.joints_driver = {}
        self.controles = {}
        
        # Inicializar módulos
        self.cadenas = cadena_joints.ModuloCadenas(self)
        self.curvas = curvas_control.ModuloCurvas(self)
        self.jerarquia = jerarquia.ModuloJerarquia(self)
        self.skinning = skinning.ModuloSkinning(self)
    
    def limpiar_rig_existente(self):
        """Limpia cualquier rig existente en la escena"""
        print("🗑️ Limpiando rig existente...")
        
        elementos_eliminar = [
            "RIG_CARRO_GRP", "JOINTS_GRP", "CONTROLES_GRP", "ctrl_global_GRP"
        ]
        
        for i in range(1, 12):
            elementos_eliminar.extend([
                f"joint_{i}", f"drv_joint_{i}", 
                f"ctrl_joint_{i}", f"ctrl_joint_{i}_GRP"
            ])
        
        eliminados = 0
        for elemento in elementos_eliminar:
            if cmds.objExists(elemento):
                try:
                    cmds.delete(elemento)
                    eliminados += 1
                except Exception:
                    continue
        
        print(f"✅ {eliminados} elementos eliminados")
        return eliminados
    
    def crear_rig_completo(self, chasis=None, ruedas=None, ejes=None):
        """Función maestra que ejecuta todo el pipeline del rig"""
        print("\n" + "="*60)
        print("🚗 INICIANDO CREACIÓN DE RIG MODULAR")
        print("="*60)
        
        # 1. Limpieza previa
        self.limpiar_rig_existente()
        
        # 2. Buscar objetos si no se proporcionaron
        if chasis is None or ruedas is None:
            chasis, ruedas, ejes = buscar_objetos_escena_filtrado()
        
        if not chasis:
            cmds.confirmDialog(title="Error", message="❌ No se encontró chasis", button=["OK"])
            return False
        
        try:
            # Pipeline de creación
            pasos = [
                ("Cadena de Deformación", self.cadenas.crear_cadena_deformacion, (chasis, ruedas, ejes)),
                ("Cadena de Drivers", self.cadenas.crear_cadena_drivers, ()),
                ("Conexiones Drivers->Deformación", self.cadenas.conectar_drivers_a_deformacion, ()),
                ("Controles", self.curvas.crear_controles, (chasis,)),
                ("Conexiones Controles->Drivers", self.curvas.conectar_controles_a_drivers, ()),
                ("Organización", self.jerarquia.organizar_jerarquia, ()),
                ("Skinning", self.skinning.aplicar_skinning, (chasis, ruedas, ejes))
            ]
            
            for nombre_paso, funcion, argumentos in pasos:
                print(f"\n🔧 Ejecutando: {nombre_paso}...")
                if not funcion(*argumentos):
                    self._manejar_error(nombre_paso)
                    return False
            
            # Éxito
            self._mostrar_exito(chasis, ruedas, ejes)
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR CRÍTICO: {e}")
            import traceback
            traceback.print_exc()
            cmds.confirmDialog(title="Error", message=f"❌ Error: {str(e)}", button=["OK"])
            return False
    
    def _manejar_error(self, paso):
        """Maneja errores del pipeline"""
        error_msg = f"❌ Error en: {paso}"
        print(error_msg)
        cmds.confirmDialog(title="Error", message=error_msg, button=["OK"])
    
    def _mostrar_exito(self, chasis, ruedas, ejes):
        """Muestra reporte de éxito"""
        print("\n" + "="*60)
        print("✅ RIG COMPLETADO EXITOSAMENTE")
        print("="*60)
        
        print(f"""
📊 RESUMEN:
  • Joints Deformación: {len(self.joints_deform)}
  • Joints Drivers: {len(self.joints_driver)}  
  • Controles: {len(self.controles)}
  • Geometría: {chasis} + {len(ruedas)} ruedas + {len(ejes)} ejes
        """)
        
        cmds.confirmDialog(
            title="Éxito", 
            message="✅ Rig creado exitosamente\n\n"
                    "🦴 Joints de deformación\n"
                    "🎮 Drivers\n" 
                    "🎨 Controles de animación", 
            button=["OK"]
        )


# Funciones globales para compatibilidad
def crear_rig_carro():
    """Función global para crear rig"""
    core = CarroRigCore()
    return core.crear_rig_completo()

def limpiar_rig_existente():
    """Función global para limpiar rig"""
    core = CarroRigCore()
    return core.limpiar_rig_existente()