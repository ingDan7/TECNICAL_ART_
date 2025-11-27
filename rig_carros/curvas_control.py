import maya.cmds as cmds
from carro_rig_utils import create_control, get_face_center

class ModuloCurvas:
    """Maneja la creación de controles y curvas"""
    
    def __init__(self, core):
        self.core = core
        
        # Configuración
        self.config = {
            'radios_control': {1: 2.5, 2: 1.5, 3: 1.0, 4: 1.5, 5: 1.0, 6: 1.2, 7: 1.2, 8: 1.2, 9: 1.2},
            'colores_ruedas': {6: 13, 7: 13, 8: 14, 9: 14},
            'colores_chasis': {1: 6, 2: 6, 3: 6, 4: 6, 5: 6}
        }
    
    def crear_controles(self, chasis):
        """Crea todos los controles de animación"""
        print("🎨 Creando Controles...")
        
        try:
            # Control global
            self._crear_control_global(chasis)
            
            # Controles de chasis
            for i in range(1, 6):
                self._crear_control_individual(i)
            
            # Controles de ruedas
            print("    🎡 Creando controles de ruedas...")
            for i in range(6, 10):
                if self._crear_control_individual(i):
                    self._mejorar_control_rueda(self.core.controles[i]['ctrl'])
                    self._crear_curva_extra_rueda(i)
            
            print(f"✅ Controles creados: {len(self.core.controles)}")
            return True
            
        except Exception as e:
            print(f"❌ Error creando controles: {e}")
            return False
    
    def _crear_control_global(self, chasis):
        """Crea control global"""
        pos_centro = get_face_center(chasis, 3)
        ctrl, grp = create_control("ctrl_global", pos_centro, radius=5, color_index=22)
        self.core.controles['global'] = {'ctrl': ctrl, 'grp': grp}
    
    def _crear_control_individual(self, joint_id):
        """Crea control individual"""
        driver = f"drv_joint_{joint_id}"
        if not cmds.objExists(driver):
            return False
            
        pos = cmds.xform(driver, q=True, ws=True, t=True)
        ctrl_name = f"ctrl_joint_{joint_id}"
        
        radio = self.config['radios_control'].get(joint_id, 1.0)
        color = self.config['colores_ruedas'].get(joint_id) or self.config['colores_chasis'].get(joint_id, 6)
        
        ctrl, grp = create_control(ctrl_name, pos, radius=radio, color_index=color)
        self.core.controles[joint_id] = {'ctrl': ctrl, 'grp': grp}
        return True
    
    def _mejorar_control_rueda(self, ctrl):
        """Mejora la forma del control de rueda"""
        try:
            # Limpiar shapes existentes
            shapes = cmds.listRelatives(ctrl, shapes=True) or []
            if shapes: cmds.delete(shapes)
            
            pos = cmds.xform(ctrl, q=True, ws=True, t=True)
            
            # Crear formas en plano YZ
            circle = cmds.circle(center=(0,0,0), normal=(1,0,0), radius=1.2, sections=16)[0]
            line1 = cmds.curve(d=1, p=[(0,-1.2,0), (0,1.2,0)], k=[0,1])
            line2 = cmds.curve(d=1, p=[(0,0,-1.2), (0,0,1.2)], k=[0,1])
            
            # Posicionar
            for obj in [circle, line1, line2]:
                cmds.xform(obj, ws=True, t=pos)
            
            # Combinar shapes
            for shape_obj in [circle, line1, line2]:
                shape = cmds.listRelatives(shape_obj, shapes=True)[0]
                cmds.parent(shape, ctrl, relative=True, shape=True)
            
            # Limpiar
            cmds.delete(circle, line1, line2)
            
            # Color
            color_idx = 13 if "joint_6" in ctrl or "joint_9" in ctrl else 14
            shapes = cmds.listRelatives(ctrl, shapes=True) or []
            for shape in shapes:
                try:
                    cmds.setAttr(f"{shape}.overrideEnabled", 1)
                    cmds.setAttr(f"{shape}.overrideColor", color_idx)
                except: continue
                    
        except Exception as e:
            print(f"    ⚠️ Error mejorando control rueda: {e}")
    
    def _crear_curva_extra_rueda(self, joint_id):
        """Crea curva extra para rueda"""
        driver = f"drv_joint_{joint_id}"
        if not cmds.objExists(driver):
            return None
        
        pos = cmds.xform(driver, q=True, ws=True, t=True)
        ctrl_name = f"ctrl_joint_{joint_id}_extra"
        
        try:
            ctrl, grp = create_control(ctrl_name, pos, radius=0.8, color_index=17)
            
            # Parent al control principal
            if joint_id in self.core.controles:
                try: cmds.parent(grp, self.core.controles[joint_id]['ctrl'])
                except: pass
            
            # Constraint
            try: cmds.parentConstraint(ctrl, driver, maintainOffset=True)
            except: pass
            
            return ctrl, grp
        except: return None
    
    def conectar_controles_a_drivers(self):
        """Conecta controles a drivers"""
        print("🔗 Conectando Controles -> Drivers...")
        
        conectados = 0
        for i in range(1, 12):
            ctrl = f"ctrl_joint_{i}"
            driver = f"drv_joint_{i}"
            
            if cmds.objExists(ctrl) and cmds.objExists(driver):
                try:
                    cmds.parentConstraint(ctrl, driver, maintainOffset=True)
                    conectados += 1
                except: pass
        
        print(f"✅ {conectados} conexiones Control->Driver")
        return conectados > 0