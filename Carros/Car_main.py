import maya.cmds as cmds
import random
import traceback

# Importar Componentes
from ui_builder import UIBuilder
from chasis_controller import ChasisController
from ruedas_controller import RuedasController
from extrusion_manager import ExtrusionManager
from VertexController import VertexController 
from ExtrusionController import ExtrusionController

# ✅ IMPORTAR SYSTEMA DE EVENTOS
from event_system import (
    EventSystem, 
    EVENT_EMERGIR_CARRO, 
    EVENT_ACTUALIZAR_VERTICES,
    EVENT_ACTUALIZAR_UI_EXTRUSION,
    EVENT_ACTUALIZAR_UI_RUEDAS
)

class ChasisConRuedas:
    def __init__(self):
        self.window_name = "chasis_con_ruedas_ui"
        
        # ✅ Inicializar EventSystem (Singleton)
        self.event_system = EventSystem()
        
        # Inicializar controladores
        self.chasis_controller = ChasisController()
        self.ruedas_controller = RuedasController()
        self.extrusion_manager = ExtrusionManager()
        self.extrusion_controller = ExtrusionController()
        self.vertex_controller = VertexController()
        
        # Construir UI
        # Nota: La UI ahora se suscribe sola a los eventos en su __init__
        self.ui_builder = UIBuilder(
            self.window_name,
            self.chasis_controller,
            self.ruedas_controller,
            self.extrusion_manager,
            self.vertex_controller,
            self  # Pasar referencia main_app para emerger_carro
        )
        
        # Conectar eventos específicos de la lógica de negocio (si los hubiera)
        self._conectar_eventos_logica()
    
    def _conectar_eventos_logica(self):
        """
        Conectar eventos de lógica de negocio.
        Nota: Las actualizaciones de UI ya no pasan por aquí, 
        la UIBuilder las escucha directamente del EventSystem.
        """
        print("🔗 Lógica de negocio conectada al EventSystem")
        # Aquí podrías suscribirte a logs o analíticas si fuera necesario
        pass

    # -------------------------------------------------------------------------
    # 🚀 LÓGICA PRINCIPAL
    # -------------------------------------------------------------------------

    def emerger_carro(self):
        """Función principal EMERGER - Crear o transformar carro existente"""
        try:
            print("🎲🎲🎲 PRESIONADO EMERGER - INICIANDO...")
            
            # VERIFICAR SI EXISTE CARRO
            carro_existente = self._verificar_carro_existente()
            print(f"🔍 Estado del carro: {'EXISTE' if carro_existente else 'NO EXISTE'}")
            
            # SIEMPRE generar nuevas dimensiones aleatorias
            dimensiones_chasis = self.chasis_controller.generar_dimensiones_aleatorias()
            
            exito = False
            if carro_existente:
                print("🔄🔄🔄 TRANSFORMANDO CARRO EXISTENTE...")
                if self._transformar_carro_existente(dimensiones_chasis):
                    print("✅✅✅ CARRO TRANSFORMADO EXITOSAMENTE")
                    exito = True
                else:
                    print("❌❌❌ FALLÓ LA TRANSFORMACIÓN - Creando nuevo carro...")
                    exito = self._crear_nuevo_carro(dimensiones_chasis)
            else:
                print("🎯🎯🎯 CREANDO NUEVO CARRO...")
                exito = self._crear_nuevo_carro(dimensiones_chasis)
            
            if exito:
                # ✅ EMITIR EVENTO DE FINALIZACIÓN
                # Esto avisa a cualquier componente (UI, Logs) que el carro está listo
                EventSystem.emit(EVENT_EMERGIR_CARRO, {"resultado": "exito"})
                print("🎉🎉🎉 PROCESO EMERGER COMPLETADO!")
            
        except Exception as e:
            cmds.warning(f"❌ Error crítico en emerger_carro: {str(e)}")
            traceback.print_exc()
    
    def _verificar_carro_existente(self):
        """Verificar si ya existe un carro en escena"""
        carro_en_escena = cmds.objExists("axioma_carro")
        
        if carro_en_escena and not self.chasis_controller.cubo_actual:
            self.chasis_controller.cubo_actual = "axioma_carro"
        
        return carro_en_escena

    def _crear_nuevo_carro(self, dimensiones_chasis):
        print("🏗️ CREANDO CARRO DESDE CERO CON VÉRTICES ALEATORIOS...")
        
        # 1. Crear chasis base
        chasis = self.chasis_controller.crear_cubo_base(
            "axioma_carro", 
            dimensiones_chasis['ancho'], 
            dimensiones_chasis['alto'], 
            dimensiones_chasis['largo']
        )

        if not chasis:
            return False

        # 2. Preservar y Modificar Vértices
        self.vertex_controller.preservar_posiciones_y_originales()
        
        print("🎲 APLICANDO DESPLAZAMIENTOS ALEATORIOS A VÉRTICES...")
        # El VertexController aplicará cambios y EMITIRÁ EVENT_ACTUALIZAR_VERTICES internamente
        desplazamientos = self.vertex_controller.aplicar_desplazamientos_aleatorios_avanzados()
        
        # Si el controller no emite automáticamente, forzamos la emisión (seguridad):
        if desplazamientos:
            EventSystem.emit(EVENT_ACTUALIZAR_VERTICES, {'desplazamientos': desplazamientos})
        
        # 3. Crear extrusiones
        for tipo in self.extrusion_manager.configuracion.keys():
            thickness_aleatorio = self.extrusion_manager.generar_thickness_aleatorio(tipo)
            resultado = self.extrusion_manager.crear_extrusion(chasis, tipo, thickness_aleatorio)
            
            if resultado:
                # ✅ EMITIR actualización de extrusión para la UI
                EventSystem.emit(EVENT_ACTUALIZAR_UI_EXTRUSION, {
                    'tipo': tipo, 
                    'thickness': thickness_aleatorio
                })
        
        # 4. Crear Ruedas
        print(f"🎯 Creando ruedas proporcionales al chasis...")
        self.ruedas_controller.crear_ruedas(dimensiones_chasis=dimensiones_chasis)
        self.ruedas_controller.posicionar_ruedas(self.chasis_controller, "todas")
        
        # La creación de ruedas debería emitir, si no, emitimos aquí la altura actual:
        altura_ruedas = self.ruedas_controller.obtener_altura_actual() if hasattr(self.ruedas_controller, 'obtener_altura_actual') else 1.0
        EventSystem.emit(EVENT_ACTUALIZAR_UI_RUEDAS, altura_ruedas)
        
        # 5. Extrusión Automática
        print("🎯 EJECUTANDO EXTRUSIÓN AUTOMÁTICA...")
        self.extrusion_controller.aplicar_extrusion_automatica(
            ruedas_controller=self.ruedas_controller
        )
        
        return True

    def _transformar_carro_existente(self, dimensiones_chasis):
        """Transformar el carro existente CON VÉRTICES ALEATORIOS"""
        try:
            # 1. Transformar Chasis
            resultado_chasis = self.chasis_controller.transformar_chasis_existente(
                dimensiones_chasis['ancho'], 
                dimensiones_chasis['alto'], 
                dimensiones_chasis['largo']
            )
            
            if not resultado_chasis:
                return False
            
            # 2. Vértices Aleatorios
            print("🎲 APLICANDO DESPLAZAMIENTOS ALEATORIOS...")
            desplazamientos = self.vertex_controller.aplicar_desplazamientos_aleatorios()
            # Asegurar emisión de evento para UI
            if desplazamientos:
                EventSystem.emit(EVENT_ACTUALIZAR_VERTICES, {'desplazamientos': desplazamientos})
            
            # 3. Transformar Ruedas
            if self.ruedas_controller.ruedas:
                self.ruedas_controller.transformar_ruedas_existentes(dimensiones_chasis=dimensiones_chasis)
                self.ruedas_controller.posicionar_ruedas(self.chasis_controller, "todas")
            else:
                self.ruedas_controller.crear_ruedas(dimensiones_chasis=dimensiones_chasis)
                self.ruedas_controller.posicionar_ruedas(self.chasis_controller, "todas")
            
            # 4. Extrusión Automática
            self.extrusion_controller.aplicar_extrusion_automatica(
                ruedas_controller=self.ruedas_controller
            )
            
            return True
            
        except Exception as e:
            cmds.warning(f"❌ Error en transformación: {str(e)}")
            traceback.print_exc()
            return False
    
    def ejecutar_extrusion_automatica(self):
        """Ejecutar extrusión automática"""
        return self.extrusion_controller.aplicar_extrusion_automatica(self.ruedas_controller)
    
    def show_ui(self):
        """Mostrar la interfaz"""
        self.ui_builder.mostrar_ventana()

# Ejecución directa
if __name__ == "__main__":
    if cmds.window("chasis_con_ruedas_ui", exists=True):
        cmds.deleteUI("chasis_con_ruedas_ui")
    
    app = ChasisConRuedas()
    app.show_ui()