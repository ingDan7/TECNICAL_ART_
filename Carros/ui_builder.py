import maya.cmds as cmds
import traceback

print("🔧 ui_builder.py CARGADO - Sistema Emerger Axioma")

# Variable para verificar que este archivo se está ejecutando
CURRENT_VERSION = "3.0.0"
print(f"🚗 Axioma Carro v{CURRENT_VERSION} - Sistema Emerger activo")

def show_message(msg, success=True):
    """Mostrar mensaje en pantalla"""
    color = (0.2, 0.8, 0.2) if success else (0.9, 0.5, 0.2)
    cmds.inViewMessage(amg=f"<hl>{msg}</hl>", pos='midCenter', fade=True, fadeStayTime=1500, backColor=color, fadeOutTime=1000)

class UIBuilder:
    def __init__(self, window_name, chasis_controller, ruedas_controller, extrusion_manager, vertex_controller, main_app):
        self.window_name = window_name
        self.chasis_controller = chasis_controller
        self.ruedas_controller = ruedas_controller
        self.extrusion_manager = extrusion_manager
        self.vertex_controller = vertex_controller
        self.main_app = main_app
        
        # ✅ AGREGAR EXTRUSION CONTROLLER
        self.extrusion_controller = self._crear_extrusion_controller_seguro()
    
    def _crear_extrusion_controller_seguro(self):
        """Crear ExtrusionController de forma segura sin importaciones circulares"""
        try:
            from ExtrusionController import ExtrusionController
            return ExtrusionController()
        except ImportError as e:
            print(f"⚠️ No se pudo crear ExtrusionController: {e}")
            class DummyExtrusionController:
                def aplicar_extrusion_automatica(self, *args, **kwargs):
                    print("⚠️ ExtrusionController no disponible en modo standalone")
                    return True
            return DummyExtrusionController()

    def _emerger_carro_desde_ui(self, *args):
        """Función que se llama desde el botón EMERGER en la UI"""
        try:
            if self.main_app is not None:
                self.main_app.emerger_carro()
            else:
                self._emerger_carro_local()
                
            show_message("✅ Carro emergido exitosamente!")
            
        except Exception as e:
            show_message(f"❌ Error al emerger carro: {str(e)}", success=False)
            traceback.print_exc()

    def _emerger_carro_local(self):
        """Sistema EMERGER local para cuando se ejecuta ui_builder solo"""
        try:
            carro_existente = self._verificar_carro_existente_local()
            
            if carro_existente:
                print("🔄 Transformando carro existente...")
                self._transformar_carro_existente_local()
            else:
                print("🎯 Creando primer carro...")
                self._crear_primer_carro_local()
                
        except Exception as e:
            show_message(f"❌ Error al emerger carro: {str(e)}", success=False)
            traceback.print_exc()

    def _verificar_carro_existente_local(self):
        """Verificar si ya existe un carro en escena (versión local)"""
        return (self.chasis_controller.cubo_actual is not None and 
                cmds.objExists(self.chasis_controller.cubo_actual))

    def _crear_primer_carro_local(self):
        """Crear el primer carro con parámetros aleatorios (versión local)"""
        dimensiones = self.chasis_controller.generar_dimensiones_aleatorias()
        
        chasis = self.chasis_controller.crear_cubo_base(
            "axioma_carro", 
            dimensiones['ancho'], 
            dimensiones['alto'], 
            dimensiones['largo']
        )
        
        if not chasis:
            return
        
        # APLICAR DESPLAZAMIENTOS ALEATORIOS A VÉRTICES
        print("🎲 APLICANDO DESPLAZAMIENTOS ALEATORIOS A VÉRTICES...")
        desplazamientos = self.vertex_controller.aplicar_desplazamientos_aleatorios()
        if desplazamientos:
            print("✅ Vértices modificados aleatoriamente")
            self.actualizar_sliders_vertices(desplazamientos)
        
        # Crear extrusiones con valores aleatorios
        for tipo in self.extrusion_manager.configuracion.keys():
            thickness_aleatorio = self.extrusion_manager.generar_thickness_aleatorio(tipo)
            self.extrusion_manager.crear_extrusion(chasis, tipo, thickness_aleatorio)
        
        # Crear y posicionar ruedas con valores aleatorios
        tamaño_ruedas = self.ruedas_controller.generar_tamanio_aleatorio()
        self.ruedas_controller.crear_ruedas(
            tamaño_ruedas['altura'], 
            tamaño_ruedas['radio']
        )

        self.ruedas_controller.posicionar_ruedas(self.chasis_controller, "todas")
        
        # Ejecutar extrusión automática
        print("🎯 EJECUTANDO EXTRUSIÓN AUTOMÁTICA...")
        resultado_extrusion = self.extrusion_controller.aplicar_extrusion_automatica(
            ruedas_controller=self.ruedas_controller
        )
        
        if resultado_extrusion:
            print("✅✅✅ EXTRUSIÓN AUTOMÁTICA APLICADA A LAS 4 RUEDAS")
        else:
            print("⚠️ Algunas extrusiones fallaron")
        
        self._actualizar_ui_despues_emerger_local()

    def _transformar_carro_existente_local(self):
        """Transformar el carro existente con nuevos parámetros aleatorios (versión local)"""
        dimensiones = self.chasis_controller.generar_dimensiones_aleatorias()
        self.chasis_controller.transformar_chasis_existente(
            dimensiones['ancho'], 
            dimensiones['alto'], 
            dimensiones['largo']
        )
        
        # APLICAR DESPLAZAMIENTOS ALEATORIOS A VÉRTICES
        print("🎲 APLICANDO DESPLAZAMIENTOS ALEATORIOS A VÉRTICES...")
        desplazamientos = self.vertex_controller.aplicar_desplazamientos_aleatorios()
        if desplazamientos:
            print("✅ Vértices modificados aleatoriamente")
            self.actualizar_sliders_vertices(desplazamientos)
        
        # Regenerar extrusiones
        for tipo in self.extrusion_manager.configuracion.keys():
            if tipo in self.extrusion_manager.extrusion_nodes:
                thickness_aleatorio = self.extrusion_manager.generar_thickness_aleatorio(tipo)
                self.extrusion_manager.ajustar_thickness(tipo, thickness_aleatorio)
        
        # Regenerar ruedas
        if self.ruedas_controller.ruedas:
            tamaño_ruedas = self.ruedas_controller.generar_tamanio_aleatorio()
            self.ruedas_controller.transformar_ruedas_existentes(
                tamaño_ruedas['altura'], 
                tamaño_ruedas['radio']
            )
            self.ruedas_controller.posicionar_ruedas(self.chasis_controller, "todas")

        # Ejecutar extrusión automática
        print("🎯 EJECUTANDO EXTRUSIÓN AUTOMÁTICA...")
        resultado_extrusion = self.extrusion_controller.aplicar_extrusion_automatica(
            ruedas_controller=self.ruedas_controller
        )
        
        if resultado_extrusion:
            print("✅✅✅ EXTRUSIÓN AUTOMÁTICA APLICADA A LAS 4 RUEDAS")
        else:
            print("⚠️ Algunas extrusiones fallaron")

    def _actualizar_ui_despues_emerger_local(self):
        """Actualizar la UI después de emerger un carro (versión local)"""
        # Actualizar label de ruedas
        if self.ruedas_controller.ruedas:
            altura_actual = self.ruedas_controller.obtener_altura_actual()
            self.actualizar_label_ruedas(altura_actual)

    # ===== FUNCIONES DE CONTROL DE VÉRTICES =====

    def _mover_par_12_13_y(self, *args):
        """Mover par 12-13 en eje Y"""
        try:
            valor = cmds.floatSliderGrp('slider_par_12_13_y', query=True, value=True)
            self.vertex_controller.mover_par_12_13_y(valor)
            show_message(f"✅ Par 12-13 Y movido a: {valor:.2f}")
        except Exception as e:
            show_message(f"❌ Error moviendo par 12-13: {str(e)}", success=False)

    def _mover_par_14_15_y(self, *args):
        """Mover par 14-15 en eje Y"""
        try:
            valor = cmds.floatSliderGrp('slider_par_14_15_y', query=True, value=True)
            self.vertex_controller.mover_par_14_15_y(valor)
            show_message(f"✅ Par 14-15 Y movido a: {valor:.2f}")
        except Exception as e:
            show_message(f"❌ Error moviendo par 14-15: {str(e)}", success=False)

    def _mover_grupo_9_10_x(self, *args):
        """Mover grupo 9-10 en eje X con espejo"""
        try:
            valor = cmds.floatSliderGrp('slider_grupo_9_10_x', query=True, value=True)
            self.vertex_controller.mover_grupo_9_10_x(valor)
            show_message(f"✅ Grupo 9-10 X movido (espejo) a: {valor:.2f}")
        except Exception as e:
            show_message(f"❌ Error moviendo grupo 9-10: {str(e)}", success=False)

    def _mover_grupo_17_18_x(self, *args):
        """Mover grupo 17-18 en eje X con espejo"""
        try:
            valor = cmds.floatSliderGrp('slider_grupo_17_18_x', query=True, value=True)
            self.vertex_controller.mover_grupo_17_18_x(valor)
            show_message(f"✅ Grupo 17-18 X movido (espejo) a: {valor:.2f}")
        except Exception as e:
            show_message(f"❌ Error moviendo grupo 17-18: {str(e)}", success=False)

    def _mover_par_16_17_y(self, *args):
        """Mover par 16-17 en eje Y"""
        try:
            valor = cmds.floatSliderGrp('slider_par_16_17_y', query=True, value=True)
            self.vertex_controller.mover_par_16_17_y(valor)
            show_message(f"✅ Par 16-17 Y movido a: {valor:.2f}")
        except Exception as e:
            show_message(f"❌ Error moviendo par 16-17: {str(e)}", success=False)

    def _mover_par_10_11_y(self, *args):
        """Mover par 10-11 en eje Y"""
        try:
            valor = cmds.floatSliderGrp('slider_par_10_11_y', query=True, value=True)
            self.vertex_controller.mover_par_10_11_y(valor)
            show_message(f"✅ Par 10-11 Y movido a: {valor:.2f}")
        except Exception as e:
            show_message(f"❌ Error moviendo par 10-11: {str(e)}", success=False)

    def _resetear_vertices(self, *args):
        """Resetear todos los vértices"""
        try:
            self.vertex_controller.resetear_todos_vertices()
            # Resetear todos los sliders a 0
            sliders = [
                'slider_par_12_13_y', 'slider_par_14_15_y',
                'slider_grupo_9_10_x', 'slider_grupo_17_18_x', 
                'slider_par_16_17_y', 'slider_par_10_11_y'
            ]
            for slider in sliders:
                if cmds.floatSliderGrp(slider, exists=True):
                    cmds.floatSliderGrp(slider, edit=True, value=0.0)
            show_message("✅ Todos los vértices reseteados")
        except Exception as e:
            show_message(f"❌ Error reseteando vértices: {str(e)}", success=False)

    def actualizar_sliders_vertices(self, desplazamientos):
        """Actualizar los sliders de vértices en la UI con los valores actuales"""
        try:
            sliders_config = [
                ('slider_par_12_13_y', desplazamientos['par_12_13_y']),
                ('slider_par_14_15_y', desplazamientos['par_14_15_y']),
                ('slider_grupo_9_10_x', desplazamientos['grupo_9_10_x']),
                ('slider_grupo_17_18_x', desplazamientos['grupo_17_18_x']),
                ('slider_par_16_17_y', desplazamientos['par_16_17_y']),
                ('slider_par_10_11_y', desplazamientos['par_10_11_y'])
            ]
            
            for slider_name, valor in sliders_config:
                if cmds.floatSliderGrp(slider_name, exists=True):
                    cmds.floatSliderGrp(slider_name, edit=True, value=valor)
                
            print("✅ Sliders de vértices actualizados en la UI")
            
        except Exception as e:
            print(f"⚠️ Error actualizando sliders en UI: {e}")

    # ===== MÉTODOS DE RUEDAS =====

    def _aumentar_altura_ruedas(self, *args):
        """Aumenta la altura de todas las ruedas"""
        try:
            nueva_altura = self.ruedas_controller.aumentar_altura()
            if nueva_altura is not None:
                self.actualizar_label_ruedas(nueva_altura)
                show_message(f"📈 Altura de ruedas aumentada a: {nueva_altura:.1f}")
            else:
                show_message("⚠️ Primero crea las ruedas con EMERGER", success=False)
                
        except Exception as e:
            show_message(f"❌ Error al aumentar altura de ruedas: {str(e)}", success=False)

    def _disminuir_altura_ruedas(self, *args):
        """Disminuye la altura de todas las ruedas"""
        try:
            nueva_altura = self.ruedas_controller.disminuir_altura()
            if nueva_altura is not None:
                self.actualizar_label_ruedas(nueva_altura)
                show_message(f"📉 Altura de ruedas disminuida a: {nueva_altura:.1f}")
            else:
                show_message("⚠️ Primero crea las ruedas con EMERGER", success=False)
                
        except Exception as e:
            show_message(f"❌ Error al disminuir altura de ruedas: {str(e)}", success=False)

    def actualizar_label_ruedas(self, altura):
        """Actualizar label de altura de ruedas en UI"""
        if cmds.text("ruedas_altura_label", exists=True):
            cmds.text("ruedas_altura_label", edit=True, label=f'Altura Actual: {altura:.1f}')

    # ===== MÉTODOS DE UTILIDAD =====

    def limpiar_escena(self, *args):
        """Limpia todos los chasis y ruedas de la escena"""
        try:
            self.ruedas_controller.limpiar_ruedas()
            self.extrusion_manager.limpiar_extrusiones()
            self.chasis_controller.limpiar_chasis()
            
            objetos_limpiar = cmds.ls(["axioma_*", "rueda_*"], transforms=True)
            if objetos_limpiar:
                cmds.delete(objetos_limpiar)
            
            show_message("🧹 Escena limpiada - Listo para nuevo carro")
            
        except Exception as e:
            show_message(f"❌ Error al limpiar escena: {str(e)}", success=False)

    # ===== INTERFAZ SIMPLIFICADA =====

    def build_ui(self, parent=None):
        """Construir la interfaz de usuario - SOLO LO ESENCIAL"""
        created_window = False
        
        # Configuración de ventana
        if parent is None:
            if cmds.window(self.window_name, exists=True):
                cmds.deleteUI(self.window_name)
            win = cmds.window(self.window_name, 
                            title="🚗 GENERADOR DE CARROS AXIOMA", 
                            width=400, 
                            height=600, 
                            sizeable=False)
            main_layout = cmds.columnLayout(adjustableColumn=True)
            created_window = True
        else:
            main_layout = parent

        # ===== ENCABEZADO PRINCIPAL =====
        cmds.text(label="🎲 GENERADOR DE CARROS AXIOMA", height=40, 
                 align="center", backgroundColor=(0.2, 0.3, 0.6), 
                 font="boldLabelFont", parent=main_layout)
        
        cmds.separator(height=10, parent=main_layout)
        
        cmds.text(label="Crea y personaliza carros 3D de forma procedural", 
                 align="center", wordWrap=True, parent=main_layout)
        
        cmds.separator(height=15, parent=main_layout)
        
        # ===== BOTÓN PRINCIPAL EMERGER =====
        cmds.button(
            label='🎯 EMERGER CARRO ALEATORIO',
            command=self._emerger_carro_desde_ui,
            backgroundColor=(0.9, 0.6, 0.1),
            height=50,
            parent=main_layout
        )
        
        cmds.separator(height=20, parent=main_layout)
        
        # ===== CONTROL DE VÉRTICES =====
        cmds.frameLayout(label="🔧 FORMA DEL CHASIS", 
                        collapsable=True, 
                        collapse=False,
                        marginWidth=10,
                        parent=main_layout)
        
        cmds.columnLayout(adjustableColumn=True, parent=main_layout)
        
        # Sliders de vértices
        cmds.text("Ajusta la forma del chasis con los sliders:", 
                 align="center", wordWrap=True, parent=main_layout)
        
        cmds.separator(height=8, parent=main_layout)
        
        cmds.floatSliderGrp('slider_par_12_13_y', 
                          label="Altura Techo Delantero", 
                          minValue=-0.5, maxValue=0.5, 
                          field=True, value=0.0,
                          columnWidth=[(1, 140), (2, 50), (3, 180)],
                          changeCommand=self._mover_par_12_13_y)
        
        cmds.floatSliderGrp('slider_par_14_15_y', 
                          label="Altura Techo Trasero", 
                          minValue=-0.5, maxValue=0.5, 
                          field=True, value=0.0,
                          columnWidth=[(1, 140), (2, 50), (3, 180)],
                          changeCommand=self._mover_par_14_15_y)
        
        cmds.floatSliderGrp('slider_grupo_9_10_x', 
                          label="Ancho Parte Delantera", 
                          minValue=-0.8, maxValue=0.8, 
                          field=True, value=0.0,
                          columnWidth=[(1, 140), (2, 50), (3, 180)],
                          changeCommand=self._mover_grupo_9_10_x)
        
        cmds.floatSliderGrp('slider_grupo_17_18_x', 
                          label="Ancho Parte Trasera", 
                          minValue=-0.8, maxValue=0.8, 
                          field=True, value=0.0,
                          columnWidth=[(1, 140), (2, 50), (3, 180)],
                          changeCommand=self._mover_grupo_17_18_x)
        
        cmds.floatSliderGrp('slider_par_16_17_y', 
                          label="Altura Parachoques Trasero", 
                          minValue=-0.3, maxValue=0.3, 
                          field=True, value=0.0,
                          columnWidth=[(1, 140), (2, 50), (3, 180)],
                          changeCommand=self._mover_par_16_17_y)
        
        cmds.floatSliderGrp('slider_par_10_11_y', 
                          label="Altura Parachoques Delantero", 
                          minValue=-0.3, maxValue=0.3, 
                          field=True, value=0.0,
                          columnWidth=[(1, 140), (2, 50), (3, 180)],
                          changeCommand=self._mover_par_10_11_y)
        
        # Botón reset vértices
        cmds.button(label="🔄 Resetear Forma", 
                   command=self._resetear_vertices, 
                   backgroundColor=(0.7, 0.3, 0.3),
                   height=30,
                   parent=main_layout)
        
        cmds.setParent('..')
        cmds.setParent('..')
        
        cmds.separator(height=15, parent=main_layout)
        
        # ===== CONTROL DE RUEDAS =====
        cmds.frameLayout(label="🎯 CONTROL DE RUEDAS", 
                        collapsable=True, 
                        collapse=False,
                        marginWidth=10,
                        parent=main_layout)
        
        cmds.columnLayout(adjustableColumn=True, parent=main_layout)
        
        cmds.text("Ajusta la altura de las ruedas:", 
                 align="center", wordWrap=True, parent=main_layout)
        
        layout_altura = cmds.rowLayout(
            numberOfColumns=3,
            columnWidth3=(120, 120, 150),
            adjustableColumn=3,
            height=40,
            parent=main_layout
        )
        
        cmds.button(label='AUMENTAR +', 
                   command=self._aumentar_altura_ruedas,
                   backgroundColor=(0.3, 0.7, 0.3),
                   parent=layout_altura)
        
        cmds.button(label='DISMINUIR -', 
                   command=self._disminuir_altura_ruedas,
                   backgroundColor=(0.8, 0.3, 0.3),
                   parent=layout_altura)
        
        cmds.text("ruedas_altura_label", 
                 label='Altura: 1.0', 
                 align="center",
                 backgroundColor=(0.4, 0.5, 0.6),
                 parent=layout_altura)
        
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        
        cmds.separator(height=20, parent=main_layout)
        
        # ===== BOTÓN DE LIMPIEZA =====
        cmds.button(
            label='🧹 LIMPIAR ESCENA',
            command=self.limpiar_escena,
            backgroundColor=(0.8, 0.2, 0.2),
            height=40,
            parent=main_layout
        )
        
        cmds.separator(height=10, parent=main_layout)
        
        # Información del sistema
        cmds.text(label=f"Versión {CURRENT_VERSION}", 
                 align="center", 
                 parent=main_layout)

        if created_window:
            cmds.showWindow(win)

    def mostrar_ventana(self):
        """Mostrar la ventana de la UI"""
        self.build_ui()

# Función para abrir la interfaz
def open_chasis_ui():
    """Abrir la interfaz de Axioma Carro"""
    try:
        from chasis_controller import ChasisController
        from ruedas_controller import RuedasController
        from extrusion_manager import ExtrusionManager
        from VertexController import VertexController
        
        chasis_controller = ChasisController()
        ruedas_controller = RuedasController()
        extrusion_manager = ExtrusionManager()
        vertex_controller = VertexController()
        
        ui_builder = UIBuilder("chasis_con_ruedas_ui", chasis_controller, ruedas_controller, extrusion_manager, vertex_controller, None)
        ui_builder.mostrar_ventana()
        
    except ImportError as e:
        cmds.warning(f"❌ Error importando controladores: {e}")
        cmds.confirmDialog(title="Error", message=f"No se pudieron cargar los controladores:\n{e}", button=["OK"])
    

if __name__ == "__main__":
    open_chasis_ui()