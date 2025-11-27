import maya.cmds as cmds
from carro_rig_utils import (
    get_face_center, align_joint_to_position, align_to_object_center
)

class ModuloCadenas:
    """Maneja las cadenas de joints (deformación y drivers)"""
    
    def __init__(self, core):
        self.core = core
    
    def crear_cadena_deformacion(self, chasis, ruedas, ejes):
        """Crea cadena de joints de deformación"""
        print("🦴 Creando Cadena de Deformación...")
        
        try:
            # Joint raíz
            self.core.joints_deform[1] = self._crear_joint("joint_1", get_face_center(chasis, 3))
            
            # Joints principales
            joints_config = [
                (2, "eje_delantero", [3, 0, 0]),
                (4, "eje_trasero", [-3, 0, 0]),
                (3, None, None, lambda: get_face_center(chasis, 6)),
                (5, None, None, lambda: get_face_center(chasis, 16))
            ]
            
            for config in joints_config:
                self._crear_joint_principal(*config)
            
            # Joints de ruedas
            ruedas_config = [
                (6, "rueda_delantera_der"),
                (7, "rueda_delantera_izq"), 
                (8, "rueda_trasera_izq"),
                (9, "rueda_trasera_der")
            ]
            
            for joint_id, rueda_name in ruedas_config:
                self._crear_joint_rueda(joint_id, rueda_name)
            
            # Joint 10
            self._crear_joint_10()
            
            # Jerarquía
            self._construir_jerarquia_deformacion()
            
            print(f"✅ Cadena deformación: {len(self.core.joints_deform)} joints")
            return True
            
        except Exception as e:
            print(f"❌ Error en cadena deformación: {e}")
            return False
    
    def _crear_joint(self, nombre, posicion):
        """Crea joint en posición"""
        cmds.select(clear=True)
        joint = cmds.joint(name=nombre)
        align_joint_to_position(joint, posicion)
        return joint
    
    def _crear_joint_principal(self, joint_id, target_obj, fallback_offset=None, custom_pos=None):
        """Crea joint principal"""
        if custom_pos:
            posicion = custom_pos()
        elif cmds.objExists(target_obj):
            posicion = align_to_object_center(target_obj)
        else:
            pos_raiz = cmds.xform("joint_1", q=True, ws=True, t=True)
            posicion = [pos_raiz[0] + fallback_offset[0], pos_raiz[1] + fallback_offset[1], pos_raiz[2] + fallback_offset[2]]
        
        self.core.joints_deform[joint_id] = self._crear_joint(f"joint_{joint_id}", posicion)
    
    def _crear_joint_rueda(self, joint_id, rueda_name):
        """Crea joint de rueda"""
        if cmds.objExists(rueda_name):
            posicion = align_to_object_center(rueda_name)
        else:
            parent_id = 2 if joint_id <= 7 else 4
            pos_parent = cmds.xform(f"joint_{parent_id}", q=True, ws=True, t=True)
            offset_y = -1.5 if joint_id in [6, 9] else 1.5
            posicion = [pos_parent[0], pos_parent[1] - 1, pos_parent[2] + offset_y]
        
        self.core.joints_deform[joint_id] = self._crear_joint(f"joint_{joint_id}", posicion)
    
    def _crear_joint_10(self):
        """Crea joint 10 con limitación de altura"""
        self.core.joints_deform[10] = self._crear_joint("joint_10", [0, 0, 0])
        cmds.parent("joint_10", "joint_1")
        
        pos_j1 = cmds.xform("joint_1", q=True, ws=True, t=True)
        altura_max = self._obtener_altura_techo()
        
        altura_propuesta = pos_j1[1] + 1.147078
        altura_final = min(altura_propuesta, altura_max - 0.01) if altura_max else altura_propuesta
        
        cmds.xform("joint_10", ws=True, t=(pos_j1[0], altura_final, pos_j1[2]))
        print("🟦 joint_10 creado y limitado por techo")
    
    def _obtener_altura_techo(self):
        """Obtiene altura del techo"""
        try:
            if cmds.objExists("axioma_carro.f[1]"):
                centro = cmds.xform("axioma_carro.f[1]", q=True, ws=True, t=True)
                return centro[1]
        except: pass
        return None
    
    def _construir_jerarquia_deformacion(self):
        """Construye jerarquía de deformación"""
        jerarquia = {
            "joint_1": ["joint_2", "joint_4", "joint_10"],
            "joint_2": ["joint_3", "joint_6", "joint_7"],
            "joint_4": ["joint_5", "joint_8", "joint_9"]
        }
        
        for padre, hijos in jerarquia.items():
            for hijo in hijos:
                if cmds.objExists(hijo) and cmds.objExists(padre):
                    try: cmds.parent(hijo, padre)
                    except: pass
    
    def crear_cadena_drivers(self):
        """Crea cadena de drivers"""
        print("🎮 Creando Cadena de Drivers...")
        
        try:
            if not cmds.objExists("joint_1"):
                return False
                
            # Duplicar jerarquía
            driver_root = cmds.duplicate("joint_1", name="drv_joint_1", renameChildren=True)[0]
            self.core.joints_driver[1] = driver_root
            
            # Renombrar
            for i in range(2, 10):
                old_name = f"joint_{i}1"
                new_name = f"drv_joint_{i}"
                if cmds.objExists(old_name):
                    try:
                        cmds.rename(old_name, new_name)
                        self.core.joints_driver[i] = new_name
                    except: pass
            
            # Joint 10
            if cmds.objExists("joint_10"):
                pos = cmds.xform("joint_10", q=True, ws=True, t=True)
                self.core.joints_driver[10] = self._crear_joint("drv_joint_10", pos)
                cmds.parent("drv_joint_10", "drv_joint_1")
            
            # Joint 11 (root driver)
            try:
                dup = cmds.duplicate("drv_joint_1", rr=True)[0]
                drv_root = cmds.rename(dup, "drv_joint_11")
                self.core.joints_driver[11] = drv_root
                cmds.parentConstraint(drv_root, "drv_joint_1", mo=True)
                cmds.scaleConstraint(drv_root, "drv_joint_1", mo=True)
            except: pass
            
            # Color amarillo
            for joint in self.core.joints_driver.values():
                if cmds.objExists(joint):
                    try:
                        cmds.setAttr(f"{joint}.overrideEnabled", 1)
                        cmds.setAttr(f"{joint}.overrideColor", 17)
                    except: continue
            
            print(f"✅ Cadena drivers: {len(self.core.joints_driver)} joints")
            return True
            
        except Exception as e:
            print(f"❌ Error en cadena drivers: {e}")
            return False
    
    def conectar_drivers_a_deformacion(self):
        """Conecta drivers a deformación"""
        print("🔗 Conectando Drivers -> Deformación...")
        
        conectados = 0
        for i in range(1, 12):
            driver = f"drv_joint_{i}"
            deform = f"joint_{i}"
            
            if cmds.objExists(driver) and cmds.objExists(deform):
                try:
                    cmds.parentConstraint(driver, deform, maintainOffset=False)
                    cmds.scaleConstraint(driver, deform, maintainOffset=False)
                    conectados += 1
                except: pass
        
        print(f"✅ {conectados} conexiones establecidas")
        return conectados > 0