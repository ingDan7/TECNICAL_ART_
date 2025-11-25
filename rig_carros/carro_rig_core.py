import maya.cmds as cmds
import math  # ✅ Importar math para funciones trigonométricas
from carro_rig_utils import (
    get_face_center, align_joint_to_position, align_to_object_center, 
    create_control, buscar_objetos_escena_filtrado, NOMBRES_ESTANDAR
)

class CarroRigCore:
    def __init__(self):
        print("🔧 CarroRigCore inicializado")
    
    def crear_curvas_control_joints(self):
        """Crea exactamente 9 curvas de control - una para cada joint"""
        try:
            print("🎨 Creando 9 curvas de control para todos los joints...")
            
            # Configuración EXACTA según especificaciones
            config_joints = {
                # JOINTS PADRES - Formas HEXAGONALES
                1: {"nombre": "joint_1", "forma": "hexagono", "color": 22, "radio": 2.0, "rotar": False},  # Centro (padre)
                2: {"nombre": "joint_2", "forma": "hexagono", "color": 6, "radio": 1.5, "rotar": False},   # Eje delantero (padre)
                4: {"nombre": "joint_4", "forma": "hexagono", "color": 14, "radio": 1.5, "rotar": False},  # Eje trasero (padre)
                
                # JOINTS HIJOS (no llantas) - Formas CUADRADAS
                3: {"nombre": "joint_3", "forma": "cuadrado", "color": 13, "radio": 1.2, "rotar": False},  # Cara delantera
                5: {"nombre": "joint_5", "forma": "cuadrado", "color": 17, "radio": 1.2, "rotar": False},  # Cara trasera
                
                # JOINTS LLANTAS - Formas CIRCULARES (rotadas 90° en Z)
                6: {"nombre": "joint_6", "forma": "circulo", "color": 18, "radio": 0.8, "rotar": True},   # Rueda delantera der
                7: {"nombre": "joint_7", "forma": "circulo", "color": 19, "radio": 0.8, "rotar": True},   # Rueda delantera izq
                8: {"nombre": "joint_8", "forma": "circulo", "color": 20, "radio": 0.8, "rotar": True},   # Rueda trasera izq
                9: {"nombre": "joint_9", "forma": "circulo", "color": 21, "radio": 0.8, "rotar": True},   # Rueda trasera der
            }
            
            # Verificar que existen los 9 joints
            joints_existentes = []
            for joint_num in range(1, 10):
                joint_name = f"joint_{joint_num}"
                if cmds.objExists(joint_name):
                    joints_existentes.append(joint_num)
                else:
                    print(f"⚠️ Joint faltante: {joint_name}")
            
            if len(joints_existentes) != 9:
                print(f"❌ Faltan joints. Encontrados: {joints_existentes}")
                return False
            
            # Crear controles para CADA UNO de los 9 joints
            for joint_num in range(1, 10):
                config = config_joints[joint_num]
                joint_name = config["nombre"]
                
                # Obtener posición exacta del joint
                pos = cmds.xform(joint_name, q=True, ws=True, t=True)
                
                # Crear control con forma específica
                ctrl_name = f"ctrl_{joint_name}"
                ctrl, grp = self._crear_control_con_forma_exacta(
                    ctrl_name, 
                    pos, 
                    config["forma"], 
                    config["radio"], 
                    config["color"]
                )
                
                # ROTACIÓN CRÍTICA: Solo para llantas (joints 6-9)
                if config["rotar"]:
                    cmds.xform(grp, ro=(0, 0, 90))  # 90° en Z para llantas
                    print(f"   🎯 Control de LLANTA {ctrl_name} rotado 90° en Z")
                
                # CONEXIÓN DIRECTA al joint correspondiente
                cmds.parentConstraint(ctrl, joint_name, mo=True)
                print(f"   ✅ Control {joint_num}: {ctrl_name} ({config['forma']}, color: {config['color']})")
            
            print("🎨 9 CURVAS CREADAS EXITOSAMENTE:")
            print("   • 3 Hexagonales (joints 1,2,4 - padres)")
            print("   • 2 Cuadradas (joints 3,5 - hijos no llantas)") 
            print("   • 4 Circulares (joints 6,7,8,9 - llantas rotadas 90°Z)")
            return True
            
        except Exception as e:
            print(f"❌ Error creando curvas de control: {e}")
            return False

    def _crear_control_con_forma_exacta(self, nombre, posicion, forma, radio, color_index):
        """Crea controles con formas geométricas exactas según especificación"""
        
        if forma == "hexagono":
            # ✅ CORREGIDO: Usar math en lugar de cmds para funciones trigonométricas
            puntos = []
            for i in range(6):
                angulo = math.radians(i * 60)  # Convertir a radianes
                x = radio * math.cos(angulo)
                z = radio * math.sin(angulo)
                puntos.append([x, 0, z])
            # Cerrar el hexágono
            puntos.append(puntos[0])
            curva = cmds.curve(name=nombre, point=puntos, degree=1)
            
        elif forma == "cuadrado":
            # CUADRADO para joints hijos no llantas
            puntos = [
                [-radio, 0, -radio], [-radio, 0, radio], 
                [radio, 0, radio], [radio, 0, -radio], [-radio, 0, -radio]
            ]
            curva = cmds.curve(name=nombre, point=puntos, degree=1)
            
        elif forma == "circulo":
            # CÍRCULO para llantas - orientado correctamente para rotación Z
            curva = cmds.circle(
                name=nombre, 
                normal=(1, 0, 0),  # Orientación en X para rotación Z correcta
                radius=radio,
                sections=12
            )[0]
            
        else:
            # Por defecto círculo
            curva = cmds.circle(name=nombre, normal=(1, 0, 0), radius=radio)[0]
        
        # Crear grupo para el control
        grp = cmds.group(curva, name=f"{nombre}_GRP")
        
        # Posicionar exactamente en la posición del joint
        cmds.xform(grp, ws=True, t=posicion)
        
        # Aplicar color específico
        self._aplicar_color_control(curva, color_index)
        
        return curva, grp

    def _aplicar_color_control(self, control, color_index):
        """Aplica color al control"""
        try:
            shapes = cmds.listRelatives(control, shapes=True)
            if shapes:
                cmds.setAttr(f"{shapes[0]}.overrideEnabled", 1)
                cmds.setAttr(f"{shapes[0]}.overrideColor", color_index)
        except:
            pass

    def _aplicar_color_control(self, control, color_index):
        """Aplica color al control"""
        try:
            shapes = cmds.listRelatives(control, shapes=True)
            if shapes:
                cmds.setAttr(f"{shapes[0]}.overrideEnabled", 1)
                cmds.setAttr(f"{shapes[0]}.overrideColor", color_index)
        except:
            pass

    def limpiar_rig_existente(self):
        """Limpia todos los elementos del rig anterior incluyendo las nuevas curvas"""
        elementos_rig = [
            "RIG_CARRO_GRP", "ctrl_global", "ctrl_global_GRP",
            "ctrl_maletero", "ctrl_maletero_GRP", "ctrl_cabina", "ctrl_cabina_GRP",
            "ctrl_capo", "ctrl_capo_GRP"
        ]
        
        # Agregar joints (1-9) y sus NUEVAS curvas de control
        for i in range(1, 10):
            elementos_rig.append(f"joint_{i}")
            elementos_rig.append(f"ctrl_joint_{i}")      # Nueva curva
            elementos_rig.append(f"ctrl_joint_{i}_GRP")  # Grupo de la nueva curva
        
        # Controles de ruedas existentes
        for rueda in NOMBRES_ESTANDAR["ruedas"]:
            elementos_rig.extend([f"ctrl_{rueda}", f"ctrl_{rueda}_GRP"])
        
        elementos_eliminados = []
        for elem in elementos_rig:
            if cmds.objExists(elem):
                try:
                    cmds.delete(elem)
                    elementos_eliminados.append(elem)
                except:
                    pass
        
        print(f"🗑️ Elementos eliminados: {len(elementos_eliminados)}")
        return len(elementos_eliminados)

    def aplicar_skinning_inteligente(self, chasis, ruedas, ejes):
        """Aplica skinning inteligente con pesos optimizados"""
        try:
            print("🔗 Aplicando skinning inteligente...")
            
            # Obtener todos los joints del rig
            joints_rig = [f"joint_{i}" for i in range(1, 10) if cmds.objExists(f"joint_{i}")]
            
            if not joints_rig:
                print("⚠️ No se encontraron joints para skinning")
                return False
            
            # Lista de todas las geometrías a skin
            geometrias = []
            if chasis and cmds.objExists(chasis):
                geometrias.append(chasis)
            if ejes:
                for eje in ejes:
                    if cmds.objExists(eje):
                        geometrias.append(eje)
            if ruedas:
                for rueda in ruedas:
                    if cmds.objExists(rueda):
                        geometrias.append(rueda)
            
            if not geometrias:
                print("⚠️ No se encontraron geometrías para skinning")
                return False
            
            # Aplicar skin cluster a cada geometría con pesos optimizados
            for geo in geometrias:
                try:
                    # Verificar si ya tiene skin cluster
                    skin_clusters = cmds.ls(cmds.listHistory(geo), type='skinCluster')
                    if skin_clusters:
                        print(f"🔄 Reconfigurando skin existente en: {geo}")
                        skin_cluster = skin_clusters[0]
                    else:
                        # Crear skin cluster
                        skin_cluster = cmds.skinCluster(joints_rig, geo, name=f"{geo}_skinCluster", maximumInfluences=3)[0]
                        print(f"✅ Skin creado para: {geo}")
                    
                    # Aplicar pesos optimizados según el tipo de geometría
                    self._aplicar_pesos_optimizados(geo, skin_cluster, joints_rig)
                    
                except Exception as e:
                    print(f"⚠️ No se pudo aplicar skin a {geo}: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en skinning inteligente: {e}")
            return False

    def _aplicar_pesos_optimizados(self, geometria, skin_cluster, joints):
        """Aplica pesos optimizados según el tipo de geometría"""
        try:
            print(f"🎯 Optimizando pesos para: {geometria}")
            
            # Determinar el tipo de geometría
            geo_name_lower = geometria.lower()
            
            if "chasis" in geo_name_lower or "axioma" in geo_name_lower:
                self._pesos_chasis(geometria, skin_cluster, joints)
            elif "eje" in geo_name_lower:
                self._pesos_ejes(geometria, skin_cluster, joints)
            elif "rueda" in geo_name_lower:
                self._pesos_ruedas(geometria, skin_cluster, joints)
            else:
                # Pesos por defecto para geometrías desconocidas
                self._pesos_default(geometria, skin_cluster, joints)
                
        except Exception as e:
            print(f"⚠️ Error optimizando pesos para {geometria}: {e}")

    def _pesos_chasis(self, chasis, skin_cluster, joints):
        """Pesos optimizados para el chasis"""
        print(f"   🏗️ Aplicando pesos de chasis...")
        
        # Resetear pesos primero
        cmds.skinPercent(skin_cluster, chasis, normalize=True, pruneWeights=0.01)
        
        # Obtener bounding box del chasis
        bb = cmds.exactWorldBoundingBox(chasis)
        centro_x = (bb[0] + bb[3]) / 2
        centro_z = (bb[2] + bb[5]) / 2
        longitud_x = bb[3] - bb[0]
        longitud_z = bb[5] - bb[2]
        
        # Joints principales
        joint_1 = "joint_1"  # Centro
        joint_2 = "joint_2"  # Eje delantero
        joint_3 = "joint_3"  # Cara delantera
        joint_4 = "joint_4"  # Eje trasero
        joint_5 = "joint_5"  # Cara trasera
        
        # Aplicar pesos basados en la posición
        vtx_count = cmds.polyEvaluate(chasis, vertex=True)
        
        for i in range(vtx_count):
            vtx = f"{chasis}.vtx[{i}]"
            pos = cmds.pointPosition(vtx, world=True)
            
            # Calcular influencias basadas en distancia
            dist_centro = abs(pos[0] - centro_x) / (longitud_x / 2)
            dist_frente = abs(pos[2] - centro_z) / (longitud_z / 2)
            
            # 🔧 PESOS EDITABLES - Chasis
            peso_centro = max(0, 1 - dist_centro * 1.5)
            peso_delantero = max(0, 0.7 - dist_frente) if pos[2] > centro_z else 0
            peso_trasero = max(0, 0.7 - dist_frente) if pos[2] < centro_z else 0
            
            # Asignar pesos
            pesos = {}
            if peso_centro > 0.1:
                pesos[joint_1] = peso_centro * 0.6  # 🔧 60% al centro
            if peso_delantero > 0.1:
                pesos[joint_2] = peso_delantero * 0.3  # 🔧 30% al eje delantero
                pesos[joint_3] = peso_delantero * 0.7  # 🔧 70% a cara delantera
            if peso_trasero > 0.1:
                pesos[joint_4] = peso_trasero * 0.3    # 🔧 30% al eje trasero
                pesos[joint_5] = peso_trasero * 0.7    # 🔧 70% a cara trasera
            
            # Normalizar y aplicar
            if pesos:
                total = sum(pesos.values())
                if total > 0:
                    for joint, peso in pesos.items():
                        pesos[joint] = peso / total
                    cmds.skinPercent(skin_cluster, vtx, transformValue=pesos.items())

    def _pesos_ejes(self, eje, skin_cluster, joints):
        """Pesos optimizados para ejes"""
        print(f"   🎯 Aplicando pesos de eje...")
        
        # Resetear pesos
        cmds.skinPercent(skin_cluster, eje, normalize=True, pruneWeights=0.01)
        
        eje_name_lower = eje.lower()
        
        if "delantero" in eje_name_lower:
            joint_principal = "joint_2"
            joint_secundario = "joint_1"
        else:  # trasero
            joint_principal = "joint_4"
            joint_secundario = "joint_1"
        
        # 🔧 PESOS EDITABLES - Ejes: 80% al joint principal, 20% al centro
        cmds.skinPercent(skin_cluster, eje, transformValue=[
            (joint_principal, 0.8),    # 🔧 Cambiar 0.8 para ajustar influencia del eje
            (joint_secundario, 0.2)    # 🔧 Cambiar 0.2 para ajustar influencia del centro
        ])

    def _pesos_ruedas(self, rueda, skin_cluster, joints):
        """Pesos optimizados para ruedas"""
        print(f"   🎯 Aplicando pesos de rueda...")
        
        # Resetear pesos
        cmds.skinPercent(skin_cluster, rueda, normalize=True, pruneWeights=0.01)
        
        rueda_name_lower = rueda.lower()
        
        # Determinar joint principal basado en el nombre de la rueda
        if "delantera" in rueda_name_lower:
            if "der" in rueda_name_lower:
                joint_principal = "joint_6"
            else:  # izq
                joint_principal = "joint_7"
            joint_eje = "joint_2"
        else:  # trasera
            if "izq" in rueda_name_lower:
                joint_principal = "joint_8"
            else:  # der
                joint_principal = "joint_9"
            joint_eje = "joint_4"
        
        # 🔧 PESOS EDITABLES - Ruedas: 90% al joint de rueda, 10% al eje
        cmds.skinPercent(skin_cluster, rueda, transformValue=[
            (joint_principal, 0.9),    # 🔧 Cambiar 0.9 para ajustar influencia de la rueda
            (joint_eje, 0.1)           # 🔧 Cambiar 0.1 para ajustar influencia del eje
        ])

    def _pesos_default(self, geometria, skin_cluster, joints):
        """Pesos por defecto para geometrías desconocidas"""
        print(f"   ⚙️ Aplicando pesos por defecto...")
        cmds.skinPercent(skin_cluster, geometria, normalize=True)

    def ajustar_rig_existente(self):
        """Ajusta el rig existente a la geometría actual del carro."""
        if not cmds.objExists("RIG_CARRO_GRP"):
            cmds.confirmDialog(title="Error", message="❌ No hay rig existente para ajustar.", button=["OK"])
            return False
        
        chasis, ruedas, ejes = buscar_objetos_escena_filtrado()
        
        if not chasis:
            cmds.confirmDialog(title="Error", message="❌ No se encontró chasis en la escena.", button=["OK"])
            return False
        
        try:
            print("🔄 Iniciando ajuste del rig existente...")
            
            # Actualizar joints según jerarquía específica
            if cmds.objExists("joint_1"):
                align_joint_to_position("joint_1", get_face_center(chasis, 3))
            
            # Joint 2 (eje delantero)
            if cmds.objExists("joint_2") and cmds.objExists("eje_delantero"):
                align_joint_to_position("joint_2", align_to_object_center("eje_delantero"))
            
            # Joint 3 (cara delantera - axioma_carro.f[6])
            if cmds.objExists("joint_3"):
                align_joint_to_position("joint_3", get_face_center(chasis, 6))
            
            # Joint 4 (eje trasero)
            if cmds.objExists("joint_4") and cmds.objExists("eje_trasero"):
                align_joint_to_position("joint_4", align_to_object_center("eje_trasero"))
            
            # Joint 5 (cara trasera - axioma_carro.f[16])
            if cmds.objExists("joint_5"):
                align_joint_to_position("joint_5", get_face_center(chasis, 16))
            
            # Ruedas
            ruedas_info = [
                ("joint_6", "rueda_delantera_der"),
                ("joint_7", "rueda_delantera_izq"), 
                ("joint_8", "rueda_trasera_izq"),
                ("joint_9", "rueda_trasera_der")
            ]
            
            for joint_name, rueda_name in ruedas_info:
                if cmds.objExists(joint_name) and cmds.objExists(rueda_name):
                    align_joint_to_position(joint_name, align_to_object_center(rueda_name))
            
            # Actualizar controles de ruedas
            for joint_name, rueda_name in ruedas_info:
                ctrl_name = f"ctrl_{rueda_name}"
                if cmds.objExists(ctrl_name) and cmds.objExists(rueda_name):
                    pos = align_to_object_center(rueda_name)
                    cmds.xform(f"{ctrl_name}_GRP", ws=True, t=pos)
            
            # Actualizar control global
            if cmds.objExists("ctrl_global"):
                pos_centro = get_face_center(chasis, 3)
                cmds.xform("ctrl_global_GRP", ws=True, t=pos_centro)
            
            # Actualizar las nuevas curvas de control de joints
            for i in range(1, 10):
                joint_name = f"joint_{i}"
                ctrl_name = f"ctrl_{joint_name}"
                grp_name = f"ctrl_{joint_name}_GRP"
                
                if cmds.objExists(joint_name) and cmds.objExists(grp_name):
                    pos = cmds.xform(joint_name, q=True, ws=True, t=True)
                    cmds.xform(grp_name, ws=True, t=pos)
            
            # Re-aplicar skinning inteligente
            self.aplicar_skinning_inteligente(chasis, ruedas, ejes)
            
            cmds.confirmDialog(
                title="Ajuste Completado", 
                message="✅ Rig ajustado correctamente.\n\nSe aplicaron pesos optimizados.", 
                button=["OK"]
            )
            return True
            
        except Exception as e:
            cmds.confirmDialog(title="Error", message=f"❌ Error al ajustar rig: {str(e)}", button=["OK"])
            return False

    def crear_rig_completo(self, chasis=None, ruedas=None, ejes=None):
        """Crea o regenera el rig completo del carro con las 9 curvas especificadas"""
        # Limpiar rig existente primero
        elementos_eliminados = self.limpiar_rig_existente()
        
        # Buscar objetos automáticamente si no se proporcionan
        if chasis is None or ruedas is None:
            chasis_encontrado, ruedas_encontradas, ejes_encontrados = buscar_objetos_escena_filtrado()
            chasis = chasis or chasis_encontrado
            ruedas = ruedas or ruedas_encontradas
            ejes = ejes or ejes_encontrados
        
        print(f"🔍 Chasis encontrado: {chasis}")
        print(f"🔍 Ruedas encontradas: {ruedas}")
        print(f"🔍 Ejes encontrados: {ejes}")
        
        if not chasis:
            cmds.confirmDialog(
                title="Error",
                message="❌ No se encontró chasis en la escena.",
                button=["OK"]
            )
            return False

        # Asegurar nombres estándar
        chasis_estandar = NOMBRES_ESTANDAR["chasis"]
        if chasis != chasis_estandar:
            try:
                cmds.rename(chasis, chasis_estandar)
                chasis = chasis_estandar
                print(f"✅ Renombrado chasis a: {chasis}")
            except:
                print(f"⚠️ No se pudo renombrar {chasis} a {chasis_estandar}")

        # CREAR SISTEMA DE RIG
        try:
            print("🔄 Creando sistema de rig...")
            
            # -----------------------------
            # CREAR JERARQUÍA EXACTA DE JOINTS (1-9)
            # -----------------------------
            
            print("📍 Creando jerarquía exacta de 9 joints...")
            
            # CREAR TODOS LOS JOINTS INDEPENDIENTES PRIMERO
            joints = {}
            
            # Joint 1: Padre principal (cara 3)
            cmds.select(clear=True)
            joints[1] = cmds.joint(name="joint_1")
            align_joint_to_position(joints[1], get_face_center(chasis, 3))
            
            # Joint 2: Eje delantero (será padre)
            cmds.select(clear=True)
            if cmds.objExists("eje_delantero"):
                joints[2] = cmds.joint(name="joint_2")
                align_joint_to_position(joints[2], align_to_object_center("eje_delantero"))
            else:
                joints[2] = cmds.joint(name="joint_2")
                pos_j1 = cmds.xform(joints[1], q=True, ws=True, t=True)
                align_joint_to_position(joints[2], [pos_j1[0] + 3, pos_j1[1], pos_j1[2]])
            
            # Joint 3: Cara delantera (hijo de joint_2 - NO será padre)
            cmds.select(clear=True)
            joints[3] = cmds.joint(name="joint_3")
            align_joint_to_position(joints[3], get_face_center(chasis, 6))
            
            # Joint 4: Eje trasero (será padre)
            cmds.select(clear=True)
            if cmds.objExists("eje_trasero"):
                joints[4] = cmds.joint(name="joint_4")
                align_joint_to_position(joints[4], align_to_object_center("eje_trasero"))
            else:
                joints[4] = cmds.joint(name="joint_4")
                pos_j1 = cmds.xform(joints[1], q=True, ws=True, t=True)
                align_joint_to_position(joints[4], [pos_j1[0] - 3, pos_j1[1], pos_j1[2]])
            
            # Joint 5: Cara trasera (hijo de joint_4 - NO será padre)
            cmds.select(clear=True)
            joints[5] = cmds.joint(name="joint_5")
            align_joint_to_position(joints[5], get_face_center(chasis, 16))
            
            # Ruedas (NO serán padres)
            # Joint 6: Rueda delantera derecha (hijo de joint_2)
            cmds.select(clear=True)
            if cmds.objExists("rueda_delantera_der"):
                joints[6] = cmds.joint(name="joint_6")
                align_joint_to_position(joints[6], align_to_object_center("rueda_delantera_der"))
            else:
                joints[6] = cmds.joint(name="joint_6")
                pos_j2 = cmds.xform(joints[2], q=True, ws=True, t=True)
                align_joint_to_position(joints[6], [pos_j2[0] + 1, pos_j2[1], pos_j2[2] - 2])
            
            # Joint 7: Rueda delantera izquierda (hijo de joint_2)
            cmds.select(clear=True)
            if cmds.objExists("rueda_delantera_izq"):
                joints[7] = cmds.joint(name="joint_7")
                align_joint_to_position(joints[7], align_to_object_center("rueda_delantera_izq"))
            else:
                joints[7] = cmds.joint(name="joint_7")
                pos_j2 = cmds.xform(joints[2], q=True, ws=True, t=True)
                align_joint_to_position(joints[7], [pos_j2[0] + 1, pos_j2[1], pos_j2[2] + 2])
            
            # Joint 8: Rueda trasera izquierda (hijo de joint_4)
            cmds.select(clear=True)
            if cmds.objExists("rueda_trasera_izq"):
                joints[8] = cmds.joint(name="joint_8")
                align_joint_to_position(joints[8], align_to_object_center("rueda_trasera_izq"))
            else:
                joints[8] = cmds.joint(name="joint_8")
                pos_j4 = cmds.xform(joints[4], q=True, ws=True, t=True)
                align_joint_to_position(joints[8], [pos_j4[0] - 1, pos_j4[1], pos_j4[2] + 2])
            
            # Joint 9: Rueda trasera derecha (hijo de joint_4)
            cmds.select(clear=True)
            if cmds.objExists("rueda_trasera_der"):
                joints[9] = cmds.joint(name="joint_9")
                align_joint_to_position(joints[9], align_to_object_center("rueda_trasera_der"))
            else:
                joints[9] = cmds.joint(name="joint_9")
                pos_j4 = cmds.xform(joints[4], q=True, ws=True, t=True)
                align_joint_to_position(joints[9], [pos_j4[0] - 1, pos_j4[1], pos_j4[2] - 2])
            
            # -----------------------------
            # CONFIGURAR JERARQUÍA EXACTA
            # -----------------------------
            
            print("📍 Configurando jerarquía exacta...")
            
            # SOLO 3 PADRES: joint1, joint2, joint4
            cmds.parent(joints[2], joints[1])
            cmds.parent(joints[4], joints[1])
            
            # Joint 3, 6, 7 son hijos de Joint 2
            cmds.parent(joints[3], joints[2])
            cmds.parent(joints[6], joints[2])
            cmds.parent(joints[7], joints[2])
            
            # Joint 5, 8, 9 son hijos de Joint 4
            cmds.parent(joints[5], joints[4])
            cmds.parent(joints[8], joints[4])
            cmds.parent(joints[9], joints[4])
            
            cmds.select(clear=True)

            # -----------------------------
            # CREAR LAS 9 CURVAS DE CONTROL ESPECIFICADAS
            # -----------------------------
            
            print("🎨 CREANDO LAS 9 CURVAS DE CONTROL...")
            if not self.crear_curvas_control_joints():
                print("❌ Error al crear las curvas de control")
                return False

            # -----------------------------
            # CREAR CONTROLES PRINCIPALES (existente)
            # -----------------------------
            
            # Control global (en el centro/padre)
            pos_centro = get_face_center(chasis, 3)
            global_ctrl, global_grp = create_control("ctrl_global", pos_centro, radius=5, color_index=22)
            
            # Controles para ruedas
            ruedas_nombres = ["rueda_delantera_der", "rueda_delantera_izq", "rueda_trasera_izq", "rueda_trasera_der"]
            for nombre_rueda in ruedas_nombres:
                if cmds.objExists(nombre_rueda):
                    pos = align_to_object_center(nombre_rueda)
                    ctrl, grp = create_control(f"ctrl_{nombre_rueda}", pos, radius=0.8, color_index=13)
                else:
                    ctrl, grp = create_control(f"ctrl_{nombre_rueda}", [0, 0, 0], radius=0.8, color_index=13)
            
            # -----------------------------
            # CONFIGURAR JERARQUÍA Y CONSTRAINTS
            # -----------------------------
            

            
            for nombre_rueda in ruedas_nombres:
                grp_name = f"ctrl_{nombre_rueda}_GRP"
                if cmds.objExists(grp_name):
                    cmds.parent(grp_name, global_ctrl)
            
            # Parentear las NUEVAS curvas de joints al control global
            for i in range(1, 10):
                grp_name = f"ctrl_joint_{i}_GRP"
                if cmds.objExists(grp_name):
                    cmds.parent(grp_name, global_ctrl)
            
            # Crear grupo principal del rig
            rig_grp = cmds.group(global_grp, name=NOMBRES_ESTANDAR["grupo_rig"])
            
            # Constraints para ruedas
            ruedas_joints = [
                ("rueda_delantera_der", "joint_6"),
                ("rueda_delantera_izq", "joint_7"),
                ("rueda_trasera_izq", "joint_8"),
                ("rueda_trasera_der", "joint_9")
            ]
            
            for rueda_name, joint_name in ruedas_joints:
                ctrl_name = f"ctrl_{rueda_name}"
                if cmds.objExists(ctrl_name) and cmds.objExists(joint_name):
                    cmds.parentConstraint(ctrl_name, joint_name, mo=True)

            # -----------------------------
            # APLICAR SKINNING INTELIGENTE
            # -----------------------------
            
            self.aplicar_skinning_inteligente(chasis, ruedas, ejes)
            
            cmds.confirmDialog(
                title="Rig del Carro Completado",
                message="✅ Rig creado CORRECTAMENTE con 9 curvas!\n\n" +
                       "• 3 Hexagonales (joints 1,2,4 - padres)\n" +
                       "• 2 Cuadradas (joints 3,5 - hijos)\n" + 
                       "• 4 Circulares (joints 6,7,8,9 - llantas rotadas 90°Z)",
                button=["OK"]
            )
            
            print("✅ Rig creado exitosamente con 9 curvas de control específicas")
            return True
            
        except Exception as e:
            error_msg = f"❌ Error al crear rig: {str(e)}"
            print(error_msg)
            cmds.confirmDialog(title="Error", message=error_msg, button=["OK"])
            return False

    # Funciones adicionales para compatibilidad
    def crear_rig_carro_con_ejes(self):
        """Crea rig para modelos con ejes separados"""
        print("🔄 Iniciando creación de rig con ejes...")
        return self.crear_rig_completo()

    def hacer_skin_completo(self, chasis, ruedas, ejes, columna, joints_ejes):
        """Conecta todos los componentes al rig"""
        print("🔗 Aplicando skinning a todos los componentes...")
        return self.aplicar_skinning_inteligente(chasis, ruedas, ejes)

# Alias para compatibilidad
crear_rig_modular = CarroRigCore.crear_rig_carro_con_ejes

# Funciones globales para compatibilidad con código existente
def limpiar_rig_existente():
    """Función global para compatibilidad"""
    core = CarroRigCore()
    return core.limpiar_rig_existente()

def ajustar_rig_existente():
    """Función global para compatibilidad"""
    core = CarroRigCore()
    return core.ajustar_rig_existente()

def crear_rig_carro(*args):
    """Función global para compatibilidad"""
    core = CarroRigCore()
    return core.crear_rig_completo()

def crear_rig_carro_con_ejes():
    """Función global para compatibilidad"""
    core = CarroRigCore()
    return core.crear_rig_carro_con_ejes()

def crear_curvas_control_todos_joints():
    """Función global para crear las 9 curvas de control específicas"""
    core = CarroRigCore()
    return core.crear_curvas_control_joints()

# Funciones para optimización de pesos
def optimizar_pesos_rig():
    """Re-optimiza los pesos del rig existente"""
    core = CarroRigCore()
    chasis, ruedas, ejes = buscar_objetos_escena_filtrado()
    if chasis:
        core.aplicar_skinning_inteligente(chasis, ruedas, ejes)
        cmds.confirmDialog(title="Éxito", message="✅ Pesos optimizados", button=["OK"])
    else:
        cmds.confirmDialog(title="Error", message="❌ No se encontró chasis", button=["OK"])

def crear_curvas_control_todos_joints():
    """Función global para crear las 9 curvas de control específicas"""
    core = CarroRigCore()
    return core.crear_curvas_control_joints()