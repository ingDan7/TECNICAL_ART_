import maya.cmds as cmds
import random

class RuedasController:
    def __init__(self):
        self.ruedas = {}
        self.altura_default = 1.0
        self.altura_minima = 0.3
        
        # Rangos PROPORCIONALES al chasis
        self.rangos_ruedas = {
            'altura': {'min': 0.18, 'max': 0.25},  # Grosor de la llanta (eje X global)
            'radio': {'min': 0.10, 'max': 0.18}    # Radio/diámetro de la llanta
        }
        
        # Callbacks
        self.on_ruedas_creadas = None
    
    def generar_tamanio_proporcional(self, dimensiones_chasis):
        """Generar tamaño de ruedas proporcional al chasis"""
        if not dimensiones_chasis:
            return self.generar_tamanio_aleatorio()
        
        try:
            proporcion_altura = random.uniform(self.rangos_ruedas['altura']['min'], 
                                             self.rangos_ruedas['altura']['max'])
            proporcion_radio = random.uniform(self.rangos_ruedas['radio']['min'], 
                                            self.rangos_ruedas['radio']['max'])
            
            # Altura = Grosor de la llanta (eje X global)
            altura_rueda = dimensiones_chasis['ancho'] * proporcion_altura
            # Radio = Tamaño de la rueda
            radio_rueda = dimensiones_chasis['alto'] * proporcion_radio
            
            altura_rueda = max(0.2, min(1.5, round(altura_rueda, 2)))
            radio_rueda = max(0.3, min(2.0, round(radio_rueda, 2)))
            
            print(f"📏 RUEDAS PROPORCIONALES - Chasis: {dimensiones_chasis['ancho']}x{dimensiones_chasis['alto']}x{dimensiones_chasis['largo']}")
            print(f"   -> Ruedas: Grosor(Altura):{altura_rueda}, Radio:{radio_rueda}")
            
            return {
                'altura': altura_rueda,
                'radio': radio_rueda
            }
            
        except Exception as e:
            print(f"⚠️ Error en tamaño proporcional, usando aleatorio: {e}")
            return self.generar_tamanio_aleatorio()
    
    def generar_tamanio_aleatorio(self):
        """Generar tamaño aleatorio como fallback"""
        return {
            'altura': round(random.uniform(0.4, 1.2), 2),  # Grosor más variado
            'radio': round(random.uniform(0.4, 1.0), 2)
        }
    
    def crear_ruedas(self, altura=None, radio=None, dimensiones_chasis=None):
        """Crear las 4 ruedas del vehículo - PIVOTES CORRECTOS EN CARAS CIRCULARES"""
        try:
            # LIMPIAR RUEDAS EXISTENTES PRIMERO
            self.limpiar_ruedas()
            
            # Determinar tamaño de ruedas
            if dimensiones_chasis:
                tamaño_ruedas = self.generar_tamanio_proporcional(dimensiones_chasis)
                altura = tamaño_ruedas['altura']
                radio = tamaño_ruedas['radio']
            elif altura is None or radio is None:
                tamaño_ruedas = self.generar_tamanio_aleatorio()
                altura = tamaño_ruedas['altura']
                radio = tamaño_ruedas['radio']
            
            posiciones = ['delantera_izq', 'delantera_der', 'trasera_izq', 'trasera_der']
            
            for posicion in posiciones:
                # CREAR CILINDRO NATIVO DE MAYA - ORIENTACIÓN CORRECTA PARA ESCALA EN X
                rueda = cmds.polyCylinder(
                    radius=radio,
                    height=altura,  # Esto será el GROSOR de la llanta (eje X)
                    subdivisionsX=10,  # 10 caras
                    subdivisionsY=1,   # 1 subdivisión en altura
                    subdivisionsZ=0,   # Sin subdivisiones adicionales
                    axis=(1, 0, 0),    # Eje X - PARA QUE EL GROSOR ESTÉ EN X
                    createUVs=4,       # UVs normales
                    constructionHistory=True,
                    name=f"rueda_{posicion}"
                )[0]
                
                # El cilindro ya está orientado correctamente con grosor en X
                # NO ROTAR - mantener orientación nativa con eje en X
                
                # AJUSTAR PIVOTE EN LA CARA CIRCULAR CORRECTA SEGÚN POSICIÓN
                self._ajustar_pivote_cara_correcta(rueda, posicion, altura)
                
                self.ruedas[posicion] = rueda
            
            # Notificar callback
            if self.on_ruedas_creadas:
                self.on_ruedas_creadas(altura)
            
            print(f"✅ 4 RUEDAS CREADAS - Grosor(X):{altura}, Radio:{radio}")
            return True
            
        except Exception as e:
            cmds.warning(f"❌ Error al crear ruedas: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def _ajustar_pivote_cara_correcta(self, rueda, posicion, altura):
        """Ajustar pivote en la cara circular CORRECTA según posición de la rueda"""
        try:
            # Para un cilindro con eje en X:
            # - Las caras circulares están en los extremos X
            # - Cara X positiva y cara X negativa
            
            # CALCULAR OFFSET PARA EL CENTRO DE LA CARA
            offset_cara = altura / 2
            
            if 'izq' in posicion:
                # RUEDA LEFT: pivote en cara X POSITIVA (que mira hacia el centro del carro)
                pivot_pos = [offset_cara, 0, 0]  # X positivo
                print(f"   🎯 Pivote LEFT en cara X positiva: {pivot_pos}")
            else:
                # RUEDA RIGHT: pivote en cara X NEGATIVA (que mira hacia el centro del carro)
                pivot_pos = [-offset_cara, 0, 0]  # X negativo
                print(f"   🎯 Pivote RIGHT en cara X negativa: {pivot_pos}")
            
            # MOVER PIVOTE AL CENTRO DE LA CARA CORRECTA
            cmds.xform(rueda, pivots=pivot_pos)
            
        except Exception as e:
            print(f"⚠️ Error ajustando pivote de {rueda}: {e}")
            cmds.xform(rueda, centerPivots=True)

    def transformar_ruedas_existentes(self, nueva_altura=None, nuevo_radio=None, dimensiones_chasis=None):
        """Transformar ruedas existentes - ESCALA CORRECTA EN EJES GLOBALES"""
        if not self.ruedas:
            print("⚠️ No hay ruedas existentes para transformar")
            return False
        
        try:
            # Determinar nuevo tamaño
            if dimensiones_chasis:
                tamaño_ruedas = self.generar_tamanio_proporcional(dimensiones_chasis)
                nueva_altura = tamaño_ruedas['altura']
                nuevo_radio = tamaño_ruedas['radio']
            elif nueva_altura is None or nuevo_radio is None:
                tamaño_aleatorio = self.generar_tamanio_aleatorio()
                nueva_altura = tamaño_aleatorio['altura']
                nuevo_radio = tamaño_aleatorio['radio']
            
            print(f"🔄 TRANSFORMANDO RUEDAS: Grosor(X):{nueva_altura}, Radio:{nuevo_radio}")
            
            for posicion, rueda_nombre in self.ruedas.items():
                if cmds.objExists(rueda_nombre):
                    # Buscar nodo polyCylinder
                    historial = cmds.listHistory(rueda_nombre)
                    nodo_cilindro = None
                    
                    for nodo in historial:
                        if cmds.nodeType(nodo) == 'polyCylinder':
                            nodo_cilindro = nodo
                            break
                    
                    if nodo_cilindro:
                        # Modificar directamente en el nodo
                        cmds.setAttr(f"{nodo_cilindro}.height", nueva_altura)  # Grosor en X
                        cmds.setAttr(f"{nodo_cilindro}.radius", nuevo_radio)   # Radio
                        
                        # REAJUSTAR PIVOTE en la misma cara correcta
                        self._ajustar_pivote_cara_correcta(rueda_nombre, posicion, nueva_altura)
                    else:
                        # ESCALAR desde pivote en cara circular
                        altura_actual = self.obtener_altura_actual()
                        radio_actual = self.obtener_radio_actual()
                        
                        if altura_actual > 0 and radio_actual > 0:
                            # ESCALA EN X para GROSOR (hacer más ancha/delgada la llanta)
                            factor_grosor = nueva_altura / altura_actual
                            # ESCALA EN Y y Z para RADIO (tamaño de la rueda)
                            factor_radio = nuevo_radio / radio_actual
                            
                            # Escalar desde el pivote en la cara circular
                            cmds.scale(factor_grosor, factor_radio, factor_radio, rueda_nombre, relative=True)
            
            print(f"✅ RUEDAS TRANSFORMADAS")
            return True
            
        except Exception as e:
            cmds.warning(f"❌ Error al transformar ruedas: {str(e)}")
            return False
    
    def obtener_altura_actual(self):
        """Obtener grosor actual de las ruedas (eje X)"""
        if not self.ruedas:
            return self.altura_default
        
        try:
            primera_rueda = list(self.ruedas.values())[0]
            if cmds.objExists(primera_rueda):
                historial = cmds.listHistory(primera_rueda)
                for nodo in historial:
                    if cmds.nodeType(nodo) == 'polyCylinder':
                        return cmds.getAttr(f"{nodo}.height")
        except:
            pass
        
        return self.altura_default
    
    def obtener_radio_actual(self):
        """Obtener radio actual de las ruedas"""
        if not self.ruedas:
            return 1.0
        
        try:
            primera_rueda = list(self.ruedas.values())[0]
            if cmds.objExists(primera_rueda):
                historial = cmds.listHistory(primera_rueda)
                for nodo in historial:
                    if cmds.nodeType(nodo) == 'polyCylinder':
                        return cmds.getAttr(f"{nodo}.radius")
        except:
            pass
        
        return 1.0

    def _calcular_posiciones_milimetricas(self, chasis_pos, ancho, alto, largo, radio_rueda, altura_rueda):
        """Calcular posiciones con contacto MILIMÉTRICO al chasis"""
        
        # ================================================================
        # 🎯 FÓRMULA MILIMÉTRICA - CONTACTO TANGENCIAL
        # ================================================================
        
        # MARGENES MILIMÉTRICOS - CONTACTO CASI PERFECTO
        MARGEN_LATERAL = 0.001     # 1mm de separación lateral
        MARGEN_VERTICAL = 0.001    # 1mm de separación vertical
        PORCENTAJE_LONGITUDINAL = 0.23  # 23% del largo
        
        # ================================================================
        # 📏 POSICIONES LATERALES - CONTACTO MILIMÉTRICO
        # ================================================================
        # El borde de la rueda toca casi perfectamente el borde del chasis
        offset_lateral = radio_rueda + MARGEN_LATERAL
        
        # ================================================================
        # 📐 POSICIONES LONGITUDINALES
        # ================================================================
        offset_longitudinal = largo * PORCENTAJE_LONGITUDINAL
        
        # ================================================================
        # 📊 ALTURA - CONTACTO MILIMÉTRICO CON SUELO
        # ================================================================
        # La base de la rueda toca casi perfectamente la base del chasis
        altura_posicion = chasis_pos[1] - (alto / 2) + (altura_rueda / 2) + MARGEN_VERTICAL
        
        # ================================================================
        # 🎯 POSICIONES FINALES - CONTACTO MILIMÉTRICO
        # ================================================================
        posiciones = {
            'delantera_izq': [
                chasis_pos[0] - (ancho / 2) - offset_lateral,  # CONTACTO lateral
                altura_posicion,                               # CONTACTO vertical
                chasis_pos[2] + offset_longitudinal           # Posición Z
            ],
            'delantera_der': [
                chasis_pos[0] + (ancho / 2) + offset_lateral,  # CONTACTO lateral
                altura_posicion,                               # CONTACTO vertical
                chasis_pos[2] + offset_longitudinal
            ],
            'trasera_izq': [
                chasis_pos[0] - (ancho / 2) - offset_lateral,  # CONTACTO lateral
                altura_posicion,                               # CONTACTO vertical
                chasis_pos[2] - offset_longitudinal
            ],
            'trasera_der': [
                chasis_pos[0] + (ancho / 2) + offset_lateral,  # CONTACTO lateral
                altura_posicion,                               # CONTACTO vertical
                chasis_pos[2] - offset_longitudinal
            ]
        }
        
        return posiciones

    def posicionar_ruedas(self, chasis_controller, tipo_posicion="todas"):
        """Posicionar ruedas con contacto MILIMÉTRICO al chasis"""
        if not self.ruedas or not chasis_controller.cubo_actual:
            cmds.warning("⚠️ No hay chasis y ruedas para posicionar")
            return
        
        dimensiones = chasis_controller.obtener_dimensiones()
        if not dimensiones:
            return
        
        chasis_pos = dimensiones['posicion']
        ancho = dimensiones['ancho']
        alto = dimensiones['alto'] 
        largo = dimensiones['largo']
        
        radio_actual = self.obtener_radio_actual()
        altura_actual = self.obtener_altura_actual()
        
        print(f"📍 POSICIONANDO RUEDAS - CONTACTO MILIMÉTRICO")
        print(f"   Chasis: {ancho:.3f}x{alto:.3f}x{largo:.3f}")
        print(f"   Ruedas: Radio:{radio_actual:.3f}, Grosor(X):{altura_actual:.3f}")
        
        # USAR FÓRMULA DE CONTACTO MILIMÉTRICO
        posiciones = self._calcular_posiciones_milimetricas(
            chasis_pos, ancho, alto, largo, radio_actual, altura_actual
        )
        
        # Aplicar posiciones
        ruedas_a_mover = []
        if tipo_posicion == "delanteras":
            ruedas_a_mover = ['delantera_izq', 'delantera_der']
        elif tipo_posicion == "traseras":
            ruedas_a_mover = ['trasera_izq', 'trasera_der']
        else:
            ruedas_a_mover = list(self.ruedas.keys())
        
        for posicion in ruedas_a_mover:
            if posicion in self.ruedas and cmds.objExists(self.ruedas[posicion]):
                cmds.move(
                    posiciones[posicion][0],
                    posiciones[posicion][1], 
                    posiciones[posicion][2],
                    self.ruedas[posicion],
                    absolute=True
                )
                print(f"   ✅ {posicion}: [{posiciones[posicion][0]:.4f}, {posiciones[posicion][1]:.4f}, {posiciones[posicion][2]:.4f}]")
        
        print("🎯 RUEDAS POSICIONADAS - CONTACTO MILIMÉTRICO PERFECTO")

    # MÉTODOS DE AJUSTE MANTENIDOS - ESCALA EN X PARA GROSOR
    def ajustar_altura_ruedas(self, nueva_altura):
        """Ajustar GROSOR de ruedas - ESCALA EN EJE X GLOBAL"""
        try:
            altura_actual = self.obtener_altura_actual()
            if altura_actual == 0:
                altura_actual = 0.001
            
            # ESCALA EN X GLOBAL para cambiar el GROSOR de la llanta
            factor_grosor = nueva_altura / altura_actual
            
            for rueda in self.ruedas.values():
                if cmds.objExists(rueda):
                    # Escalar solo en X - hace más ancha/delgada la llanta
                    cmds.scale(factor_grosor, 1, 1, rueda, relative=True)
            
            print(f"📏 GROSOR de ruedas ajustado (eje X global): {nueva_altura:.3f}")
            return True
        except Exception as e:
            cmds.warning(f"Error al ajustar grosor: {str(e)}")
            return False

    def ajustar_radio_ruedas(self, nuevo_radio):
        """Ajustar RADIO de ruedas - ESCALA EN EJES Y y Z GLOBALES"""
        try:
            radio_actual = self.obtener_radio_actual()
            if radio_actual == 0:
                radio_actual = 0.001
            
            # ESCALA EN Y y Z GLOBALES para cambiar el RADIO de la rueda
            factor_radio = nuevo_radio / radio_actual
            
            for rueda in self.ruedas.values():
                if cmds.objExists(rueda):
                    # Escalar en Y y Z - cambia el tamaño/diámetro de la rueda
                    cmds.scale(1, factor_radio, factor_radio, rueda, relative=True)
            
            print(f"📏 RADIO de ruedas ajustado (ejes Y,Z globales): {nuevo_radio:.3f}")
            return True
        except Exception as e:
            cmds.warning(f"Error al ajustar radio: {str(e)}")
            return False

    def aumentar_altura(self, incremento=0.1):
        """Aumentar GROSOR de ruedas (hacer más anchas)"""
        if not self.ruedas:
            cmds.warning("Primero crea las ruedas")
            return None
        
        altura_actual = self.obtener_altura_actual()
        nueva_altura = altura_actual + incremento
        
        if self.ajustar_altura_ruedas(nueva_altura):
            return nueva_altura
        
        return None
    
    def disminuir_altura(self, decremento=0.1):
        """Disminuir GROSOR de ruedas (hacer más delgadas)"""
        if not self.ruedas:
            cmds.warning("Primero crea las ruedas")
            return None
        
        altura_actual = self.obtener_altura_actual()
        nueva_altura = max(self.altura_minima, altura_actual - decremento)
        
        if self.ajustar_altura_ruedas(nueva_altura):
            return nueva_altura
        
        return None
    
    def limpiar_ruedas(self):
        """Eliminar todas las ruedas"""
        for rueda in self.ruedas.values():
            if cmds.objExists(rueda):
                cmds.delete(rueda)
        self.ruedas = {}
        print("🧹 Ruedas limpiadas")