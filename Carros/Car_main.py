import maya.cmds as cmds
import random
from ui_builder import UIBuilder
from chasis_controller import ChasisController
from ruedas_controller import RuedasController
from extrusion_manager import ExtrusionManager
from VertexController import VertexController 
from ExtrusionController import ExtrusionController

class ChasisConRuedas:
    def __init__(self):
        self.window_name = "chasis_con_ruedas_ui"
        
        # Inicializar controladores
        self.chasis_controller = ChasisController()
        self.ruedas_controller = RuedasController()
        self.extrusion_manager = ExtrusionManager()
        self.extrusion_controller = ExtrusionController()
        self.vertex_controller = VertexController()
        
        # Construir UI
        self.ui_builder = UIBuilder(
            self.window_name,
            self.chasis_controller,
            self.ruedas_controller,
            self.extrusion_manager,
            self.vertex_controller,
            self  # Pasar referencia para callbacks
        )
        
        # Conectar eventos
        self._conectar_eventos()
    
    def _conectar_eventos(self):
        """Conectar callbacks entre componentes"""
        self.extrusion_manager.on_extrusion_creada = self._actualizar_ui_extrusion
        self.ruedas_controller.on_ruedas_creadas = self._actualizar_ui_ruedas
    
    def _actualizar_ui_extrusion(self, tipo, thickness):
        """Callback para actualizar UI cuando se crea una extrusión"""
        self.ui_builder.actualizar_label_extrusion(tipo, thickness)
    
    def _actualizar_ui_ruedas(self, altura):
        """Callback para actualizar UI cuando se crean ruedas"""
        self.ui_builder.actualizar_label_ruedas(altura)

    def actualizar_sliders_vertices(self, desplazamientos):
        """Actualizar los sliders de vértices en la UI con los valores actuales"""
        try:
            if desplazamientos:
                print(f"✅ Desplazamientos aplicados - Par 12-13 Y: {desplazamientos['par_12_13_y']:.3f}")
                self.ui_builder.actualizar_sliders_vertices(desplazamientos)
                
        except Exception as e:
            print(f"⚠️ No se pudieron actualizar sliders de vértices: {e}")
    
    def emerger_carro(self):
        """Función principal EMERGER - Crear o transformar carro existente"""
        try:
            print("🎲🎲🎲 PRESIONADO EMERGER - INICIANDO...")
            
            # VERIFICAR SI EXISTE CARRO
            carro_existente = self._verificar_carro_existente()
            print(f"🔍 Estado del carro: {'EXISTE' if carro_existente else 'NO EXISTE'}")
            
            # SIEMPRE generar nuevas dimensiones aleatorias
            dimensiones_chasis = self.chasis_controller.generar_dimensiones_aleatorias()
            print(f"📐 NUEVAS DIMENSIONES GENERADAS - Ancho:{dimensiones_chasis['ancho']}, Alto:{dimensiones_chasis['alto']}, Largo:{dimensiones_chasis['largo']}")
            
            if carro_existente:
                print("🔄🔄🔄 TRANSFORMANDO CARRO EXISTENTE...")
                resultado = self._transformar_carro_existente(dimensiones_chasis)
                if resultado:
                    print("✅✅✅ CARRO TRANSFORMADO EXITOSAMENTE")
                else:
                    print("❌❌❌ FALLÓ LA TRANSFORMACIÓN - Creando nuevo carro...")
                    self._crear_nuevo_carro(dimensiones_chasis)
            else:
                print("🎯🎯🎯 CREANDO NUEVO CARRO...")
                self._crear_nuevo_carro(dimensiones_chasis)
                
            print("🎉🎉🎉 PROCESO EMERGER COMPLETADO!")
            
        except Exception as e:
            cmds.warning(f"❌ Error crítico en emerger_carro: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _verificar_carro_existente(self):
        """Verificar si ya existe un carro en escena"""
        carro_en_escena = cmds.objExists("axioma_carro")
        
        if carro_en_escena and not self.chasis_controller.cubo_actual:
            self.chasis_controller.cubo_actual = "axioma_carro"
            print("🔍 Carro encontrado en escena, actualizando referencia del controlador")
        
        return carro_en_escena
    
    def _desparentear_temporalmente(self):
        """Desparentear temporalmente para transformaciones limpias"""
        try:
            print("🔓 DESPARENTEANDO TEMPORALMENTE PARA TRANSFORMACIONES...")
            
            # Lista de objetos a desparentear
            objetos_a_desparentear = [
                "rueda_delantera_izq", "rueda_delantera_der",
                "rueda_trasera_izq", "rueda_trasera_der", 
                "eje_delantero", "eje_trasero"
            ]
            
            for obj in objetos_a_desparentear:
                if cmds.objExists(obj):
                    # Verificar si tiene parent
                    parent_actual = cmds.listRelatives(obj, parent=True)
                    if parent_actual:
                        cmds.parent(obj, world=True)
                        print(f"   🔓 {obj} desparenteado")
            
            print("✅ DESPARENTEO TEMPORAL COMPLETADO")
            return True
            
        except Exception as e:
            print(f"⚠️ Error en desparenteo temporal: {e}")
            return False

    def _recrear_jerarquia(self):
        """Recrear la jerarquía después de las transformaciones"""
        try:
            print("🔗 RECREANDO JERARQUÍA DESPUÉS DE TRANSFORMACIONES...")
            
            # 1. PARENTEAR RUEDAS DELANTERAS AL EJE DELANTERO
            if cmds.objExists("rueda_delantera_izq") and cmds.objExists("rueda_delantera_der") and cmds.objExists("eje_delantero"):
                cmds.select(clear=True)
                cmds.select("rueda_delantera_izq", replace=True)
                cmds.select("rueda_delantera_der", add=True)
                cmds.select("eje_delantero", add=True)
                cmds.parent()
                print("   ✅ Ruedas delanteras -> eje_delantero")
            
            # 2. PARENTEAR RUEDAS TRASERAS AL EJE TRASERO
            if cmds.objExists("rueda_trasera_izq") and cmds.objExists("rueda_trasera_der") and cmds.objExists("eje_trasero"):
                cmds.select(clear=True)
                cmds.select("rueda_trasera_izq", replace=True)
                cmds.select("rueda_trasera_der", add=True)
                cmds.select("eje_trasero", add=True)
                cmds.parent()
                print("   ✅ Ruedas traseras -> eje_trasero")
            
            # 3. PARENTEAR EJES AL CHASIS
            if cmds.objExists("eje_delantero") and cmds.objExists("eje_trasero") and cmds.objExists("axioma_carro"):
                cmds.select(clear=True)
                cmds.select("eje_delantero", replace=True)
                cmds.select("eje_trasero", add=True)
                cmds.select("axioma_carro", add=True)
                cmds.parent()
                print("   ✅ Ejes -> axioma_carro")
            
            print("✅✅✅ JERARQUÍA RECREADA EXITOSAMENTE")
            return True
            
        except Exception as e:
            print(f"❌ Error recreando jerarquía: {e}")
            return False

    def _crear_nuevo_carro(self, dimensiones_chasis):
        print("🏗️ CREANDO CARRO DESDE CERO CON VÉRTICES ALEATORIOS...")
        
        # Crear chasis base
        chasis = self.chasis_controller.crear_cubo_base(
            "axioma_carro", 
            dimensiones_chasis['ancho'], 
            dimensiones_chasis['alto'], 
            dimensiones_chasis['largo']
        )

        if not chasis:
            print("❌❌❌ ERROR CRÍTICO: No se pudo crear el chasis base")
            return False

        # PRESERVAR POSICIONES Y INMEDIATAMENTE después de crear el cubo
        self.vertex_controller.preservar_posiciones_y_originales()
        
        # APLICAR DESPLAZAMIENTOS ALEATORIOS A VÉRTICES
        print("🎲 APLICANDO DESPLAZAMIENTOS ALEATORIOS A VÉRTICES...")
        desplazamientos = self.vertex_controller.aplicar_desplazamientos_aleatorios_avanzados()
        if desplazamientos:
            print("✅ Vértices modificados aleatoriamente")
            self.actualizar_sliders_vertices(desplazamientos)
        
        # Crear extrusiones con valores aleatorios
        for tipo in self.extrusion_manager.configuracion.keys():
            thickness_aleatorio = self.extrusion_manager.generar_thickness_aleatorio(tipo)
            print(f"🏗️ Creando {tipo} con thickness: {thickness_aleatorio}")
            resultado = self.extrusion_manager.crear_extrusion(chasis, tipo, thickness_aleatorio)
            if resultado:
                self._actualizar_ui_extrusion(tipo, thickness_aleatorio)
        
        # CREAR RUEDAS PROPORCIONALES AL CHASIS
        print(f"🎯 Creando ruedas proporcionales al chasis...")
        self.ruedas_controller.crear_ruedas(dimensiones_chasis=dimensiones_chasis)
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
        
        # CREAR JERARQUÍA INICIAL
        self._recrear_jerarquia()
        
        return True

    def _transformar_carro_existente(self, dimensiones_chasis):
        """Transformar el carro existente CON VÉRTICES ALEATORIOS"""
        print("🔄🔄🔄 TRANSFORMACIÓN COMPLETA CON VÉRTICES ALEATORIOS...")
        
        try:
            # 🔓 PASO CRÍTICO: DESPARENTEAR ANTES DE TRANSFORMAR
            self._desparentear_temporalmente()
            
            # 1. TRANSFORMAR CHASIS BASE
            print(f"📏 TRANSFORMANDO CHASIS: {dimensiones_chasis['ancho']}x{dimensiones_chasis['alto']}x{dimensiones_chasis['largo']}")
            resultado_chasis = self.chasis_controller.transformar_chasis_existente(
                dimensiones_chasis['ancho'], 
                dimensiones_chasis['alto'], 
                dimensiones_chasis['largo']
            )
            
            if not resultado_chasis:
                print("❌ FALLÓ LA TRANSFORMACIÓN DEL CHASIS BASE")
                return False
            
            # 2. APLICAR DESPLAZAMIENTOS ALEATORIOS A VÉRTICES
            print("🎲 APLICANDO DESPLAZAMIENTOS ALEATORIOS A VÉRTICES...")
            desplazamientos = self.vertex_controller.aplicar_desplazamientos_aleatorios()
            if desplazamientos:
                print("✅ Vértices modificados aleatoriamente")
                self.actualizar_sliders_vertices(desplazamientos)
            
            # 3. TRANSFORMAR RUEDAS PROPORCIONALMENTE
            if self.ruedas_controller.ruedas:
                print(f"🔄 Transformando ruedas proporcionalmente...")
                self.ruedas_controller.transformar_ruedas_existentes(dimensiones_chasis=dimensiones_chasis)
                self.ruedas_controller.posicionar_ruedas(self.chasis_controller, "todas")
            else:
                # Si no hay ruedas, crearlas
                print(f"🎯 Creando nuevas ruedas proporcionales...")
                self.ruedas_controller.crear_ruedas(dimensiones_chasis=dimensiones_chasis)
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
            
            # 🔗 PASO CRÍTICO: VOLVER A CREAR JERARQUÍA DESPUÉS DE TRANSFORMAR
            self._recrear_jerarquia()
            
            print("✅✅✅ TRANSFORMACIÓN COMPLETADA CON JERARQUÍA")
            return True
            
        except Exception as e:
            cmds.warning(f"❌ Error en transformación: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def ejecutar_extrusion_automatica(self):
        """Ejecutar extrusión automática"""
        return self.extrusion_controller.aplicar_extrusion_automatica(self.ruedas_controller)
    
    def _limpiar_escena_silenciosa(self):
        """Limpia la escena sin mostrar mensajes"""
        try:
            self.ruedas_controller.limpiar_ruedas()
            self.extrusion_manager.limpiar_extrusiones()
            self.chasis_controller.limpiar_chasis()
            
            # Limpiar objetos residuales
            objetos_limpiar = cmds.ls(["axioma_*", "rueda_*"], transforms=True)
            if objetos_limpiar:
                cmds.delete(objetos_limpiar)
        except:
            pass  # Limpieza silenciosa
    
    def show_ui(self):
        """Mostrar la interfaz"""
        self.ui_builder.mostrar_ventana()

# Ejecución directa
if __name__ == "__main__":
    # Limpiar interfaz previa
    if cmds.window("chasis_con_ruedas_ui", exists=True):
        cmds.deleteUI("chasis_con_ruedas_ui")
    
    # Crear y mostrar interfaz
    app = ChasisConRuedas()
    app.show_ui()
