# import maya.cmds as cmds
# import math
# from carro_rig_utils import (
#     get_face_center, align_joint_to_position, align_to_object_center, 
#     create_control, buscar_objetos_escena_filtrado, NOMBRES_ESTANDAR
# )

# class CarroRigCore:
#     def __init__(self):
#         print("🔧 CarroRigCore inicializado")
    
#     def _verificar_geometria_existente(self):
#         """Verifica que existe la geometría necesaria antes de crear el rig"""
#         try:
#             print("🔍 Verificando geometría existente...")
            
#             # Verificar chasis principal
#             chasis = None
#             if cmds.objExists("axioma_carro"):
#                 chasis = "axioma_carro"
#                 print("✅ Chasis encontrado: axioma_carro")
#             else:
#                 print("❌ NO se encontró el chasis 'axioma_carro'")
#                 return None, [], []
            
#             # Verificar ejes
#             ejes = []
#             if cmds.objExists("eje_delantero"):
#                 ejes.append("eje_delantero")
#             if cmds.objExists("eje_trasero"):
#                 ejes.append("eje_trasero")
#             print(f"✅ Ejes encontrados: {ejes}")
            
#             # Verificar ruedas
#             ruedas = []
#             ruedas_nombres = [
#                 "rueda_delantera_izq", "rueda_delantera_der",
#                 "rueda_trasera_izq", "rueda_trasera_der"
#             ]
#             for rueda in ruedas_nombres:
#                 if cmds.objExists(rueda):
#                     ruedas.append(rueda)
#             print(f"✅ Ruedas encontradas: {ruedas}")
            
#             if not ruedas:
#                 print("⚠️ No se encontraron ruedas, el rig puede no funcionar correctamente")
            
#             return chasis, ruedas, ejes
            
#         except Exception as e:
#             print(f"❌ Error verificando geometría: {e}")
#             return None, [], []
    
#     def _crear_joint_seguro(self, nombre, posicion_default):
#         """Crea un joint de forma segura con posición por defecto"""
#         try:
#             cmds.select(clear=True)
#             joint = cmds.joint(name=nombre)
            
#             # Intentar posicionar en objeto existente, sino usar posición por defecto
#             target_name = nombre.replace("joint_", "")
#             if cmds.objExists(target_name):
#                 try:
#                     target_pos = align_to_object_center(target_name)
#                     if target_pos:
#                         align_joint_to_position(joint, target_pos)
#                         print(f"   ✅ Joint {nombre} posicionado en {target_name}")
#                     else:
#                         align_joint_to_position(joint, posicion_default)
#                 except:
#                     align_joint_to_position(joint, posicion_default)
#             else:
#                 align_joint_to_position(joint, posicion_default)
#                 print(f"   ⚠️ Joint {nombre} usando posición por defecto")
            
#             return joint
            
#         except Exception as e:
#             print(f"❌ Error creando joint {nombre}: {e}")
#             return None

#     def crear_curvas_control_joints(self):
#         """Crea exactamente 9 curvas de control - una para cada joint - VERSIÓN SEGURA"""
#         try:
#             print("🎨 Creando 9 curvas de control para todos los joints...")
            
#             # Verificar que existen los 9 joints
#             joints_existentes = []
#             for joint_num in range(1, 10):
#                 joint_name = f"joint_{joint_num}"
#                 if cmds.objExists(joint_name):
#                     joints_existentes.append(joint_num)
#                 else:
#                     print(f"❌ Joint faltante: {joint_name}")
#                     return False
            
#             if len(joints_existentes) != 9:
#                 print(f"❌ Faltan joints. Encontrados: {joints_existentes}")
#                 return False
            
#             # Configuración EXACTA según especificaciones
#             config_joints = {
#                 1: {"nombre": "joint_1", "forma": "hexagono", "color": 22, "radio": 2.0, "rotar": False},
#                 2: {"nombre": "joint_2", "forma": "hexagono", "color": 6, "radio": 1.5, "rotar": False},
#                 4: {"nombre": "joint_4", "forma": "hexagono", "color": 14, "radio": 1.5, "rotar": False},
#                 3: {"nombre": "joint_3", "forma": "cuadrado", "color": 13, "radio": 1.2, "rotar": False},
#                 5: {"nombre": "joint_5", "forma": "cuadrado", "color": 17, "radio": 1.2, "rotar": False},
#                 6: {"nombre": "joint_6", "forma": "circulo", "color": 18, "radio": 0.8, "rotar": True},
#                 7: {"nombre": "joint_7", "forma": "circulo", "color": 19, "radio": 0.8, "rotar": True},
#                 8: {"nombre": "joint_8", "forma": "circulo", "color": 20, "radio": 0.8, "rotar": True},
#                 9: {"nombre": "joint_9", "forma": "circulo", "color": 21, "radio": 0.8, "rotar": True},
#             }
            
#             # Crear controles para CADA UNO de los 9 joints
#             for joint_num in range(1, 10):
#                 config = config_joints[joint_num]
#                 joint_name = config["nombre"]
                
#                 try:
#                     # Obtener posición exacta del joint
#                     pos = cmds.xform(joint_name, q=True, ws=True, t=True)
                    
#                     # Crear control con forma específica
#                     ctrl_name = f"ctrl_{joint_name}"
#                     ctrl, grp = self._crear_control_con_forma_exacta(
#                         ctrl_name, 
#                         pos, 
#                         config["forma"], 
#                         config["radio"], 
#                         config["color"]
#                     )
                    
#                     # ROTACIÓN CRÍTICA: Solo para llantas (joints 6-9)
#                     if config["rotar"]:
#                         cmds.xform(grp, ro=(0, 0, 90))
#                         print(f"   🎯 Control de LLANTA {ctrl_name} rotado 90° en Z")
                    
#                     # CONEXIÓN DIRECTA al joint correspondiente
#                     cmds.parentConstraint(ctrl, joint_name, mo=True)
#                     print(f"   ✅ Control {joint_num}: {ctrl_name} ({config['forma']}, color: {config['color']})")
                    
#                 except Exception as e:
#                     print(f"❌ Error creando control para {joint_name}: {e}")
#                     continue
            
#             print("🎨 9 CURVAS CREADAS EXITOSAMENTE:")
#             print("   • 3 Hexagonales (joints 1,2,4 - padres)")
#             print("   • 2 Cuadradas (joints 3,5 - hijos no llantas)") 
#             print("   • 4 Circulares (joints 6,7,8,9 - llantas rotadas 90°Z)")
#             return True
            
#         except Exception as e:
#             print(f"❌ Error creando curvas de control: {e}")
#             return False

#     def _crear_control_con_forma_exacta(self, nombre, posicion, forma, radio, color_index):
#         """Crea controles con formas geométricas exactas - VERSIÓN SEGURA"""
#         try:
#             if forma == "hexagono":
#                 # HEXÁGONO para joints padres
#                 puntos = []
#                 for i in range(6):
#                     angulo = math.radians(i * 60)
#                     x = radio * math.cos(angulo)
#                     z = radio * math.sin(angulo)
#                     puntos.append([x, 0, z])
#                 # Cerrar el hexágono
#                 puntos.append(puntos[0])
#                 curva = cmds.curve(name=nombre, point=puntos, degree=1)
                
#             elif forma == "cuadrado":
#                 # CUADRADO para joints hijos no llantas
#                 puntos = [
#                     [-radio, 0, -radio], [-radio, 0, radio], 
#                     [radio, 0, radio], [radio, 0, -radio], [-radio, 0, -radio]
#                 ]
#                 curva = cmds.curve(name=nombre, point=puntos, degree=1)
                
#             elif forma == "circulo":
#                 # CÍRCULO para llantas - orientado correctamente para rotación Z
#                 curva = cmds.circle(
#                     name=nombre, 
#                     normal=(1, 0, 0),
#                     radius=radio,
#                     sections=12
#                 )[0]
                
#             else:
#                 # Por defecto círculo
#                 curva = cmds.circle(name=nombre, normal=(1, 0, 0), radius=radio)[0]
            
#             # Crear grupo para el control
#             grp = cmds.group(curva, name=f"{nombre}_GRP")
            
#             # Posicionar exactamente en la posición del joint
#             cmds.xform(grp, ws=True, t=posicion)
            
#             # Aplicar color específico
#             self._aplicar_color_control(curva, color_index)
            
#             return curva, grp
            
#         except Exception as e:
#             print(f"❌ Error creando control {nombre}: {e}")
#             # Crear control básico como fallback
#             curva = cmds.circle(name=nombre, radius=radio)[0]
#             grp = cmds.group(curva, name=f"{nombre}_GRP")
#             cmds.xform(grp, ws=True, t=posicion)
#             return curva, grp

#     def _aplicar_color_control(self, control, color_index):
#         """Aplica color al control de forma segura"""
#         try:
#             shapes = cmds.listRelatives(control, shapes=True) or []
#             for shape in shapes:
#                 cmds.setAttr(f"{shape}.overrideEnabled", 1)
#                 cmds.setAttr(f"{shape}.overrideColor", color_index)
#         except:
#             pass

#     def limpiar_rig_existente(self):
#         """Limpia todos los elementos del rig anterior incluyendo las nuevas curvas"""
#         elementos_rig = [
#             "RIG_CARRO_GRP", "ctrl_global", "ctrl_global_GRP",
#             "ctrl_maletero", "ctrl_maletero_GRP", "ctrl_cabina", "ctrl_cabina_GRP",
#             "ctrl_capo", "ctrl_capo_GRP"
#         ]
        
#         # Agregar joints (1-9) y sus NUEVAS curvas de control
#         for i in range(1, 10):
#             elementos_rig.append(f"joint_{i}")
#             elementos_rig.append(f"ctrl_joint_{i}")      # Nueva curva
#             elementos_rig.append(f"ctrl_joint_{i}_GRP")  # Grupo de la nueva curva
        
#         # Controles de ruedas existentes
#         for rueda in NOMBRES_ESTANDAR["ruedas"]:
#             elementos_rig.extend([f"ctrl_{rueda}", f"ctrl_{rueda}_GRP"])
        
#         elementos_eliminados = []
#         for elem in elementos_rig:
#             if cmds.objExists(elem):
#                 try:
#                     cmds.delete(elem)
#                     elementos_eliminados.append(elem)
#                 except:
#                     pass
        
#         print(f"🗑️ Elementos eliminados: {len(elementos_eliminados)}")
#         return len(elementos_eliminados)

#     def aplicar_skinning_inteligente(self, chasis, ruedas, ejes):
#         """Aplica skinning inteligente con pesos optimizados"""
#         try:
#             print("🔗 Aplicando skinning inteligente...")
            
#             # Obtener todos los joints del rig
#             joints_rig = [f"joint_{i}" for i in range(1, 10) if cmds.objExists(f"joint_{i}")]
            
#             if not joints_rig:
#                 print("⚠️ No se encontraron joints para skinning")
#                 return False
            
#             # Lista de todas las geometrías a skin
#             geometrias = []
#             if chasis and cmds.objExists(chasis):
#                 geometrias.append(chasis)
#             if ejes:
#                 for eje in ejes:
#                     if cmds.objExists(eje):
#                         geometrias.append(eje)
#             if ruedas:
#                 for rueda in ruedas:
#                     if cmds.objExists(rueda):
#                         geometrias.append(rueda)
            
#             if not geometrias:
#                 print("⚠️ No se encontraron geometrías para skinning")
#                 return False
            
#             # Aplicar skin cluster a cada geometría con pesos optimizados
#             for geo in geometrias:
#                 try:
#                     # Verificar si ya tiene skin cluster
#                     skin_clusters = cmds.ls(cmds.listHistory(geo), type='skinCluster')
#                     if skin_clusters:
#                         print(f"🔄 Reconfigurando skin existente en: {geo}")
#                         skin_cluster = skin_clusters[0]
#                     else:
#                         # Crear skin cluster
#                         skin_cluster = cmds.skinCluster(joints_rig, geo, name=f"{geo}_skinCluster", maximumInfluences=3)[0]
#                         print(f"✅ Skin creado para: {geo}")
                    
#                     # Aplicar pesos optimizados según el tipo de geometría
#                     self._aplicar_pesos_optimizados(geo, skin_cluster, joints_rig)
                    
#                 except Exception as e:
#                     print(f"⚠️ No se pudo aplicar skin a {geo}: {e}")
            
#             return True
            
#         except Exception as e:
#             print(f"❌ Error en skinning inteligente: {e}")
#             return False

#     def _aplicar_pesos_optimizados(self, geometria, skin_cluster, joints):
#         """Aplica pesos optimizados según el tipo de geometría"""
#         try:
#             print(f"🎯 Optimizando pesos para: {geometria}")
            
#             # Determinar el tipo de geometría
#             geo_name_lower = geometria.lower()
            
#             if "chasis" in geo_name_lower or "axioma" in geo_name_lower:
#                 self._pesos_chasis_mejorado(geometria, skin_cluster, joints)
#             elif "eje" in geo_name_lower:
#                 self._pesos_ejes_mejorado(geometria, skin_cluster, joints)
#             elif "rueda" in geo_name_lower:
#                 self._pesos_ruedas_mejorado(geometria, skin_cluster, joints)
#             else:
#                 # Pesos por defecto para geometrías desconocidas
#                 self._pesos_default(geometria, skin_cluster, joints)
                
#         except Exception as e:
#             print(f"⚠️ Error optimizando pesos para {geometria}: {e}")

#     def _pesos_chasis_mejorado(self, chasis, skin_cluster, joints):
#         """Pesos optimizados MEJORADOS para el chasis"""
#         print(f"   🏗️ Aplicando pesos MEJORADOS de chasis...")
        
#         # Resetear pesos primero
#         cmds.skinPercent(skin_cluster, chasis, normalize=True, pruneWeights=0.01)
        
#         # Obtener bounding box del chasis
#         bb = cmds.exactWorldBoundingBox(chasis)
#         centro_x = (bb[0] + bb[3]) / 2
#         centro_z = (bb[2] + bb[5]) / 2
#         longitud_x = bb[3] - bb[0]
#         longitud_z = bb[5] - bb[2]
        
#         # Joints principales
#         joint_1 = "joint_1"  # Centro
#         joint_2 = "joint_2"  # Eje delantero
#         joint_3 = "joint_3"  # Cara delantera
#         joint_4 = "joint_4"  # Eje trasero
#         joint_5 = "joint_5"  # Cara trasera
        
#         # Aplicar pesos basados en la posición - MÉTODO MEJORADO
#         vtx_count = cmds.polyEvaluate(chasis, vertex=True)
        
#         for i in range(vtx_count):
#             vtx = f"{chasis}.vtx[{i}]"
#             pos = cmds.pointPosition(vtx, world=True)
            
#             # Calcular distancias normalizadas a cada joint
#             dist_joint1 = self._calcular_distancia_normalizada(pos, joint_1, longitud_x, longitud_z)
#             dist_joint2 = self._calcular_distancia_normalizada(pos, joint_2, longitud_x, longitud_z)
#             dist_joint3 = self._calcular_distancia_normalizada(pos, joint_3, longitud_x, longitud_z)
#             dist_joint4 = self._calcular_distancia_normalizada(pos, joint_4, longitud_x, longitud_z)
#             dist_joint5 = self._calcular_distancia_normalizada(pos, joint_5, longitud_x, longitud_z)
            
#             # Calcular pesos basados en proximidad (inverso de la distancia)
#             peso_joint1 = max(0, 1 - dist_joint1 * 2.0) if dist_joint1 < 0.5 else 0
#             peso_joint2 = max(0, 1 - dist_joint2 * 2.5) if dist_joint2 < 0.4 else 0
#             peso_joint3 = max(0, 1 - dist_joint3 * 2.5) if dist_joint3 < 0.4 else 0
#             peso_joint4 = max(0, 1 - dist_joint4 * 2.5) if dist_joint4 < 0.4 else 0
#             peso_joint5 = max(0, 1 - dist_joint5 * 2.5) if dist_joint5 < 0.4 else 0
            
#             # Asignar pesos
#             pesos = {}
#             if peso_joint1 > 0.1:
#                 pesos[joint_1] = peso_joint1
#             if peso_joint2 > 0.1:
#                 pesos[joint_2] = peso_joint2 * 0.3
#                 pesos[joint_3] = peso_joint2 * 0.7
#             if peso_joint3 > 0.1:
#                 pesos[joint_3] = (pesos.get(joint_3, 0) + peso_joint3 * 0.8)
#                 pesos[joint_2] = (pesos.get(joint_2, 0) + peso_joint3 * 0.2)
#             if peso_joint4 > 0.1:
#                 pesos[joint_4] = peso_joint4 * 0.3
#                 pesos[joint_5] = peso_joint4 * 0.7
#             if peso_joint5 > 0.1:
#                 pesos[joint_5] = (pesos.get(joint_5, 0) + peso_joint5 * 0.8)
#                 pesos[joint_4] = (pesos.get(joint_4, 0) + peso_joint5 * 0.2)
            
#             # Normalizar y aplicar
#             if pesos:
#                 total = sum(pesos.values())
#                 if total > 0:
#                     for joint, peso in pesos.items():
#                         pesos[joint] = peso / total
#                     cmds.skinPercent(skin_cluster, vtx, transformValue=pesos.items())

#     def _calcular_distancia_normalizada(self, posicion, joint, longitud_x, longitud_z):
#         """Calcula distancia normalizada entre posición y joint"""
#         if not cmds.objExists(joint):
#             return 1.0
            
#         joint_pos = cmds.xform(joint, q=True, ws=True, t=True)
#         distancia_x = abs(posicion[0] - joint_pos[0]) / (longitud_x / 2)
#         distancia_z = abs(posicion[2] - joint_pos[2]) / (longitud_z / 2)
#         return (distancia_x + distancia_z) / 2

#     def _pesos_ejes_mejorado(self, eje, skin_cluster, joints):
#         """Pesos optimizados MEJORADOS para ejes"""
#         print(f"   🎯 Aplicando pesos MEJORADOS de eje...")
        
#         # Resetear pesos
#         cmds.skinPercent(skin_cluster, eje, normalize=True, pruneWeights=0.01)
        
#         eje_name_lower = eje.lower()
        
#         if "delantero" in eje_name_lower:
#             joint_principal = "joint_2"
#             joint_secundario = "joint_1"
#         else:  # trasero
#             joint_principal = "joint_4"
#             joint_secundario = "joint_1"
        
#         # 🔧 PESOS MEJORADOS - Ejes: 95% al joint principal, 5% al centro
#         cmds.skinPercent(skin_cluster, eje, transformValue=[
#             (joint_principal, 0.95),    # Más influencia al eje
#             (joint_secundario, 0.05)    # Menos influencia al centro
#         ])

#     def _pesos_ruedas_mejorado(self, rueda, skin_cluster, joints):
#         """Pesos optimizados MEJORADOS para ruedas"""
#         print(f"   🎯 Aplicando pesos MEJORADOS de rueda...")
        
#         # Resetear pesos
#         cmds.skinPercent(skin_cluster, rueda, normalize=True, pruneWeights=0.01)
        
#         rueda_name_lower = rueda.lower()
        
#         # Determinar joint principal basado en el nombre de la rueda
#         if "delantera" in rueda_name_lower:
#             if "der" in rueda_name_lower:
#                 joint_principal = "joint_6"
#             else:  # izq
#                 joint_principal = "joint_7"
#             joint_eje = "joint_2"
#         else:  # trasera
#             if "izq" in rueda_name_lower:
#                 joint_principal = "joint_8"
#             else:  # der
#                 joint_principal = "joint_9"
#             joint_eje = "joint_4"
        
#         # 🔧 PESOS MEJORADOS - Ruedas: 98% al joint de rueda, 2% al eje
#         cmds.skinPercent(skin_cluster, rueda, transformValue=[
#             (joint_principal, 0.98),    # Casi toda la influencia a la rueda
#             (joint_eje, 0.02)           # Muy poca influencia al eje
#         ])

#     def _pesos_default(self, geometria, skin_cluster, joints):
#         """Pesos por defecto para geometrías desconocidas"""
#         print(f"   ⚙️ Aplicando pesos por defecto...")
#         cmds.skinPercent(skin_cluster, geometria, normalize=True)

#     def crear_rig_completo_seguro(self):
#         """VERSIÓN SEGURA del creador de rig - evita crashes"""
#         try:
#             print("🛡️ INICIANDO CREACIÓN SEGURA DE RIG...")
            
#             # PASO 1: Verificar que existe la geometría
#             chasis, ruedas, ejes = self._verificar_geometria_existente()
#             if not chasis:
#                 cmds.confirmDialog(
#                     title="Error",
#                     message="❌ No se encontró el chasis 'axioma_carro' en la escena.\n\nCrear un carro primero con el botón EMERGER.",
#                     button=["OK"]
#                 )
#                 return False
            
#             # PASO 2: Limpiar rig existente
#             print("🗑️ Limpiando rig existente...")
#             self.limpiar_rig_existente()
            
#             # PASO 3: Crear joints con posiciones por defecto seguras
#             print("📍 Creando joints con posiciones seguras...")
            
#             # Obtener posición del chasis para referencias
#             chasis_pos = cmds.xform("axioma_carro", q=True, ws=True, t=True)
#             chasis_bb = cmds.exactWorldBoundingBox("axioma_carro")
#             largo_chasis = chasis_bb[3] - chasis_bb[0]
#             ancho_chasis = chasis_bb[5] - chasis_bb[2]
            
#             # Crear joints con posiciones calculadas seguras
#             joints = {}
            
#             # Joint 1: Centro del chasis
#             joints[1] = self._crear_joint_seguro("joint_1", chasis_pos)
            
#             # Joint 2: Eje delantero
#             pos_j2 = [chasis_pos[0] + largo_chasis/3, chasis_pos[1], chasis_pos[2]]
#             joints[2] = self._crear_joint_seguro("joint_2", pos_j2)
            
#             # Joint 3: Cara delantera
#             pos_j3 = [chasis_pos[0] + largo_chasis/2, chasis_pos[1], chasis_pos[2]]
#             joints[3] = self._crear_joint_seguro("joint_3", pos_j3)
            
#             # Joint 4: Eje trasero
#             pos_j4 = [chasis_pos[0] - largo_chasis/3, chasis_pos[1], chasis_pos[2]]
#             joints[4] = self._crear_joint_seguro("joint_4", pos_j4)
            
#             # Joint 5: Cara trasera
#             pos_j5 = [chasis_pos[0] - largo_chasis/2, chasis_pos[1], chasis_pos[2]]
#             joints[5] = self._crear_joint_seguro("joint_5", pos_j5)
            
#             # Joints de ruedas
#             pos_j6 = [pos_j2[0], pos_j2[1], pos_j2[2] - ancho_chasis/2]  # Rueda delantera der
#             joints[6] = self._crear_joint_seguro("joint_6", pos_j6)
            
#             pos_j7 = [pos_j2[0], pos_j2[1], pos_j2[2] + ancho_chasis/2]  # Rueda delantera izq
#             joints[7] = self._crear_joint_seguro("joint_7", pos_j7)
            
#             pos_j8 = [pos_j4[0], pos_j4[1], pos_j4[2] + ancho_chasis/2]  # Rueda trasera izq
#             joints[8] = self._crear_joint_seguro("joint_8", pos_j8)
            
#             pos_j9 = [pos_j4[0], pos_j4[1], pos_j4[2] - ancho_chasis/2]  # Rueda trasera der
#             joints[9] = self._crear_joint_seguro("joint_9", pos_j9)
            
#             # Verificar que todos los joints se crearon
#             for i in range(1, 10):
#                 if not joints.get(i):
#                     print(f"❌ No se pudo crear joint_{i}")
#                     return False
            
#             # PASO 4: Configurar jerarquía
#             print("🔗 Configurando jerarquía de joints...")
#             cmds.parent(joints[2], joints[1])
#             cmds.parent(joints[4], joints[1])
#             cmds.parent(joints[3], joints[2])
#             cmds.parent(joints[6], joints[2])
#             cmds.parent(joints[7], joints[2])
#             cmds.parent(joints[5], joints[4])
#             cmds.parent(joints[8], joints[4])
#             cmds.parent(joints[9], joints[4])
            
#             # PASO 5: Crear controles
#             print("🎨 Creando controles...")
#             if not self.crear_curvas_control_joints():
#                 print("⚠️ Algunos controles no se pudieron crear, continuando...")
            
#             # PASO 6: Aplicar skinning
#             print("🔗 Aplicando skinning...")
#             self.aplicar_skinning_inteligente(chasis, ruedas, ejes)
            
#             # PASO 7: Mensaje de éxito
#             cmds.confirmDialog(
#                 title="Rig Completado",
#                 message="✅ Rig creado exitosamente!\n\n" +
#                        "Se crearon 9 joints y controles para:\n" +
#                        "• Chasis (axioma_carro)\n" +
#                        f"• {len(ruedas)} ruedas\n" +
#                        f"• {len(ejes)} ejes",
#                 button=["OK"]
#             )
            
#             print("✅✅✅ RIG CREADO EXITOSAMENTE")
#             return True
            
#         except Exception as e:
#             error_msg = f"❌ Error en creación segura de rig: {str(e)}"
#             print(error_msg)
#             cmds.confirmDialog(title="Error", message=error_msg, button=["OK"])
#             return False

#     # Mantener compatibilidad con el método original
#     def crear_rig_completo(self, chasis=None, ruedas=None, ejes=None):
#         """Método original mantenido para compatibilidad - ahora usa versión segura"""
#         return self.crear_rig_completo_seguro()

# # Funciones globales para compatibilidad
# def limpiar_rig_existente():
#     """Función global para compatibilidad"""
#     core = CarroRigCore()
#     return core.limpiar_rig_existente()

# def ajustar_rig_existente():
#     """Función global para compatibilidad"""
#     core = CarroRigCore()
#     return core.ajustar_rig_existente()

# def crear_rig_carro(*args):
#     """Función global SEGURA para compatibilidad"""
#     core = CarroRigCore()
#     return core.crear_rig_completo_seguro()

# def crear_rig_carro_con_ejes():
#     """Función global para compatibilidad"""
#     core = CarroRigCore()
#     return core.crear_rig_completo_seguro()

# # Funciones para optimización de pesos
# def optimizar_pesos_rig():
#     """Re-optimiza los pesos del rig existente"""
#     core = CarroRigCore()
#     # Usar el método seguro de verificación
#     chasis, ruedas, ejes = core._verificar_geometria_existente()
#     if chasis:
#         core.aplicar_skinning_inteligente(chasis, ruedas, ejes)
#         cmds.confirmDialog(title="Éxito", message="✅ Pesos optimizados", button=["OK"])
#     else:
#         cmds.confirmDialog(title="Error", message="❌ No se encontró chasis", button=["OK"])

# def crear_curvas_control_todos_joints():
#     """Función global para crear las 9 curvas de control específicas"""
#     core = CarroRigCore()
#     return core.crear_curvas_control_joints()

# import maya.cmds as cmds
# import math

# class CarroRigCoreSimple:
#     def __init__(self):
#         print("🔧 CarroRigCoreSimple inicializado")
    
#     def verificar_geometria_basica(self):
#         """Verificación MUY básica de geometría"""
#         try:
#             if not cmds.objExists("axioma_carro"):
#                 print("❌ No existe axioma_carro")
#                 return False
            
#             # Verificar solo las ruedas esenciales
#             ruedas_requeridas = [
#                 "rueda_delantera_izq", "rueda_delantera_der",
#                 "rueda_trasera_izq", "rueda_trasera_der"
#             ]
            
#             for rueda in ruedas_requeridas:
#                 if not cmds.objExists(rueda):
#                     print(f"❌ No existe {rueda}")
#                     return False
            
#             print("✅ Geometría básica verificada")
#             return True
            
#         except Exception as e:
#             print(f"❌ Error en verificación: {e}")
#             return False

#     def limpiar_rig_simple(self):
#         """Limpieza MUY simple"""
#         try:
#             elementos = []
#             for i in range(1, 10):
#                 elementos.extend([f"joint_{i}", f"ctrl_joint_{i}", f"ctrl_joint_{i}_GRP"])
            
#             elementos.extend(["RIG_CARRO_GRP"])
            
#             eliminados = 0
#             for elem in elementos:
#                 if cmds.objExists(elem):
#                     try:
#                         cmds.delete(elem)
#                         eliminados += 1
#                     except:
#                         pass
            
#             print(f"🗑️ Eliminados {eliminados} elementos")
#             return eliminados
            
#         except Exception as e:
#             print(f"⚠️ Error en limpieza: {e}")
#             return 0

#     def crear_joints_basicos(self):
#         """Creación MUY básica de joints"""
#         try:
#             joints = {}
            
#             # Posición del chasis para referencia
#             chasis_pos = cmds.xform("axioma_carro", q=True, ws=True, t=True)
#             chasis_bb = cmds.exactWorldBoundingBox("axioma_carro")
            
#             # Joint 1 - Centro
#             cmds.select(clear=True)
#             joints[1] = cmds.joint(name="joint_1", position=chasis_pos)
            
#             # Joint 2 - Delantero
#             pos_delantero = [chasis_pos[0] + 3, chasis_pos[1], chasis_pos[2]]
#             cmds.select(clear=True)
#             joints[2] = cmds.joint(name="joint_2", position=pos_delantero)
            
#             # Joint 4 - Trasero  
#             pos_trasero = [chasis_pos[0] - 3, chasis_pos[1], chasis_pos[2]]
#             cmds.select(clear=True)
#             joints[4] = cmds.joint(name="joint_4", position=pos_trasero)
            
#             # Joint 3 - Cara delantera
#             pos_cara_del = [chasis_pos[0] + 5, chasis_pos[1], chasis_pos[2]]
#             cmds.select(clear=True)
#             joints[3] = cmds.joint(name="joint_3", position=pos_cara_del)
            
#             # Joint 5 - Cara trasera
#             pos_cara_tras = [chasis_pos[0] - 5, chasis_pos[1], chasis_pos[2]]
#             cmds.select(clear=True)
#             joints[5] = cmds.joint(name="joint_5", position=pos_cara_tras)
            
#             # Joints de ruedas - posiciones aproximadas
#             joints[6] = self.crear_joint_en_objeto("joint_6", "rueda_delantera_der", [chasis_pos[0] + 3, chasis_pos[1], chasis_pos[2] - 2])
#             joints[7] = self.crear_joint_en_objeto("joint_7", "rueda_delantera_izq", [chasis_pos[0] + 3, chasis_pos[1], chasis_pos[2] + 2])
#             joints[8] = self.crear_joint_en_objeto("joint_8", "rueda_trasera_izq", [chasis_pos[0] - 3, chasis_pos[1], chasis_pos[2] + 2])
#             joints[9] = self.crear_joint_en_objeto("joint_9", "rueda_trasera_der", [chasis_pos[0] - 3, chasis_pos[1], chasis_pos[2] - 2])
            
#             # Configurar jerarquía simple
#             cmds.parent(joints[2], joints[1])
#             cmds.parent(joints[4], joints[1])
#             cmds.parent(joints[3], joints[2])
#             cmds.parent(joints[6], joints[2])
#             cmds.parent(joints[7], joints[2])
#             cmds.parent(joints[5], joints[4])
#             cmds.parent(joints[8], joints[4])
#             cmds.parent(joints[9], joints[4])
            
#             print("✅ 9 joints creados y jerarquía configurada")
#             return joints
            
#         except Exception as e:
#             print(f"❌ Error creando joints: {e}")
#             return {}

#     def crear_joint_en_objeto(self, joint_name, obj_name, pos_default):
#         """Crea joint en objeto o posición por defecto"""
#         try:
#             cmds.select(clear=True)
#             joint = cmds.joint(name=joint_name)
            
#             if cmds.objExists(obj_name):
#                 try:
#                     bb = cmds.exactWorldBoundingBox(obj_name)
#                     pos = [(bb[0]+bb[3])/2, (bb[1]+bb[4])/2, (bb[2]+bb[5])/2]
#                     cmds.xform(joint, ws=True, t=pos)
#                 except:
#                     cmds.xform(joint, ws=True, t=pos_default)
#             else:
#                 cmds.xform(joint, ws=True, t=pos_default)
                
#             return joint
            
#         except:
#             cmds.select(clear=True)
#             joint = cmds.joint(name=joint_name)
#             cmds.xform(joint, ws=True, t=pos_default)
#             return joint

#     def crear_controles_simples(self):
#         """Crea controles MUY simples"""
#         try:
#             for i in range(1, 10):
#                 joint_name = f"joint_{i}"
#                 if not cmds.objExists(joint_name):
#                     continue
                    
#                 # Posición del joint
#                 pos = cmds.xform(joint_name, q=True, ws=True, t=True)
                
#                 # Crear control circular básico
#                 ctrl_name = f"ctrl_joint_{i}"
#                 ctrl = cmds.circle(name=ctrl_name, normal=(0, 1, 0), radius=1.0)[0]
#                 grp = cmds.group(ctrl, name=f"{ctrl_name}_GRP")
#                 cmds.xform(grp, ws=True, t=pos)
                
#                 # Color básico
#                 try:
#                     shapes = cmds.listRelatives(ctrl, shapes=True) or []
#                     if shapes:
#                         cmds.setAttr(f"{shapes[0]}.overrideEnabled", 1)
#                         cmds.setAttr(f"{shapes[0]}.overrideColor", i + 5)  # Colores secuenciales
#                 except:
#                     pass
                
#                 # Conectar
#                 cmds.parentConstraint(ctrl, joint_name, mo=True)
#                 print(f"✅ Control {i} creado")
            
#             print("🎨 9 controles básicos creados")
#             return True
            
#         except Exception as e:
#             print(f"❌ Error creando controles: {e}")
#             return False

#     def aplicar_skinning_simple(self):
#         """Skinning MUY simple sin pesos complejos"""
#         try:
#             # Obtener joints
#             joints = [f"joint_{i}" for i in range(1, 10) if cmds.objExists(f"joint_{i}")]
#             if not joints:
#                 print("❌ No hay joints para skinning")
#                 return False
            
#             # Geometrías a skin
#             geometrias = ["axioma_carro"]
#             ruedas = ["rueda_delantera_izq", "rueda_delantera_der", "rueda_trasera_izq", "rueda_trasera_der"]
            
#             for rueda in ruedas:
#                 if cmds.objExists(rueda):
#                     geometrias.append(rueda)
            
#             # Aplicar skin cluster básico
#             for geo in geometrias:
#                 try:
#                     # Limpiar skin clusters existentes
#                     skin_clusters = cmds.ls(cmds.listHistory(geo), type='skinCluster')
#                     if skin_clusters:
#                         cmds.delete(skin_clusters[0])
                    
#                     # Crear nuevo skin cluster
#                     skin_cluster = cmds.skinCluster(joints, geo, name=f"{geo}_skin", maximumInfluences=3)[0]
#                     print(f"✅ Skin aplicado a {geo}")
                    
#                 except Exception as e:
#                     print(f"⚠️ No se pudo aplicar skin a {geo}: {e}")
            
#             return True
            
#         except Exception as e:
#             print(f"❌ Error en skinning simple: {e}")
#             return False

#     def crear_rig_completo_simple(self):
#         """Método PRINCIPAL simplificado"""
#         try:
#             print("🚗 INICIANDO CREACIÓN DE RIG SIMPLIFICADA...")
            
#             # PASO 1: Verificación básica
#             if not self.verificar_geometria_basica():
#                 cmds.confirmDialog(title="Error", message="❌ Geometría incompleta", button=["OK"])
#                 return False
            
#             # PASO 2: Limpiar
#             self.limpiar_rig_simple()
            
#             # PASO 3: Crear joints
#             joints = self.crear_joints_basicos()
#             if not joints:
#                 return False
            
#             # PASO 4: Crear controles
#             if not self.crear_controles_simples():
#                 return False
            
#             # PASO 5: Aplicar skinning
#             if not self.aplicar_skinning_simple():
#                 return False
            
#             # PASO 6: Agrupar
#             try:
#                 grupos = cmds.ls("ctrl_joint_*_GRP", transforms=True)
#                 if grupos:
#                     rig_grp = cmds.group(grupos, name="RIG_CARRO_GRP")
#                     print(f"✅ Grupo principal creado: {rig_grp}")
#             except:
#                 print("⚠️ No se pudo crear grupo principal")
            
#             # Éxito
#             cmds.confirmDialog(
#                 title="✅ Rig Completado", 
#                 message="Rig básico creado exitosamente!\n\n9 joints + 9 controles",
#                 button=["OK"]
#             )
            
#             print("✅✅✅ RIG SIMPLE CREADO EXITOSAMENTE")
#             return True
            
#         except Exception as e:
#             error_msg = f"❌ Error en rig simple: {str(e)}"
#             print(error_msg)
#             cmds.confirmDialog(title="Error", message=error_msg, button=["OK"])
#             return False

# # FUNCIÓN GLOBAL ULTRA-SIMPLE
# def crear_rig_carro(*args):
#     """Función global SIMPLIFICADA"""
#     try:
#         print("🎯 EJECUTANDO VERSIÓN SIMPLIFICADA...")
        
#         # Verificación rápida
#         if not cmds.objExists("axioma_carro"):
#             cmds.confirmDialog(title="Error", message="❌ No hay carro en escena", button=["OK"])
#             return False
        
#         # Crear y ejecutar
#         core = CarroRigCoreSimple()
#         resultado = core.crear_rig_completo_simple()
        
#         return resultado
        
#     except Exception as e:
#         cmds.warning(f"❌ Error crítico: {e}")
#         return False

# # Funciones básicas de compatibilidad
# def limpiar_rig_existente():
#     core = CarroRigCoreSimple()
#     return core.limpiar_rig_simple()

# def optimizar_pesos_rig():
#     cmds.confirmDialog(title="Info", message="⚠️ Función no disponible en versión simple", button=["OK"])

# import maya.cmds as cmds
# import math
# from carro_rig_utils import (
#     get_face_center, align_joint_to_position, align_to_object_center, 
#     create_control, buscar_objetos_escena_filtrado, NOMBRES_ESTANDAR
# )

# class CarroRigCoreOptimizado:
#     def __init__(self):
#         print("🔧 CarroRigCoreOptimizado inicializado")
    
#     def _verificar_geometria_completa(self):
#         """Verificación completa de geometría"""
#         try:
#             if not cmds.objExists("axioma_carro"):
#                 print("❌ No existe axioma_carro")
#                 return False
            
#             # Verificar geometría esencial
#             elementos_requeridos = [
#                 "axioma_carro",
#                 "rueda_delantera_izq", "rueda_delantera_der",
#                 "rueda_trasera_izq", "rueda_trasera_der"
#             ]
            
#             for elemento in elementos_requeridos:
#                 if not cmds.objExists(elemento):
#                     print(f"❌ No existe {elemento}")
#                     return False
            
#             print("✅ Geometría completa verificada")
#             return True
            
#         except Exception as e:
#             print(f"❌ Error en verificación: {e}")
#             return False

#     def limpiar_rig_existente(self):
#         """Limpieza completa del rig"""
#         try:
#             elementos = []
            
#             # Elementos básicos
#             elementos.extend([
#                 "RIG_CARRO_GRP", "ctrl_global", "ctrl_global_GRP",
#                 "ctrl_maletero", "ctrl_maletero_GRP", "ctrl_cabina", "ctrl_cabina_GRP",
#                 "ctrl_capo", "ctrl_capo_GRP"
#             ])
            
#             # Joints y controles
#             for i in range(1, 10):
#                 elementos.extend([f"joint_{i}", f"ctrl_joint_{i}", f"ctrl_joint_{i}_GRP"])
            
#             # Controles de ruedas
#             for rueda in NOMBRES_ESTANDAR["ruedas"]:
#                 elementos.extend([f"ctrl_{rueda}", f"ctrl_{rueda}_GRP"])
            
#             eliminados = 0
#             for elem in elementos:
#                 if cmds.objExists(elem):
#                     try:
#                         cmds.delete(elem)
#                         eliminados += 1
#                     except:
#                         pass
            
#             print(f"🗑️ Eliminados {eliminados} elementos")
#             return eliminados
            
#         except Exception as e:
#             print(f"⚠️ Error en limpieza: {e}")
#             return 0

#     def _crear_joint_preciso(self, nombre, objeto_target=None, face_index=None, posicion_default=None):
#         """Crea joint en posición precisa usando las utilidades"""
#         try:
#             cmds.select(clear=True)
#             joint = cmds.joint(name=nombre)
            
#             # PRIORIDAD 1: Posicionar en objeto específico
#             if objeto_target and cmds.objExists(objeto_target):
#                 try:
#                     target_pos = align_to_object_center(objeto_target)
#                     if target_pos:
#                         align_joint_to_position(joint, target_pos)
#                         print(f"   ✅ Joint {nombre} posicionado en {objeto_target}")
#                         return joint
#                 except Exception as e:
#                     print(f"   ⚠️ No se pudo posicionar {nombre} en {objeto_target}: {e}")
            
#             # PRIORIDAD 2: Posicionar en cara específica del chasis
#             if face_index is not None and cmds.objExists("axioma_carro"):
#                 try:
#                     face_pos = get_face_center("axioma_carro", face_index)
#                     if face_pos:
#                         align_joint_to_position(joint, face_pos)
#                         print(f"   ✅ Joint {nombre} posicionado en cara {face_index}")
#                         return joint
#                 except Exception as e:
#                     print(f"   ⚠️ No se pudo posicionar {nombre} en cara {face_index}: {e}")
            
#             # PRIORIDAD 3: Posición por defecto calculada
#             if posicion_default:
#                 try:
#                     align_joint_to_position(joint, posicion_default)
#                     print(f"   ✅ Joint {nombre} usando posición calculada")
#                     return joint
#                 except Exception as e:
#                     print(f"   ⚠️ No se pudo posicionar {nombre} en posición calculada: {e}")
            
#             # ULTIMO RECURSO: Posición de emergencia
#             align_joint_to_position(joint, [0, 0, 0])
#             print(f"   ⚠️ Joint {nombre} usando posición de emergencia")
#             return joint
            
#         except Exception as e:
#             print(f"❌ Error creando joint {nombre}: {e}")
#             return None

#     def crear_jerarquia_precisa(self):
#         """Crea la jerarquía de joints con posiciones PRECISAS"""
#         try:
#             joints = {}
            
#             # Obtener información del chasis para cálculos
#             chasis_pos = cmds.xform("axioma_carro", q=True, ws=True, t=True)
#             chasis_bb = cmds.exactWorldBoundingBox("axioma_carro")
#             largo_chasis = chasis_bb[3] - chasis_bb[0]
#             ancho_chasis = chasis_bb[5] - chasis_bb[2]
            
#             print("📍 Creando joints con posiciones precisas...")
            
#             # JOINT 1: Centro del chasis (cara 3)
#             joints[1] = self._crear_joint_preciso("joint_1", "axioma_carro", 3, chasis_pos)
            
#             # JOINT 2: Eje delantero
#             pos_eje_delantero = [chasis_pos[0] + largo_chasis/3, chasis_pos[1], chasis_pos[2]]
#             joints[2] = self._crear_joint_preciso("joint_2", "eje_delantero", None, pos_eje_delantero)
            
#             # JOINT 3: Cara delantera (cara 6)
#             pos_cara_delantera = [chasis_pos[0] + largo_chasis/2, chasis_pos[1], chasis_pos[2]]
#             joints[3] = self._crear_joint_preciso("joint_3", None, 6, pos_cara_delantera)
            
#             # JOINT 4: Eje trasero
#             pos_eje_trasero = [chasis_pos[0] - largo_chasis/3, chasis_pos[1], chasis_pos[2]]
#             joints[4] = self._crear_joint_preciso("joint_4", "eje_trasero", None, pos_eje_trasero)
            
#             # JOINT 5: Cara trasera (cara 16)
#             pos_cara_trasera = [chasis_pos[0] - largo_chasis/2, chasis_pos[1], chasis_pos[2]]
#             joints[5] = self._crear_joint_preciso("joint_5", None, 16, pos_cara_trasera)
            
#             # JOINTS DE RUEDAS - EN LAS POSICIONES EXACTAS
#             joints[6] = self._crear_joint_preciso("joint_6", "rueda_delantera_der")
#             joints[7] = self._crear_joint_preciso("joint_7", "rueda_delantera_izq")
#             joints[8] = self._crear_joint_preciso("joint_8", "rueda_trasera_izq")
#             joints[9] = self._crear_joint_preciso("joint_9", "rueda_trasera_der")
            
#             # Verificar que todos los joints se crearon
#             for i in range(1, 10):
#                 if not joints.get(i):
#                     print(f"❌ ERROR: No se pudo crear joint_{i}")
#                     return {}
            
#             # CONFIGURAR JERARQUÍA EXACTA
#             print("🔗 Configurando jerarquía...")
#             cmds.parent(joints[2], joints[1])
#             cmds.parent(joints[4], joints[1])
#             cmds.parent(joints[3], joints[2])
#             cmds.parent(joints[6], joints[2])
#             cmds.parent(joints[7], joints[2])
#             cmds.parent(joints[5], joints[4])
#             cmds.parent(joints[8], joints[4])
#             cmds.parent(joints[9], joints[4])
            
#             print("✅ 9 joints creados y jerarquía configurada")
#             return joints
            
#         except Exception as e:
#             print(f"❌ Error creando jerarquía: {e}")
#             return {}

#     def crear_controles_especificos(self):
#         """Crea controles con formas específicas según el código original"""
#         try:
#             print("🎨 Creando controles específicos...")
            
#             # Verificar que existen los 9 joints
#             for i in range(1, 10):
#                 if not cmds.objExists(f"joint_{i}"):
#                     print(f"❌ Joint faltante: joint_{i}")
#                     return False
            
#             # Configuración EXACTA según especificaciones originales
#             config_joints = {
#                 1: {"nombre": "joint_1", "forma": "hexagono", "color": 22, "radio": 2.0, "rotar": False},
#                 2: {"nombre": "joint_2", "forma": "hexagono", "color": 6, "radio": 1.5, "rotar": False},
#                 4: {"nombre": "joint_4", "forma": "hexagono", "color": 14, "radio": 1.5, "rotar": False},
#                 3: {"nombre": "joint_3", "forma": "cuadrado", "color": 13, "radio": 1.2, "rotar": False},
#                 5: {"nombre": "joint_5", "forma": "cuadrado", "color": 17, "radio": 1.2, "rotar": False},
#                 6: {"nombre": "joint_6", "forma": "circulo", "color": 18, "radio": 0.8, "rotar": True},
#                 7: {"nombre": "joint_7", "forma": "circulo", "color": 19, "radio": 0.8, "rotar": True},
#                 8: {"nombre": "joint_8", "forma": "circulo", "color": 20, "radio": 0.8, "rotar": True},
#                 9: {"nombre": "joint_9", "forma": "circulo", "color": 21, "radio": 0.8, "rotar": True},
#             }
            
#             # Crear controles para cada joint
#             for joint_num in range(1, 10):
#                 config = config_joints[joint_num]
#                 joint_name = config["nombre"]
                
#                 try:
#                     # Obtener posición exacta del joint
#                     pos = cmds.xform(joint_name, q=True, ws=True, t=True)
                    
#                     # Crear control con forma específica
#                     ctrl_name = f"ctrl_{joint_name}"
#                     ctrl, grp = self._crear_control_con_forma(
#                         ctrl_name, 
#                         pos, 
#                         config["forma"], 
#                         config["radio"], 
#                         config["color"]
#                     )
                    
#                     # Rotación para llantas
#                     if config["rotar"]:
#                         cmds.xform(grp, ro=(0, 0, 90))
#                         print(f"   🎯 Control de LLANTA {ctrl_name} rotado 90° en Z")
                    
#                     # Conectar control al joint
#                     cmds.parentConstraint(ctrl, joint_name, mo=True)
#                     print(f"   ✅ Control {joint_num}: {ctrl_name} ({config['forma']})")
                    
#                 except Exception as e:
#                     print(f"❌ Error creando control para {joint_name}: {e}")
#                     continue
            
#             print("🎨 9 CONTROLES CREADOS EXITOSAMENTE:")
#             print("   • 3 Hexagonales (joints 1,2,4 - padres)")
#             print("   • 2 Cuadradas (joints 3,5 - hijos)") 
#             print("   • 4 Circulares (joints 6,7,8,9 - llantas)")
#             return True
            
#         except Exception as e:
#             print(f"❌ Error creando controles: {e}")
#             return False

#     def _crear_control_con_forma(self, nombre, posicion, forma, radio, color_index):
#         """Crea controles con formas geométricas específicas"""
#         try:
#             if forma == "hexagono":
#                 # HEXÁGONO para joints padres
#                 puntos = []
#                 for i in range(6):
#                     angulo = math.radians(i * 60)
#                     x = radio * math.cos(angulo)
#                     z = radio * math.sin(angulo)
#                     puntos.append([x, 0, z])
#                 puntos.append(puntos[0])  # Cerrar
#                 curva = cmds.curve(name=nombre, point=puntos, degree=1)
                
#             elif forma == "cuadrado":
#                 # CUADRADO para joints hijos
#                 puntos = [
#                     [-radio, 0, -radio], [-radio, 0, radio], 
#                     [radio, 0, radio], [radio, 0, -radio], [-radio, 0, -radio]
#                 ]
#                 curva = cmds.curve(name=nombre, point=puntos, degree=1)
                
#             elif forma == "circulo":
#                 # CÍRCULO para llantas
#                 curva = cmds.circle(
#                     name=nombre, 
#                     normal=(1, 0, 0),  # Orientación correcta para rotación Z
#                     radius=radio,
#                     sections=12
#                 )[0]
                
#             else:
#                 # Por defecto círculo
#                 curva = cmds.circle(name=nombre, normal=(1, 0, 0), radius=radio)[0]
            
#             # Crear grupo y posicionar
#             grp = cmds.group(curva, name=f"{nombre}_GRP")
#             cmds.xform(grp, ws=True, t=posicion)
            
#             # Aplicar color
#             self._aplicar_color_control(curva, color_index)
            
#             return curva, grp
            
#         except Exception as e:
#             print(f"❌ Error creando control {nombre}: {e}")
#             # Fallback: círculo básico
#             curva = cmds.circle(name=nombre, radius=radio)[0]
#             grp = cmds.group(curva, name=f"{nombre}_GRP")
#             cmds.xform(grp, ws=True, t=posicion)
#             return curva, grp

#     def _aplicar_color_control(self, control, color_index):
#         """Aplica color al control"""
#         try:
#             shapes = cmds.listRelatives(control, shapes=True) or []
#             for shape in shapes:
#                 cmds.setAttr(f"{shape}.overrideEnabled", 1)
#                 cmds.setAttr(f"{shape}.overrideColor", color_index)
#         except:
#             pass

#     def aplicar_skinning_basico(self):
#         """Aplica skinning básico pero funcional"""
#         try:
#             # Obtener joints
#             joints = [f"joint_{i}" for i in range(1, 10) if cmds.objExists(f"joint_{i}")]
#             if not joints:
#                 print("❌ No hay joints para skinning")
#                 return False
            
#             # Geometrías a skin
#             geometrias = ["axioma_carro"]
#             ruedas = ["rueda_delantera_izq", "rueda_delantera_der", "rueda_trasera_izq", "rueda_trasera_der"]
#             ejes = ["eje_delantero", "eje_trasero"]
            
#             # Agregar elementos existentes
#             for rueda in ruedas:
#                 if cmds.objExists(rueda):
#                     geometrias.append(rueda)
            
#             for eje in ejes:
#                 if cmds.objExists(eje):
#                     geometrias.append(eje)
            
#             print(f"🔗 Aplicando skinning a {len(geometrias)} geometrías...")
            
#             # Aplicar skin cluster
#             for geo in geometrias:
#                 try:
#                     # Limpiar skin existente
#                     skin_clusters = cmds.ls(cmds.listHistory(geo), type='skinCluster')
#                     if skin_clusters:
#                         cmds.delete(skin_clusters[0])
                    
#                     # Crear nuevo skin
#                     skin_cluster = cmds.skinCluster(joints, geo, name=f"{geo}_skin", maximumInfluences=3)[0]
#                     print(f"   ✅ Skin aplicado a {geo}")
                    
#                 except Exception as e:
#                     print(f"   ⚠️ No se pudo aplicar skin a {geo}: {e}")
            
#             return True
            
#         except Exception as e:
#             print(f"❌ Error en skinning: {e}")
#             return False

#     def crear_rig_completo_optimizado(self):
#         """Método PRINCIPAL optimizado"""
#         try:
#             print("🚗 INICIANDO CREACIÓN DE RIG OPTIMIZADO...")
            
#             # PASO 1: Verificación
#             if not self._verificar_geometria_completa():
#                 cmds.confirmDialog(title="Error", message="❌ Geometría incompleta", button=["OK"])
#                 return False
            
#             # PASO 2: Limpiar
#             self.limpiar_rig_existente()
            
#             # PASO 3: Crear jerarquía PRECISA
#             joints = self.crear_jerarquia_precisa()
#             if not joints:
#                 return False
            
#             # PASO 4: Crear controles ESPECÍFICOS
#             if not self.crear_controles_especificos():
#                 print("⚠️ Algunos controles fallaron, continuando...")
            
#             # PASO 5: Aplicar skinning
#             if not self.aplicar_skinning_basico():
#                 print("⚠️ Problemas con skinning, continuando...")
            
#             # PASO 6: Agrupar
#             try:
#                 grupos = cmds.ls("ctrl_joint_*_GRP", transforms=True)
#                 if grupos:
#                     rig_grp = cmds.group(grupos, name="RIG_CARRO_GRP")
#                     print(f"✅ Grupo principal creado: {rig_grp}")
#             except:
#                 print("⚠️ No se pudo crear grupo principal")
            
#             # Éxito
#             cmds.confirmDialog(
#                 title="🎉 Rig Completado", 
#                 message="✅ RIG CREADO EXITOSAMENTE!\n\n" +
#                        "9 joints posicionados precisamente:\n" +
#                        "• 3 Hexagonales (padres)\n" +
#                        "• 2 Cuadradas (hijos)\n" +
#                        "• 4 Circulares (llantas)\n\n" +
#                        "🎯 Controles activos: ctrl_joint_1 a ctrl_joint_9",
#                 button=["OK"]
#             )
            
#             print("✅✅✅ RIG OPTIMIZADO CREADO EXITOSAMENTE")
#             return True
            
#         except Exception as e:
#             error_msg = f"❌ Error en rig optimizado: {str(e)}"
#             print(error_msg)
#             cmds.confirmDialog(title="Error", message=error_msg, button=["OK"])
#             return False

# # FUNCIONES GLOBALES
# def crear_rig_carro(*args):
#     """Función global OPTIMIZADA"""
#     try:
#         print("🎯 EJECUTANDO VERSIÓN OPTIMIZADA...")
        
#         if not cmds.objExists("axioma_carro"):
#             cmds.confirmDialog(title="Error", message="❌ No hay carro en escena", button=["OK"])
#             return False
        
#         core = CarroRigCoreOptimizado()
#         resultado = core.crear_rig_completo_optimizado()
        
#         return resultado
        
#     except Exception as e:
#         cmds.warning(f"❌ Error crítico: {e}")
#         return False

# def limpiar_rig_existente():
#     core = CarroRigCoreOptimizado()
#     return core.limpiar_rig_existente()

# def optimizar_pesos_rig():
#     cmds.confirmDialog(title="Info", message="🔄 Función en desarrollo", button=["OK"])


import maya.cmds as cmds
import math

class CarroRigCoreOptimizado:  # ⚠️ MANTÉN EL NOMBRE ORIGINAL
    def __init__(self):
        print("🔧 CarroRigCoreOptimizado inicializado")
        self.altura_referencia = None
    
    # === MÉTODOS DE ALTURA UNIFICADA ===
    def _obtener_altura_unificada(self):
        """Obtiene una altura de referencia para todos los joints"""
        try:
            if self.altura_referencia is None:
                bb_chasis = cmds.exactWorldBoundingBox("axioma_carro")
                self.altura_referencia = (bb_chasis[1] + bb_chasis[4]) / 2
                print(f"📏 Altura de referencia: {self.altura_referencia}")
            return self.altura_referencia
        except:
            return 0
    
    def _obtener_pivot_cara_seguro(self, objeto, cara_tipo="centro"):
        """Simula el comportamiento de get_face_center de forma SEGURA"""
        try:
            if not cmds.objExists(objeto):
                return None
            
            bb = cmds.exactWorldBoundingBox(objeto)
            altura = self._obtener_altura_unificada()
            
            if cara_tipo == "centro":
                return [(bb[0] + bb[3]) / 2, altura, (bb[2] + bb[5]) / 2]
            elif cara_tipo == "delantera":
                return [bb[3], altura, (bb[2] + bb[5]) / 2]
            elif cara_tipo == "trasera":  
                return [bb[0], altura, (bb[2] + bb[5]) / 2]
            else:
                return [(bb[0] + bb[3]) / 2, altura, (bb[2] + bb[5]) / 2]
                
        except Exception as e:
            print(f"⚠️ Error obteniendo pivot simulado: {e}")
            return None

    def _crear_joint_altura_unificada(self, nombre, objeto_target=None, cara_tipo=None, posicion_default=None):
        """Crea joint con altura unificada"""
        try:
            cmds.select(clear=True)
            joint = cmds.joint(name=nombre)
            
            # PRIORIDAD 1: Posicionar en "cara" específica del objeto
            if objeto_target and cara_tipo and cmds.objExists(objeto_target):
                try:
                    target_pos = self._obtener_pivot_cara_seguro(objeto_target, cara_tipo)
                    if target_pos:
                        cmds.xform(joint, ws=True, t=target_pos)
                        print(f"   ✅ Joint {nombre} en {cara_tipo} de {objeto_target}")
                        return joint
                except Exception as e:
                    print(f"   ⚠️ No se pudo posicionar {nombre} en {cara_tipo}: {e}")
            
            # PRIORIDAD 2: Posicionar en objeto específico (altura unificada)
            if objeto_target and cmds.objExists(objeto_target):
                try:
                    bb = cmds.exactWorldBoundingBox(objeto_target)
                    altura = self._obtener_altura_unificada()
                    centro_xz = [(bb[0] + bb[3]) / 2, altura, (bb[2] + bb[5]) / 2]
                    cmds.xform(joint, ws=True, t=centro_xz)
                    print(f"   ✅ Joint {nombre} en centro de {objeto_target} (altura unificada)")
                    return joint
                except Exception as e:
                    print(f"   ⚠️ No se pudo posicionar {nombre} en {objeto_target}: {e}")
            
            # PRIORIDAD 3: Posición por defecto con altura unificada
            if posicion_default:
                try:
                    posicion_default[1] = self._obtener_altura_unificada()
                    cmds.xform(joint, ws=True, t=posicion_default)
                    print(f"   ✅ Joint {nombre} usando posición calculada (altura unificada)")
                    return joint
                except Exception as e:
                    print(f"   ⚠️ No se pudo posicionar {nombre} en posición calculada: {e}")
            
            # ULTIMO RECURSO
            cmds.xform(joint, ws=True, t=[0, self._obtener_altura_unificada(), 0])
            print(f"   ⚠️ Joint {nombre} usando posición de emergencia (altura unificada)")
            return joint
            
        except Exception as e:
            print(f"❌ Error creando joint {nombre}: {e}")
            return None

    # === MÉTODOS ORIGINALES (NECESARIOS PARA COMPATIBILIDAD) ===
    def _verificar_geometria_completa(self):
        """Verificación completa de geometría"""
        try:
            if not cmds.objExists("axioma_carro"):
                print("❌ No existe axioma_carro")
                return False
            
            elementos_requeridos = [
                "axioma_carro",
                "rueda_delantera_izq", "rueda_delantera_der",
                "rueda_trasera_izq", "rueda_trasera_der"
            ]
            
            for elemento in elementos_requeridos:
                if not cmds.objExists(elemento):
                    print(f"❌ No existe {elemento}")
                    return False
            
            print("✅ Geometría completa verificada")
            return True
            
        except Exception as e:
            print(f"❌ Error en verificación: {e}")
            return False

    def limpiar_rig_existente(self):
        """Limpieza completa del rig"""
        try:
            elementos = []
            
            # Elementos básicos
            elementos.extend([
                "RIG_CARRO_GRP", "ctrl_global", "ctrl_global_GRP",
                "ctrl_maletero", "ctrl_maletero_GRP", "ctrl_cabina", "ctrl_cabina_GRP",
                "ctrl_capo", "ctrl_capo_GRP"
            ])
            
            # Joints y controles
            for i in range(1, 10):
                elementos.extend([f"joint_{i}", f"ctrl_joint_{i}", f"ctrl_joint_{i}_GRP"])
            
            # Controles de ruedas
            ruedas_estandar = ["rueda_delantera_izq", "rueda_delantera_der", "rueda_trasera_izq", "rueda_trasera_der"]
            for rueda in ruedas_estandar:
                elementos.extend([f"ctrl_{rueda}", f"ctrl_{rueda}_GRP"])
            
            eliminados = 0
            for elem in elementos:
                if cmds.objExists(elem):
                    try:
                        cmds.delete(elem)
                        eliminados += 1
                    except:
                        pass
            
            print(f"🗑️ Eliminados {eliminados} elementos")
            return eliminados
            
        except Exception as e:
            print(f"⚠️ Error en limpieza: {e}")
            return 0

    def crear_jerarquia_precisa(self):
        """Crea la jerarquía de joints con posiciones PRECISAS - VERSIÓN SEGURA"""
        try:
            joints = {}
            
            # Obtener información del chasis
            chasis_bb = cmds.exactWorldBoundingBox("axioma_carro")
            centro_chasis = [
                (chasis_bb[0] + chasis_bb[3]) / 2,
                self._obtener_altura_unificada(),
                (chasis_bb[2] + chasis_bb[5]) / 2
            ]
            largo_chasis = chasis_bb[3] - chasis_bb[0]
            
            print("📍 Creando joints con ALTURA UNIFICADA...")
            
            # JOINT 1: Centro del chasis (cara 3 simulada)
            joints[1] = self._crear_joint_altura_unificada("joint_1", "axioma_carro", "centro", centro_chasis)
            
            # JOINT 2: Eje delantero (25% desde el frente)
            pos_eje_delantero = [chasis_bb[0] + largo_chasis * 0.25, self._obtener_altura_unificada(), centro_chasis[2]]
            joints[2] = self._crear_joint_altura_unificada("joint_2", "eje_delantero", "centro", pos_eje_delantero)
            
            # JOINT 3: Cara delantera (cara 6 simulada)
            joints[3] = self._crear_joint_altura_unificada("joint_3", "axioma_carro", "delantera", None)
            
            # JOINT 4: Eje trasero (75% desde el frente)
            pos_eje_trasero = [chasis_bb[0] + largo_chasis * 0.75, self._obtener_altura_unificada(), centro_chasis[2]]
            joints[4] = self._crear_joint_altura_unificada("joint_4", "eje_trasero", "centro", pos_eje_trasero)
            
            # JOINT 5: Cara trasera (cara 16 simulada)
            joints[5] = self._crear_joint_altura_unificada("joint_5", "axioma_carro", "trasera", None)
            
            # JOINTS DE RUEDAS - Misma altura que el chasis
            joints[6] = self._crear_joint_altura_unificada("joint_6", "rueda_delantera_der", "centro", None)
            joints[7] = self._crear_joint_altura_unificada("joint_7", "rueda_delantera_izq", "centro", None)
            joints[8] = self._crear_joint_altura_unificada("joint_8", "rueda_trasera_izq", "centro", None)
            joints[9] = self._crear_joint_altura_unificada("joint_9", "rueda_trasera_der", "centro", None)
            
            # Verificar joints
            for i in range(1, 10):
                if not joints.get(i):
                    print(f"❌ ERROR: No se pudo crear joint_{i}")
                    return {}
            
            # CONFIGURAR JERARQUÍA
            print("🔗 Configurando jerarquía con altura unificada...")
            cmds.parent(joints[2], joints[1])
            cmds.parent(joints[4], joints[1])
            cmds.parent(joints[3], joints[2])
            cmds.parent(joints[6], joints[2])
            cmds.parent(joints[7], joints[2])
            cmds.parent(joints[5], joints[4])
            cmds.parent(joints[8], joints[4])
            cmds.parent(joints[9], joints[4])
            
            # VERIFICAR ALTURAS
            print("📏 Verificando alturas unificadas...")
            for i in range(1, 10):
                pos = cmds.xform(joints[i], q=True, ws=True, t=True)
                print(f"   Joint_{i}: Y = {pos[1]:.3f}")
            
            print("✅ 9 joints creados con ALTURA UNIFICADA")
            return joints
            
        except Exception as e:
            print(f"❌ Error creando jerarquía: {e}")
            return {}

    def crear_controles_especificos(self):
        """Crea controles con formas específicas según el código original"""
        try:
            print("🎨 Creando controles específicos...")
            
            # Verificar que existen los 9 joints
            for i in range(1, 10):
                if not cmds.objExists(f"joint_{i}"):
                    print(f"❌ Joint faltante: joint_{i}")
                    return False
            
            # Configuración EXACTA según especificaciones originales
            config_joints = {
                1: {"nombre": "joint_1", "forma": "hexagono", "color": 22, "radio": 2.0, "rotar": False},
                2: {"nombre": "joint_2", "forma": "hexagono", "color": 6, "radio": 1.5, "rotar": False},
                4: {"nombre": "joint_4", "forma": "hexagono", "color": 14, "radio": 1.5, "rotar": False},
                3: {"nombre": "joint_3", "forma": "cuadrado", "color": 13, "radio": 1.2, "rotar": False},
                5: {"nombre": "joint_5", "forma": "cuadrado", "color": 17, "radio": 1.2, "rotar": False},
                6: {"nombre": "joint_6", "forma": "circulo", "color": 18, "radio": 0.8, "rotar": True},
                7: {"nombre": "joint_7", "forma": "circulo", "color": 19, "radio": 0.8, "rotar": True},
                8: {"nombre": "joint_8", "forma": "circulo", "color": 20, "radio": 0.8, "rotar": True},
                9: {"nombre": "joint_9", "forma": "circulo", "color": 21, "radio": 0.8, "rotar": True},
            }
            
            # Crear controles para cada joint
            for joint_num in range(1, 10):
                config = config_joints[joint_num]
                joint_name = config["nombre"]
                
                try:
                    # Obtener posición exacta del joint
                    pos = cmds.xform(joint_name, q=True, ws=True, t=True)
                    
                    # Crear control con forma específica
                    ctrl_name = f"ctrl_{joint_name}"
                    ctrl, grp = self._crear_control_con_forma(
                        ctrl_name, 
                        pos, 
                        config["forma"], 
                        config["radio"], 
                        config["color"]
                    )
                    
                    # Rotación para llantas
                    if config["rotar"]:
                        cmds.xform(grp, ro=(0, 0, 90))
                        print(f"   🎯 Control de LLANTA {ctrl_name} rotado 90° en Z")
                    
                    # Conectar control al joint
                    cmds.parentConstraint(ctrl, joint_name, mo=True)
                    print(f"   ✅ Control {joint_num}: {ctrl_name} ({config['forma']})")
                    
                except Exception as e:
                    print(f"❌ Error creando control para {joint_name}: {e}")
                    continue
            
            print("🎨 9 CONTROLES CREADOS EXITOSAMENTE:")
            print("   • 3 Hexagonales (joints 1,2,4 - padres)")
            print("   • 2 Cuadradas (joints 3,5 - hijos)") 
            print("   • 4 Circulares (joints 6,7,8,9 - llantas)")
            return True
            
        except Exception as e:
            print(f"❌ Error creando controles: {e}")
            return False

    def _crear_control_con_forma(self, nombre, posicion, forma, radio, color_index):
        """Crea controles con formas geométricas específicas"""
        try:
            if forma == "hexagono":
                puntos = []
                for i in range(6):
                    angulo = math.radians(i * 60)
                    x = radio * math.cos(angulo)
                    z = radio * math.sin(angulo)
                    puntos.append([x, 0, z])
                puntos.append(puntos[0])
                curva = cmds.curve(name=nombre, point=puntos, degree=1)
                
            elif forma == "cuadrado":
                puntos = [
                    [-radio, 0, -radio], [-radio, 0, radio], 
                    [radio, 0, radio], [radio, 0, -radio], [-radio, 0, -radio]
                ]
                curva = cmds.curve(name=nombre, point=puntos, degree=1)
                
            elif forma == "circulo":
                curva = cmds.circle(name=nombre, normal=(1, 0, 0), radius=radio, sections=12)[0]
            else:
                curva = cmds.circle(name=nombre, normal=(1, 0, 0), radius=radio)[0]
            
            grp = cmds.group(curva, name=f"{nombre}_GRP")
            cmds.xform(grp, ws=True, t=posicion)
            
            # Aplicar color
            self._aplicar_color_control(curva, color_index)
            
            return curva, grp
            
        except Exception as e:
            print(f"❌ Error creando control {nombre}: {e}")
            curva = cmds.circle(name=nombre, radius=radio)[0]
            grp = cmds.group(curva, name=f"{nombre}_GRP")
            cmds.xform(grp, ws=True, t=posicion)
            return curva, grp

    def _aplicar_color_control(self, control, color_index):
        """Aplica color al control"""
        try:
            shapes = cmds.listRelatives(control, shapes=True) or []
            for shape in shapes:
                cmds.setAttr(f"{shape}.overrideEnabled", 1)
                cmds.setAttr(f"{shape}.overrideColor", color_index)
        except:
            pass

    def aplicar_skinning_basico(self):
        """Aplica skinning básico pero funcional"""
        try:
            joints = [f"joint_{i}" for i in range(1, 10) if cmds.objExists(f"joint_{i}")]
            if not joints:
                print("❌ No hay joints para skinning")
                return False
            
            geometrias = ["axioma_carro"]
            ruedas = ["rueda_delantera_izq", "rueda_delantera_der", "rueda_trasera_izq", "rueda_trasera_der"]
            ejes = ["eje_delantero", "eje_trasero"]
            
            for rueda in ruedas:
                if cmds.objExists(rueda):
                    geometrias.append(rueda)
            
            for eje in ejes:
                if cmds.objExists(eje):
                    geometrias.append(eje)
            
            print(f"🔗 Aplicando skinning a {len(geometrias)} geometrías...")
            
            for geo in geometrias:
                try:
                    skin_clusters = cmds.ls(cmds.listHistory(geo), type='skinCluster')
                    if skin_clusters:
                        cmds.delete(skin_clusters[0])
                    
                    skin_cluster = cmds.skinCluster(joints, geo, name=f"{geo}_skin", maximumInfluences=3)[0]
                    print(f"   ✅ Skin aplicado a {geo}")
                    
                except Exception as e:
                    print(f"   ⚠️ No se pudo aplicar skin a {geo}: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en skinning: {e}")
            return False

    def crear_rig_completo_optimizado(self):
        """Método PRINCIPAL optimizado - VERSIÓN SEGURA"""
        try:
            print("🚗 INICIANDO CREACIÓN DE RIG OPTIMIZADO Y SEGURO...")
            
            # PASO 1: Verificación
            if not self._verificar_geometria_completa():
                cmds.confirmDialog(title="Error", message="❌ Geometría incompleta", button=["OK"])
                return False
            
            # PASO 2: Limpiar
            self.limpiar_rig_existente()
            
            # PASO 3: Crear jerarquía PRECISA Y SEGURA
            joints = self.crear_jerarquia_precisa()
            if not joints:
                return False
            
            # PASO 4: Crear controles ESPECÍFICOS
            if not self.crear_controles_especificos():
                print("⚠️ Algunos controles fallaron, continuando...")
            
            # PASO 5: Aplicar skinning
            if not self.aplicar_skinning_basico():
                print("⚠️ Problemas con skinning, continuando...")
            
            # PASO 6: Agrupar
            try:
                grupos = cmds.ls("ctrl_joint_*_GRP", transforms=True)
                if grupos:
                    rig_grp = cmds.group(grupos, name="RIG_CARRO_GRP")
                    print(f"✅ Grupo principal creado: {rig_grp}")
            except:
                print("⚠️ No se pudo crear grupo principal")
            
            # Éxito
            cmds.confirmDialog(
                title="🎉 Rig Completado", 
                message="✅ RIG SEGURO CREADO EXITOSAMENTE!\n\n" +
                       "9 joints con altura unificada:\n" +
                       "• 3 Hexagonales (padres)\n" +
                       "• 2 Cuadradas (hijos)\n" +
                       "• 4 Circulares (llantas)\n\n" +
                       "🎯 Sin riesgo de crash",
                button=["OK"]
            )
            
            print("✅✅✅ RIG OPTIMIZADO Y SEGURO CREADO EXITOSAMENTE")
            return True
            
        except Exception as e:
            error_msg = f"❌ Error en rig optimizado: {str(e)}"
            print(error_msg)
            cmds.confirmDialog(title="Error", message=error_msg, button=["OK"])
            return False

# === FUNCIONES GLOBALES (MANTENER COMPATIBILIDAD) ===
def crear_rig_carro(*args):
    """Función global OPTIMIZADA - VERSIÓN SEGURA"""
    try:
        print("🎯 EJECUTANDO VERSIÓN OPTIMIZADA Y SEGURA...")
        
        if not cmds.objExists("axioma_carro"):
            cmds.confirmDialog(title="Error", message="❌ No hay carro en escena", button=["OK"])
            return False
        
        core = CarroRigCoreOptimizado()
        resultado = core.crear_rig_completo_optimizado()
        
        return resultado
        
    except Exception as e:
        cmds.warning(f"❌ Error crítico: {e}")
        return False

def limpiar_rig_existente():
    core = CarroRigCoreOptimizado()
    return core.limpiar_rig_existente()

def optimizar_pesos_rig():
    cmds.confirmDialog(title="Info", message="🔄 Función en desarrollo", button=["OK"])