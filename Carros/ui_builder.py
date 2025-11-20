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
        self.main_app = main_app  # Puede ser None si se ejecuta solo
        
        # ✅ AGREGAR EXTRUSION CONTROLLER
        self.extrusion_controller = self._crear_extrusion_controller_seguro()
    
    def _crear_extrusion_controller_seguro(self):
        """Crear ExtrusionController de forma segura sin importaciones circulares"""
        try:
            # Intentar importar dinámicamente
            from ExtrusionController import ExtrusionController
            return ExtrusionController()
        except ImportError as e:
            print(f"⚠️ No se pudo crear ExtrusionController: {e}")
            # Crear un objeto dummy que no cause errores
            class DummyExtrusionController:
                def aplicar_extrusion_automatica(self, *args, **kwargs):
                    print("⚠️ ExtrusionController no disponible en modo standalone")
                    return True  # Retornar True para evitar errores
            return DummyExtrusionController()

    def _emerger_carro_desde_ui(self, *args):
        """Función que se llama desde el botón EMERGER en la UI"""
        try:
            if self.main_app is not None:
                # Si tenemos main_app, usar su método
                self.main_app.emerger_carro()
            else:
                # Si no hay main_app (ejecución independiente), usar el sistema local
                self._emerger_carro_local()
                
            show_message("✅ Carro emergido exitosamente!")
            
        except Exception as e:
            show_message(f"❌ Error al emerger carro: {str(e)}", success=False)
            traceback.print_exc()

    def _emerger_carro_local(self):
        """Sistema EMERGER local para cuando se ejecuta ui_builder solo"""
        try:
            # Verificar si ya existe un carro
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
        # Generar dimensiones aleatorias para el chasis
        dimensiones = self.chasis_controller.generar_dimensiones_aleatorias()
        
        # Crear chasis
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
        
        # ✅✅✅ EJECUTAR EXTRUSIÓN AUTOMÁTICA EN LAS 4 RUEDAS Y CHASIS
        print("🎯 EJECUTANDO EXTRUSIÓN AUTOMÁTICA...")
        resultado_extrusion = self.extrusion_controller.aplicar_extrusion_automatica(
            ruedas_controller=self.ruedas_controller
        )
        
        if resultado_extrusion:
            print("✅✅✅ EXTRUSIÓN AUTOMÁTICA APLICADA A LAS 4 RUEDAS")
        else:
            print("⚠️ Algunas extrusiones fallaron")
        
        # CREAR JERARQUÍA DESDE UI_BUILDER
        self._recrear_jerarquia_desde_ui()
        
        # Actualizar UI
        self._actualizar_ui_despues_emerger_local()

    def _transformar_carro_existente_local(self):
        """Transformar el carro existente con nuevos parámetros aleatorios (versión local)"""
        # 🔓 DESPARENTEAR TEMPORALMENTE
        self._desparentear_temporalmente_desde_ui()
        
        # Regenerar dimensiones del chasis
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

        # ✅✅✅ EJECUTAR EXTRUSIÓN AUTOMÁTICA EN LAS 4 RUEDAS Y CHASIS
        print("🎯 EJECUTANDO EXTRUSIÓN AUTOMÁTICA...")
        resultado_extrusion = self.extrusion_controller.aplicar_extrusion_automatica(
            ruedas_controller=self.ruedas_controller
        )
        
        if resultado_extrusion:
            print("✅✅✅ EXTRUSIÓN AUTOMÁTICA APLICADA A LAS 4 RUEDAS")
        else:
            print("⚠️ Algunas extrusiones fallaron")

        # 🔗 RECREAR JERARQUÍA DESPUÉS DE TRANSFORMAR
        self._recrear_jerarquia_desde_ui()

    def _desparentear_temporalmente_desde_ui(self):
        """Desparentear temporalmente desde UI Builder"""
        try:
            print("🔓 DESPARENTEANDO TEMPORALMENTE DESDE UI...")
            
            objetos_a_desparentear = [
                "rueda_delantera_izq", "rueda_delantera_der",
                "rueda_trasera_izq", "rueda_trasera_der", 
                "eje_delantero", "eje_trasero"
            ]
            
            for obj in objetos_a_desparentear:
                if cmds.objExists(obj):
                    parent_actual = cmds.listRelatives(obj, parent=True)
                    if parent_actual:
                        cmds.parent(obj, world=True)
            
            print("✅ DESPARENTEO TEMPORAL COMPLETADO DESDE UI")
            
        except Exception as e:
            print(f"⚠️ Error en desparenteo temporal desde UI: {e}")

    def _recrear_jerarquia_desde_ui(self):
        """Recrear jerarquía desde UI Builder"""
        try:
            print("🔗 RECREANDO JERARQUÍA DESDE UI...")
            
            # 1. PARENTEAR RUEDAS DELANTERAS AL EJE DELANTERO
            if cmds.objExists("rueda_delantera_izq") and cmds.objExists("rueda_delantera_der") and cmds.objExists("eje_delantero"):
                cmds.select(clear=True)
                cmds.select("rueda_delantera_izq", replace=True)
                cmds.select("rueda_delantera_der", add=True)
                cmds.select("eje_delantero", add=True)
                cmds.parent()
            
            # 2. PARENTEAR RUEDAS TRASERAS AL EJE TRASERO
            if cmds.objExists("rueda_trasera_izq") and cmds.objExists("rueda_trasera_der") and cmds.objExists("eje_trasero"):
                cmds.select(clear=True)
                cmds.select("rueda_trasera_izq", replace=True)
                cmds.select("rueda_trasera_der", add=True)
                cmds.select("eje_trasero", add=True)
                cmds.parent()
            
            # 3. PARENTEAR EJES AL CHASIS
            if cmds.objExists("eje_delantero") and cmds.objExists("eje_trasero") and cmds.objExists("axioma_carro"):
                cmds.select(clear=True)
                cmds.select("eje_delantero", replace=True)
                cmds.select("eje_trasero", add=True)
                cmds.select("axioma_carro", add=True)
                cmds.parent()
            
            print("✅ JERARQUÍA RECREADA DESDE UI")
            
        except Exception as e:
            print(f"⚠️ Error recreando jerarquía desde UI: {e}")

    def _actualizar_ui_despues_emerger_local(self):
        """Actualizar la UI después de emerger un carro (versión local)"""
        # Actualizar labels de extrusiones
        for tipo in self.extrusion_manager.configuracion.keys():
            if tipo in self.extrusion_manager.extrusion_nodes:
                thickness_actual = self.extrusion_manager.obtener_thickness_actual(tipo)
                self.actualizar_label_extrusion(tipo, thickness_actual)
        
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

    # Funciones de selección
    def _seleccionar_par_12_13(self, *args):
        try:
            self.vertex_controller.seleccionar_par_12_13()
            show_message("✅ Par 12-13 seleccionado")
        except Exception as e:
            show_message(f"❌ Error seleccionando par 12-13: {str(e)}", success=False)

    def _seleccionar_par_14_15(self, *args):
        try:
            self.vertex_controller.seleccionar_par_14_15()
            show_message("✅ Par 14-15 seleccionado")
        except Exception as e:
            show_message(f"❌ Error seleccionando par 14-15: {str(e)}", success=False)

    def _seleccionar_grupo_9_10(self, *args):
        try:
            self.vertex_controller.seleccionar_grupo_9_10()
            show_message("✅ Grupo 9-10 seleccionado")
        except Exception as e:
            show_message(f"❌ Error seleccionando grupo 9-10: {str(e)}", success=False)

    def _seleccionar_grupo_17_18(self, *args):
        try:
            self.vertex_controller.seleccionar_grupo_17_18()
            show_message("✅ Grupo 17-18 seleccionado")
        except Exception as e:
            show_message(f"❌ Error seleccionando grupo 17-18: {str(e)}", success=False)

    def _seleccionar_par_16_17(self, *args):
        try:
            self.vertex_controller.seleccionar_par_16_17()
            show_message("✅ Par 16-17 seleccionado")
        except Exception as e:
            show_message(f"❌ Error seleccionando par 16-17: {str(e)}", success=False)

    def _seleccionar_par_10_11(self, *args):
        try:
            self.vertex_controller.seleccionar_par_10_11()
            show_message("✅ Par 10-11 seleccionado")
        except Exception as e:
            show_message(f"❌ Error seleccionando par 10-11: {str(e)}", success=False)

    def actualizar_sliders_vertices(self, desplazamientos):
        """Actualizar los sliders de vértices en la UI con los valores actuales"""
        try:
            # Actualizar cada slider con sus valores correspondientes
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

    # ===== MÉTODOS DE EXTRUSIÓN =====

    def _aumentar_thickness(self, tipo):
        """Aumenta el thickness de una extrusión"""
        try:
            nuevo_thickness = self.extrusion_manager.aumentar_thickness(tipo)
            if nuevo_thickness is not None:
                self.actualizar_label_extrusion(tipo, nuevo_thickness)
                show_message(f"📈 {tipo.upper()} thickness aumentado a: {nuevo_thickness:.1f}")
            else:
                show_message(f"⚠️ Primero crea el {tipo} con EMERGER", success=False)
                
        except Exception as e:
            show_message(f"❌ Error al aumentar {tipo}: {str(e)}", success=False)

    def _disminuir_thickness(self, tipo):
        """Disminuye el thickness de una extrusión"""
        try:
            nuevo_thickness = self.extrusion_manager.disminuir_thickness(tipo)
            if nuevo_thickness is not None:
                self.actualizar_label_extrusion(tipo, nuevo_thickness)
                show_message(f"📉 {tipo.upper()} thickness disminuido a: {nuevo_thickness:.1f}")
            else:
                show_message(f"⚠️ Primero crea el {tipo} con EMERGER", success=False)
                
        except Exception as e:
            show_message(f"❌ Error al disminuir {tipo}: {str(e)}", success=False)

    def actualizar_label_extrusion(self, tipo, thickness):
        """Actualizar label de thickness de extrusión en UI"""
        label_key = f'{tipo}_thickness_label'
        if cmds.text(label_key, exists=True):
            cmds.text(label_key, edit=True, label=f'Thickness: {thickness:.1f}')

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
            cmds.text("ruedas_altura_label", edit=True, label=f'Altura: {altura:.1f}')

    def _posicionar_ruedas_delanteras(self, *args):
        """Posiciona las ruedas delanteras"""
        try:
            self.ruedas_controller.posicionar_ruedas(self.chasis_controller, "delanteras")
            show_message("✅ Ruedas delanteras reposicionadas")
        except Exception as e:
            show_message(f"❌ Error al posicionar ruedas delanteras: {str(e)}", success=False)

    def _posicionar_ruedas_traseras(self, *args):
        """Posiciona las ruedas traseras"""
        try:
            self.ruedas_controller.posicionar_ruedas(self.chasis_controller, "traseras")
            show_message("✅ Ruedas traseras reposicionadas")
        except Exception as e:
            show_message(f"❌ Error al posicionar ruedas traseras: {str(e)}", success=False)

    def _posicionar_todas_ruedas(self, *args):
        """Posiciona todas las ruedas"""
        try:
            self.ruedas_controller.posicionar_ruedas(self.chasis_controller, "todas")
            show_message("✅ Todas las ruedas reposicionadas")
        except Exception as e:
            show_message(f"❌ Error al posicionar ruedas: {str(e)}", success=False)

    # ===== MÉTODOS DE UTILIDAD =====

    def limpiar_escena(self, *args):
        """Limpia todos los chasis y ruedas de la escena"""
        try:
            # Limpiar mediante controladores
            self.ruedas_controller.limpiar_ruedas()
            self.extrusion_manager.limpiar_extrusiones()
            self.chasis_controller.limpiar_chasis()
            
            # Limpiar objetos residuales
            objetos_limpiar = cmds.ls(["axioma_*", "rueda_*"], transforms=True)
            if objetos_limpiar:
                cmds.delete(objetos_limpiar)
            
            # Resetear labels a valores por defecto
            self._resetear_labels()
            
            show_message("🧹 Escena limpiada - Listo para nuevo axioma")
            
        except Exception as e:
            show_message(f"❌ Error al limpiar escena: {str(e)}", success=False)

    def _resetear_labels(self):
        """Resetear todos los labels a valores por defecto"""
        # Resetear labels de extrusiones
        for tipo in self.extrusion_manager.configuracion.keys():
            default_thickness = self.extrusion_manager.configuracion[tipo]['thickness_default']
            self.actualizar_label_extrusion(tipo, default_thickness)
        
        # Resetear label de ruedas
        self.actualizar_label_ruedas(self.ruedas_controller.altura_default)

    # ===== INTERFAZ DE USUARIO =====

    def build_ui(self, parent=None):
        """Construir la interfaz de usuario simplificada - SISTEMA EMERGER"""
        created_window = False
        
        # Si no hay parent, crear ventana independiente
        if parent is None:
            if cmds.window(self.window_name, exists=True):
                cmds.deleteUI(self.window_name)
            win = cmds.window(self.window_name, title="🚗 Axioma Carro - Sistema Emerger", w=400, h=700, sizeable=True)
            main_layout = cmds.columnLayout(adjustableColumn=True)
            created_window = True
        else:
            # Usar el parent proporcionado directamente
            main_layout = parent

        # ===== ENCABEZADO PRINCIPAL =====
        cmds.text(label="🎲 SISTEMA EMERGER AXIOMA", height=30, 
                 align="center", backgroundColor=(0.2, 0.3, 0.6), parent=main_layout)
        cmds.separator(height=10, parent=main_layout)
        
        cmds.text(label="💡 Click EMERGER para crear o transformar el carro", 
                 align="center", wordWrap=True, parent=main_layout)
        cmds.separator(height=15, parent=main_layout)
        
        # ===== BOTÓN PRINCIPAL EMERGER =====
        cmds.button(
            label='🎯 EMERGER CARRO',
            command=self._emerger_carro_desde_ui,
            backgroundColor=(0.9, 0.6, 0.1),
            height=50,
            parent=main_layout
        )
        
        cmds.separator(height=15, parent=main_layout)
        
        # ===== CONTROL DE VÉRTICES =====
        cmds.frameLayout(label="🔧 Control de Vértices", collapsable=True, collapse=False, parent=main_layout)
        cmds.columnLayout(adjustableColumn=True, parent=main_layout)
        
        # Pares en Y (12-13 y 14-15)
        cmds.frameLayout(label="Pares en Y - Individuales", collapsable=True, parent=main_layout)
        cmds.columnLayout(adjustableColumn=True)
        
        cmds.text("Par 12-13:", align="left", parent=main_layout)
        cmds.floatSliderGrp('slider_par_12_13_y', label="Desplazamiento Y", minValue=-0.5, maxValue=0.5, field=True, value=0.0, changeCommand=self._mover_par_12_13_y)
        cmds.button(label="Seleccionar Par 12-13", command=self._seleccionar_par_12_13, backgroundColor=(0.2, 0.5, 0.8))
        cmds.separator(height=5, parent=main_layout)
        
        cmds.text("Par 14-15:", align="left", parent=main_layout)
        cmds.floatSliderGrp('slider_par_14_15_y', label="Desplazamiento Y", minValue=-0.5, maxValue=0.5, field=True, value=0.0, changeCommand=self._mover_par_14_15_y)
        cmds.button(label="Seleccionar Par 14-15", command=self._seleccionar_par_14_15, backgroundColor=(0.3, 0.6, 0.3))
        
        cmds.setParent('..')
        cmds.setParent('..')
        
        # Grupos en X con espejo
        cmds.frameLayout(label="Grupos en X con Espejo", collapsable=True, parent=main_layout)
        cmds.columnLayout(adjustableColumn=True)
        
        cmds.text("Grupo 9-10 (Reflejo 8,11):", align="left", parent=main_layout)
        cmds.floatSliderGrp('slider_grupo_9_10_x', label="Desplazamiento X", minValue=-0.8, maxValue=0.8, field=True, value=0.0, changeCommand=self._mover_grupo_9_10_x)
        cmds.button(label="Seleccionar Grupo 9-10", command=self._seleccionar_grupo_9_10, backgroundColor=(0.8, 0.5, 0.2))
        cmds.separator(height=5, parent=main_layout)
        
        cmds.text("Grupo 17-18 (Reflejo 16,19):", align="left", parent=main_layout)
        cmds.floatSliderGrp('slider_grupo_17_18_x', label="Desplazamiento X", minValue=-0.8, maxValue=0.8, field=True, value=0.0, changeCommand=self._mover_grupo_17_18_x)
        cmds.button(label="Seleccionar Grupo 17-18", command=self._seleccionar_grupo_17_18, backgroundColor=(0.7, 0.3, 0.3))
        
        cmds.setParent('..')
        cmds.setParent('..')
        
        # Pares individuales en Y (16-17 y 10-11)
        cmds.frameLayout(label="Pares Individuales en Y", collapsable=True, parent=main_layout)
        cmds.columnLayout(adjustableColumn=True)
        
        cmds.text("Par 16-17:", align="left", parent=main_layout)
        cmds.floatSliderGrp('slider_par_16_17_y', label="Desplazamiento Y", minValue=-0.3, maxValue=0.3, field=True, value=0.0, changeCommand=self._mover_par_16_17_y)
        cmds.button(label="Seleccionar Par 16-17", command=self._seleccionar_par_16_17, backgroundColor=(0.5, 0.3, 0.7))
        cmds.separator(height=5, parent=main_layout)
        
        cmds.text("Par 10-11:", align="left", parent=main_layout)
        cmds.floatSliderGrp('slider_par_10_11_y', label="Desplazamiento Y", minValue=-0.3, maxValue=0.3, field=True, value=0.0, changeCommand=self._mover_par_10_11_y)
        cmds.button(label="Seleccionar Par 10-11", command=self._seleccionar_par_10_11, backgroundColor=(0.3, 0.7, 0.5))
        
        cmds.setParent('..')
        cmds.setParent('..')
        
        # Botón reset vértices
        cmds.button(label="🔄 Resetear Todos los Vértices", command=self._resetear_vertices, backgroundColor=(0.7, 0.3, 0.3))
        
        cmds.setParent('..')
        cmds.setParent('..')
        
        cmds.separator(height=10, parent=main_layout)
        
        # ===== CONTROL DE EXTRUSIONES =====
        cmds.frameLayout(label="🎨 Control de Extrusiones", collapsable=True, parent=main_layout)
        cmds.columnLayout(adjustableColumn=True, parent=main_layout)
        
        # Configuración de extrusiones
        extrusiones_config = [
            ('capo', '🚗 CAPÓ FRONTAL', (0.2, 0.5, 0.8)),
            ('techo', '🚙 TECHO', (0.8, 0.6, 0.2)),
            ('maletero', '🚛 MALETERO', (0.7, 0.3, 0.3))
        ]
        
        for tipo, label, color in extrusiones_config:
            cmds.text(label, align="left", backgroundColor=color, parent=main_layout)
            layout = cmds.rowLayout(
                numberOfColumns=4,
                columnWidth4=(60, 60, 60, 120),
                adjustableColumn=4,
                parent=main_layout
            )
            
            cmds.button(label='+', 
                       command=lambda x, t=tipo: self._aumentar_thickness(t),
                       backgroundColor=(0.3, 0.7, 0.3),
                       parent=layout)
            cmds.button(label='-', 
                       command=lambda x, t=tipo: self._disminuir_thickness(t),
                       backgroundColor=(0.8, 0.3, 0.3),
                       parent=layout)
            
            # Crear label para mostrar thickness actual
            default_thickness = self.extrusion_manager.configuracion[tipo]['thickness_default']
            cmds.text(f'{tipo}_thickness_label', 
                     label=f'Thickness: {default_thickness:.1f}', 
                     align="center",
                     width=120,
                     parent=layout)
            
            cmds.setParent('..')
            cmds.separator(height=5, parent=main_layout)
        
        cmds.setParent('..')
        cmds.setParent('..')
        
        # ===== CONTROL DE RUEDAS =====
        cmds.frameLayout(label="🎯 Control de Ruedas", collapsable=True, parent=main_layout)
        cmds.columnLayout(adjustableColumn=True, parent=main_layout)


        
        # Control de altura
        cmds.text("Altura de Ruedas:", align="left", parent=main_layout)
        layout_altura = cmds.rowLayout(
            numberOfColumns=4,
            columnWidth4=(60, 60, 60, 120),
            adjustableColumn=4,
            parent=main_layout
        )
        
        cmds.button(label='+', 
                   command=self._aumentar_altura_ruedas,
                   backgroundColor=(0.3, 0.7, 0.3),
                   parent=layout_altura)
        cmds.button(label='-', 
                   command=self._disminuir_altura_ruedas,
                   backgroundColor=(0.8, 0.3, 0.3),
                   parent=layout_altura)
        
        cmds.text("ruedas_altura_label", 
                 label='Altura: 1.0', 
                 align="center",
                 width=120,
                 parent=layout_altura)
        
        cmds.setParent('..')
        cmds.separator(height=8, parent=main_layout)
        
        # Botones de posicionamiento
        cmds.text("Reposicionar Ruedas:", align="left", parent=main_layout)
        layout_posicion = cmds.rowLayout(
            numberOfColumns=3,
            columnWidth3=(130, 130, 130),
            adjustableColumn=3,
            parent=main_layout
        )
        
        cmds.button(label='Delanteras', 
                   command=self._posicionar_ruedas_delanteras,
                   backgroundColor=(0.2, 0.5, 0.8),
                   parent=layout_posicion)
        cmds.button(label='Traseras', 
                   command=self._posicionar_ruedas_traseras,
                   backgroundColor=(0.8, 0.5, 0.2),
                   parent=layout_posicion)
        cmds.button(label='Todas', 
                   command=self._posicionar_todas_ruedas,
                   backgroundColor=(0.3, 0.6, 0.3),
                   parent=layout_posicion)
        
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        
        # ===== BOTONES DE UTILIDAD =====
        cmds.separator(height=15, parent=main_layout)
        
        buttons_layout = cmds.rowLayout(
            numberOfColumns=2,
            columnWidth2=(195, 195),
            adjustableColumn=2,
            parent=main_layout
        )
        
        cmds.button(
            label='🧹 Limpiar Escena',
            command=self.limpiar_escena,
            backgroundColor=(0.8, 0.2, 0.2),
            parent=buttons_layout
        )
        
        cmds.button(
            label='❌ Cerrar',
            command=lambda x: cmds.deleteUI(self.window_name) if cmds.window(self.window_name, exists=True) else None,
            backgroundColor=(0.4, 0.4, 0.4),
            parent=buttons_layout
        )
        
        cmds.setParent('..')
        
        # Información del sistema
        cmds.separator(height=10, parent=main_layout)
        cmds.text(label="🎲 Cada click en EMERGER genera un carro único", 
                 align="center", parent=main_layout)
        cmds.text(label="📏 Dimensiones y formas dentro de rangos controlados", 
                 align="center", parent=main_layout)

        if created_window:
            cmds.showWindow(win)

    def mostrar_ventana(self):
        """Mostrar la ventana de la UI"""
        self.build_ui()

# ✅ NUEVA VERSIÓN SEGURA:
def open_chasis_ui():
    """Abrir la interfaz de Axioma Carro - Sistema Emerger"""
    try:
        # Importar dinámicamente para evitar importaciones circulares
        from chasis_controller import ChasisController
        from ruedas_controller import RuedasController
        from extrusion_manager import ExtrusionManager
        from VertexController import VertexController
        
        # Crear controladores temporales
        chasis_controller = ChasisController()
        ruedas_controller = RuedasController()
        extrusion_manager = ExtrusionManager()
        vertex_controller = VertexController()
        
        # Crear UI
        ui_builder = UIBuilder("chasis_con_ruedas_ui", chasis_controller, ruedas_controller, extrusion_manager, vertex_controller, None)
        ui_builder.mostrar_ventana()
        
    except ImportError as e:
        cmds.warning(f"❌ Error importando controladores: {e}")
        cmds.confirmDialog(title="Error", message=f"No se pudieron cargar los controladores:\n{e}", button=["OK"])
    

if __name__ == "__main__":
    open_chasis_ui()


