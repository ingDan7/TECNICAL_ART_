import maya.cmds as cmds
import random

class RuedasController:
    def __init__(self):
        self.ruedas = {}
        self.ejes = {}
        self.altura_default = 1.0
        self.altura_minima = 0.3
        
        # Rangos PROPORCIONALES al chasis
        self.rangos_ruedas = {
            'altura': {'min': 0.18, 'max': 0.25},
            'radio': {'min': 0.10, 'max': 0.18}
        }
        
        # Callbacks
        self.on_ruedas_creadas = None

    def _obtener_posicion_cara_inferior(self):
        """Obtener la posición Y de la cara inferior del chasis (axioma_carro.f[3])"""
        try:
            cara_inferior = "axioma_carro.f[3]"
            if cmds.objExists(cara_inferior):
                # Obtener el bounding box de la cara inferior
                bbox = cmds.xform(cara_inferior, query=True, boundingBox=True, worldSpace=True)
                # bbox = [xmin, ymin, zmin, xmax, ymax, zmax]
                # Para la cara inferior, nos interesa la Y máxima (parte superior de la cara)
                return bbox[4]  # ymax del bounding box
            else:
                print("⚠️ No se encontró la cara inferior axioma_carro.f[3]")
                return 0
        except Exception as e:
            print(f"⚠️ Error obteniendo posición cara inferior: {e}")
            return 0

    def crear_ruedas(self, altura=None, radio=None, dimensiones_chasis=None):
        """Crear las 4 ruedas del vehículo CON EJES - MÉTODO PRINCIPAL"""
        try:
            print("🚗 CREANDO RUEDAS Y EJES...")
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
            
            print(f"📏 Parámetros ruedas - Radio: {radio}, Grosor: {altura}")
            
            # Crear las 4 ruedas
            posiciones = ['delantera_izq', 'delantera_der', 'trasera_izq', 'trasera_der']
            
            for posicion in posiciones:
                rueda = cmds.polyCylinder(
                    radius=radio,
                    height=altura,
                    subdivisionsAxis=16,
                    subdivisionsHeight=1,
                    subdivisionsCaps=1,
                    axis=(1, 0, 0),
                    createUVs=2,
                    constructionHistory=True,
                    name=f"rueda_{posicion}"
                )
                rueda_name = rueda[0]
                self.ruedas[posicion] = rueda_name
                
                # ✅ AJUSTAR PIVOTE EN TAPA INTERNA INMEDIATAMENTE
                self._ajustar_pivote_tapa_interna(rueda_name, posicion, altura)
                print(f"  ✅ Rueda {posicion} creada con pivote en tapa interna")
            
            # Crear ejes con longitud dinámica
            self._crear_ejes_longitud_dinamica(altura, radio, dimensiones_chasis)
            
            if self.on_ruedas_creadas:
                self.on_ruedas_creadas(altura)
            
            print("🎉 RUEDAS Y EJES CREADOS EXITOSAMENTE")
            return True
            
        except Exception as e:
            cmds.warning(f"❌ Error al crear ruedas: {str(e)}")
            return False

    def _ajustar_pivote_tapa_interna(self, rueda, posicion, altura):
        """Ajustar pivote en la TAPA INTERNA de la llanta para crecimiento desde base"""
        try:
            # Calcular offset para el centro de la tapa INTERNA
            offset_tapa = altura / 2
            
            if 'izq' in posicion:
                # RUEDA IZQUIERDA: pivote en tapa X POSITIVA (que mira hacia el centro del carro)
                pivot_pos = [offset_tapa, 0, 0]  # X positivo - TAPA INTERNA
                print(f"   🎯 Pivote IZQ en tapa interna X positiva: {pivot_pos}")
            else:
                # RUEDA DERECHA: pivote en tapa X NEGATIVA (que mira hacia el centro del carro)
                pivot_pos = [-offset_tapa, 0, 0]  # X negativo - TAPA INTERNA
                print(f"   🎯 Pivote DER en tapa interna X negativa: {pivot_pos}")
            
            # MOVER PIVOTE AL CENTRO DE LA TAPA INTERNA
            cmds.xform(rueda, pivots=pivot_pos, worldSpace=True)
            cmds.makeIdentity(rueda, apply=True, translate=True, rotate=True, scale=True)
            
        except Exception as e:
            print(f"⚠️ Error ajustando pivote de {rueda}: {e}")
            cmds.xform(rueda, centerPivots=True)

    def _crear_ejes_longitud_dinamica(self, altura_rueda, radio_rueda, dimensiones_chasis):
        """Crear ejes con LONGITUD DINÁMICA basada en vértices de llantas - CORREGIDO"""
        try:
            if not dimensiones_chasis:
                dimensiones_chasis = {
                    'ancho': 3.0, 'largo': 6.0, 'alto': 1.5, 'posicion': [0, 0, 0]
                }
            
            chasis_pos = dimensiones_chasis['posicion']
            largo = dimensiones_chasis['largo']
            
            # Parámetros de ejes
            radio_eje = max(0.1, radio_rueda * 0.25)
            
            print(f"🔧 Creando ejes con LONGITUD DINÁMICA - Radio: {radio_eje:.3f}")
            
            # Crear eje delantero
            eje_delantero = cmds.polyCylinder(
                radius=radio_eje,
                height=1.0,  # Longitud temporal, se ajustará después
                subdivisionsAxis=12,
                subdivisionsHeight=1,
                subdivisionsCaps=1,
                axis=(1, 0, 0),
                createUVs=2,
                constructionHistory=True,
                name="eje_delantero"
            )
            eje_delantero_name = eje_delantero[0]
            
            # Crear eje trasero
            eje_trasero = cmds.polyCylinder(
                radius=radio_eje,
                height=1.0,  # Longitud temporal, se ajustará después
                subdivisionsAxis=12,
                subdivisionsHeight=1,
                subdivisionsCaps=1,
                axis=(1, 0, 0),
                createUVs=2,
                constructionHistory=True,
                name="eje_trasero"
            )
            eje_trasero_name = eje_trasero[0]
            
            # OBTENER POSICIÓN Y DE LA CARA INFERIOR DEL CHASIS
            y_cara_inferior = self._obtener_posicion_cara_inferior()
            
            # Posicionar ejes inicialmente - USANDO LA CARA INFERIOR COMO REFERENCIA
            offset_longitudinal = largo * 0.23
            
            # Eje delantero - POSICIONAR EN LA MISMA Y QUE LA CARA INFERIOR
            cmds.move(
                chasis_pos[0], y_cara_inferior, chasis_pos[2] + offset_longitudinal,
                eje_delantero_name, absolute=True
            )
            
            # Eje trasero - POSICIONAR EN LA MISMA Y QUE LA CARA INFERIOR
            cmds.move(
                chasis_pos[0], y_cara_inferior, chasis_pos[2] - offset_longitudinal,
                eje_trasero_name, absolute=True
            )
            
            # Aplicar color rojo a los ejes
            self._aplicar_color_simple(eje_delantero_name, [1.0, 0.0, 0.0])
            self._aplicar_color_simple(eje_trasero_name, [1.0, 0.0, 0.0])
            
            # Guardar referencias
            self.ejes = {
                'delantero': eje_delantero_name,
                'trasero': eje_trasero_name
            }
            
            # AJUSTAR LONGITUD DINÁMICA DE EJES BASADA EN VÉRTICES
            self._ajustar_longitud_ejes_dinamica()
            
            print("✅ EJES CREADOS CON LONGITUD DINÁMICA")
            
        except Exception as e:
            print(f"⚠️ Error creando ejes: {e}")

    def ajustar_altura_ruedas(self, nueva_altura):
        """Ajustar GROSOR de ruedas - USANDO SCALE DESDE PIVOTE"""
        try:
            if not self.ruedas:
                cmds.warning("No hay ruedas para ajustar")
                return False
            
            altura_actual = self.obtener_altura_actual()
            if altura_actual == 0:
                altura_actual = 0.001
            
            print(f"📏 AJUSTANDO GROSOR de ruedas: {altura_actual:.3f} → {nueva_altura:.3f}")
            
            # ✅ USAR SCALE DESDE PIVOTE
            factor_grosor = nueva_altura / altura_actual
            
            for posicion, rueda in self.ruedas.items():
                if cmds.objExists(rueda):
                    # Escalar solo en X desde el pivote en la tapa interna
                    cmds.scale(factor_grosor, 1, 1, rueda, relative=True)
                    print(f"  ✅ {posicion} - Grosor escalado: {factor_grosor:.3f}")
            
            # ✅ ACTUALIZAR EJES DESPUÉS DE AJUSTAR ALTURA
            self._ajustar_longitud_ejes_dinamica()
            
            print(f"✅ GROSOR de ruedas ajustado correctamente: {nueva_altura:.3f}")
            return True
            
        except Exception as e:
            cmds.warning(f"Error al ajustar grosor: {str(e)}")
            return False

    def ajustar_radio_ruedas(self, nuevo_radio):
        """Ajustar RADIO de ruedas - USANDO SCALE DESDE PIVOTE"""
        try:
            if not self.ruedas:
                cmds.warning("No hay ruedas para ajustar")
                return False
            
            radio_actual = self.obtener_radio_actual()
            if radio_actual == 0:
                radio_actual = 0.001
            
            print(f"📏 AJUSTANDO RADIO de ruedas: {radio_actual:.3f} → {nuevo_radio:.3f}")
            
            # ✅ USAR SCALE DESDE PIVOTE
            factor_radio = nuevo_radio / radio_actual
            
            for rueda in self.ruedas.values():
                if cmds.objExists(rueda):
                    # Escalar en Y y Z desde el pivote
                    cmds.scale(1, factor_radio, factor_radio, rueda, relative=True)
            
            # ✅ ACTUALIZAR EJES DESPUÉS DE AJUSTAR RADIO
            self._ajustar_longitud_ejes_dinamica()
            
            print(f"✅ RADIO de ruedas ajustado correctamente: {nuevo_radio:.3f}")
            return True
            
        except Exception as e:
            cmds.warning(f"Error al ajustar radio: {str(e)}")
            return False

    def transformar_ruedas_existentes(self, nueva_altura=None, nuevo_radio=None, dimensiones_chasis=None):
        """Transformar ruedas existentes - USANDO SCALE"""
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
            
            print(f"🔄 TRANSFORMANDO RUEDAS: Grosor:{nueva_altura}, Radio:{nuevo_radio}")
            
            # ✅ APLICAR TRANSFORMACIONES USANDO SCALE
            if nueva_altura is not None:
                self.ajustar_altura_ruedas(nueva_altura)
            
            if nuevo_radio is not None:
                self.ajustar_radio_ruedas(nuevo_radio)
            
            print(f"✅ RUEDAS TRANSFORMADAS Y EJES ACTUALIZADOS")
            return True
            
        except Exception as e:
            cmds.warning(f"❌ Error al transformar ruedas: {str(e)}")
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

    def obtener_altura_actual(self):
        """Obtener grosor actual de las ruedas - CONSIDERANDO ESCALA"""
        if not self.ruedas:
            return self.altura_default
        
        try:
            primera_rueda = list(self.ruedas.values())[0]
            if cmds.objExists(primera_rueda):
                # Obtener escala actual en X (que afecta la altura)
                escala = cmds.getAttr(f"{primera_rueda}.scaleX")
                
                # Buscar altura base en el nodo polyCylinder
                historial = cmds.listHistory(primera_rueda)
                for nodo in historial:
                    if cmds.nodeType(nodo) == 'polyCylinder':
                        altura_base = cmds.getAttr(f"{nodo}.height")
                        # Calcular altura real considerando la escala
                        altura_real = altura_base * escala
                        return altura_real
        except:
            pass
        
        return self.altura_default
    
    def obtener_radio_actual(self):
        """Obtener radio actual de las ruedas - CONSIDERANDO ESCALA"""
        if not self.ruedas:
            return 1.0
        
        try:
            primera_rueda = list(self.ruedas.values())[0]
            if cmds.objExists(primera_rueda):
                # Obtener escala actual en Y o Z (que afecta el radio)
                escala = cmds.getAttr(f"{primera_rueda}.scaleY")  # Usamos Y como referencia
                
                # Buscar radio base en el nodo polyCylinder
                historial = cmds.listHistory(primera_rueda)
                for nodo in historial:
                    if cmds.nodeType(nodo) == 'polyCylinder':
                        radio_base = cmds.getAttr(f"{nodo}.radius")
                        # Calcular radio real considerando la escala
                        radio_real = radio_base * escala
                        return radio_real
        except:
            pass
        
        return 1.0

    def _ajustar_longitud_ejes_dinamica(self):
        """AJUSTAR LONGITUD DE EJES DINÁMICAMENTE basado en vértices de llantas - CORREGIDO"""
        try:
            print("📏 AJUSTANDO LONGITUD DINÁMICA DE EJES...")
            
            # OBTENER POSICIÓN Y DE LA CARA INFERIOR
            y_cara_inferior = self._obtener_posicion_cara_inferior()
            
            # ================================================================
            # 1. AJUSTAR EJE TRASERO - VÉRTICES ESPECÍFICOS
            # ================================================================
            if 'trasera_der' in self.ruedas and 'trasera_izq' in self.ruedas and 'trasero' in self.ejes:
                rueda_der = self.ruedas['trasera_der']
                rueda_izq = self.ruedas['trasera_izq']
                eje = self.ejes['trasero']
                
                # VERIFICAR VÉRTICES ESPECÍFICOS
                vertice_der_32 = f"{rueda_der}.vtx[32]"
                vertice_izq_32 = f"{rueda_izq}.vtx[32]"
                
                if cmds.objExists(vertice_der_32) and cmds.objExists(vertice_izq_32):
                    # Obtener posiciones de los vértices
                    pos_der = cmds.xform(vertice_der_32, query=True, translation=True, worldSpace=True)
                    pos_izq = cmds.xform(vertice_izq_32, query=True, translation=True, worldSpace=True)
                    
                    # Calcular distancia entre vértices (longitud necesaria del eje)
                    distancia = ((pos_der[0] - pos_izq[0])**2 + 
                                (pos_der[1] - pos_izq[1])**2 + 
                                (pos_der[2] - pos_izq[2])**2)**0.5
                    
                    # Ajustar longitud del eje trasero
                    self._ajustar_longitud_eje(eje, distancia)
                    print(f"  ✅ Eje trasero - Longitud ajustada: {distancia:.3f}")
                    
                    # Posicionar eje en el centro entre los vértices EN X y Z, pero usar Y DE LA CARA INFERIOR
                    centro_x = (pos_der[0] + pos_izq[0]) / 2
                    centro_z = (pos_der[2] + pos_izq[2]) / 2
                    
                    cmds.move(centro_x, y_cara_inferior, centro_z, eje, absolute=True)
                    
                else:
                    print("  ⚠️ Vértices no encontrados para eje trasero")
            
            # ================================================================
            # 2. AJUSTAR EJE DELANTERO - VÉRTICES ESPECÍFICOS
            # ================================================================
            if 'delantera_der' in self.ruedas and 'delantera_izq' in self.ruedas and 'delantero' in self.ejes:
                rueda_der = self.ruedas['delantera_der']
                rueda_izq = self.ruedas['delantera_izq']
                eje = self.ejes['delantero']
                
                # VERIFICAR VÉRTICES ESPECÍFICOS
                vertice_der_32 = f"{rueda_der}.vtx[32]"
                vertice_izq_32 = f"{rueda_izq}.vtx[32]"
                
                if cmds.objExists(vertice_der_32) and cmds.objExists(vertice_izq_32):
                    # Obtener posiciones de los vértices
                    pos_der = cmds.xform(vertice_der_32, query=True, translation=True, worldSpace=True)
                    pos_izq = cmds.xform(vertice_izq_32, query=True, translation=True, worldSpace=True)
                    
                    # Calcular distancia entre vértices (longitud necesaria del eje)
                    distancia = ((pos_der[0] - pos_izq[0])**2 + 
                                (pos_der[1] - pos_izq[1])**2 + 
                                (pos_der[2] - pos_izq[2])**2)**0.5
                    
                    # Ajustar longitud del eje delantero
                    self._ajustar_longitud_eje(eje, distancia)
                    print(f"  ✅ Eje delantero - Longitud ajustada: {distancia:.3f}")
                    
                    # Posicionar eje en el centro entre los vértices EN X y Z, pero usar Y DE LA CARA INFERIOR
                    centro_x = (pos_der[0] + pos_izq[0]) / 2
                    centro_z = (pos_der[2] + pos_izq[2]) / 2
                    
                    cmds.move(centro_x, y_cara_inferior, centro_z, eje, absolute=True)
                    
                else:
                    print("  ⚠️ Vértices no encontrados para eje delantero")
            
            print("🎯 LONGITUD DE EJES AJUSTADA DINÁMICAMENTE")
            
        except Exception as e:
            print(f"❌ Error ajustando longitud de ejes: {e}")

    def _ajustar_longitud_eje(self, eje, nueva_longitud):
        """Ajustar la longitud de un eje específico"""
        try:
            # Buscar nodo polyCylinder del eje
            historial = cmds.listHistory(eje)
            nodo_cilindro = None
            
            for nodo in historial:
                if cmds.nodeType(nodo) == 'polyCylinder':
                    nodo_cilindro = nodo
                    break
            
            if nodo_cilindro:
                # Ajustar longitud (height) del eje
                cmds.setAttr(f"{nodo_cilindro}.height", nueva_longitud)
                return True
            else:
                print(f"  ⚠️ No se encontró nodo polyCylinder para {eje}")
                return False
                
        except Exception as e:
            print(f"  ❌ Error ajustando longitud del eje {eje}: {e}")
            return False

    def posicionar_ruedas(self, chasis_controller, tipo_posicion="todas"):
        """Posicionar ruedas y actualizar ejes dinámicamente - CORREGIDO DEFINITIVO"""
        if not self.ruedas:
            cmds.warning("⚠️ No hay ruedas para posicionar")
            return False
        
        dimensiones = chasis_controller.obtener_dimensiones()
        if not dimensiones:
            return False
        
        chasis_pos = dimensiones['posicion']
        ancho = dimensiones['ancho']
        alto = dimensiones['alto'] 
        largo = dimensiones['largo']
        
        radio_actual = self.obtener_radio_actual()
        altura_actual = self.obtener_altura_actual()
        
        print(f"📍 POSICIONANDO RUEDAS - Chasis: {ancho:.3f}x{alto:.3f}x{largo:.3f}")
        
        # OBTENER POSICIÓN Y DE LA CARA INFERIOR DEL CHASIS
        y_cara_inferior = self._obtener_posicion_cara_inferior()
        print(f"🎯 Posición Y cara inferior: {y_cara_inferior:.3f}")
        
        # Calcular posiciones - USANDO LA MISMA Y PARA RUEDAS Y EJES
        MARGEN_LATERAL = 0.001
        PORCENTAJE_LONGITUDINAL = 0.23
        
        offset_lateral = radio_actual + MARGEN_LATERAL
        offset_longitudinal = largo * PORCENTAJE_LONGITUDINAL
        
        # ✅ CORRECCIÓN CRÍTICA: USAR LA MISMA Y PARA RUEDAS Y EJES
        # Esto asegura que los centros de las llantas coincidan con los ejes
        altura_posicion = y_cara_inferior
        
        print(f"🎯 Altura ruedas y ejes: {altura_posicion:.3f} (MISMA POSICIÓN)")
        
        # Definir posiciones
        posiciones = {
            'delantera_izq': [
                chasis_pos[0] - (ancho / 2) - offset_lateral,
                altura_posicion,
                chasis_pos[2] + offset_longitudinal
            ],
            'delantera_der': [
                chasis_pos[0] + (ancho / 2) + offset_lateral,
                altura_posicion,
                chasis_pos[2] + offset_longitudinal
            ],
            'trasera_izq': [
                chasis_pos[0] - (ancho / 2) - offset_lateral,
                altura_posicion,
                chasis_pos[2] - offset_longitudinal
            ],
            'trasera_der': [
                chasis_pos[0] + (ancho / 2) + offset_lateral,
                altura_posicion,
                chasis_pos[2] - offset_longitudinal
            ]
        }
        
        # Aplicar posiciones a las ruedas
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
                print(f"   ✅ {posicion}: [{posiciones[posicion][0]:.3f}, {posiciones[posicion][1]:.3f}, {posiciones[posicion][2]:.3f}]")
        
        # ✅ ACTUALIZAR LONGITUD Y POSICIÓN DE EJES DINÁMICAMENTE
        self._ajustar_longitud_ejes_dinamica()
        
        print("🎯 RUEDAS Y EJES POSICIONADOS CORRECTAMENTE")
        return True

    def _aplicar_color_simple(self, objeto, color_rgb):
        """Aplicar color de manera simple"""
        try:
            if not cmds.objExists(objeto):
                return
                
            material_name = f"material_{objeto}"
            if cmds.objExists(material_name):
                cmds.delete(material_name)
                
            material = cmds.shadingNode('lambert', asShader=True, name=material_name)
            cmds.setAttr(f"{material}.color", color_rgb[0], color_rgb[1], color_rgb[2])
            
            shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, 
                                    name=f"{material_name}SG")
            cmds.connectAttr(f"{material}.outColor", f"{shading_group}.surfaceShader")
            cmds.sets(objeto, edit=True, forceElement=shading_group)
            
        except Exception as e:
            print(f"⚠️ Error aplicando color: {e}")

    def generar_tamanio_proporcional(self, dimensiones_chasis):
        """Generar tamaño de ruedas proporcional al chasis"""
        if not dimensiones_chasis:
            return self.generar_tamanio_aleatorio()
        
        try:
            proporcion_altura = random.uniform(self.rangos_ruedas['altura']['min'], 
                                             self.rangos_ruedas['altura']['max'])
            proporcion_radio = random.uniform(self.rangos_ruedas['radio']['min'], 
                                            self.rangos_ruedas['radio']['max'])
            
            altura_rueda = dimensiones_chasis['ancho'] * proporcion_altura
            radio_rueda = dimensiones_chasis['alto'] * proporcion_radio
            
            altura_rueda = max(0.2, min(1.5, round(altura_rueda, 2)))
            radio_rueda = max(0.3, min(2.0, round(radio_rueda, 2)))
            
            return {'altura': altura_rueda, 'radio': radio_rueda}
            
        except Exception as e:
            print(f"⚠️ Error en tamaño proporcional: {e}")
            return self.generar_tamanio_aleatorio()
    
    def generar_tamanio_aleatorio(self):
        """Generar tamaño aleatorio como fallback"""
        return {
            'altura': round(random.uniform(0.4, 1.2), 2),
            'radio': round(random.uniform(0.4, 1.0), 2)
        }

    def limpiar_ruedas(self):
        """Eliminar todas las ruedas Y ejes"""
        print("🧹 LIMPIANDO RUEDAS Y EJES...")
        
        # Limpiar ruedas
        for rueda in self.ruedas.values():
            if cmds.objExists(rueda):
                cmds.delete(rueda)
        self.ruedas = {}
        
        # Limpiar ejes
        for eje in self.ejes.values():
            if cmds.objExists(eje):
                cmds.delete(eje)
        self.ejes = {}
        
        print("✅ RUEDAS Y EJES LIMPIADOS")

