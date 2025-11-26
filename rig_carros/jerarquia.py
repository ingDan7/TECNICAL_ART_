import maya.cmds as cmds
from carro_rig_utils import NOMBRES_ESTANDAR

class ModuloJerarquia:
    """Maneja la organización y jerarquía del rig"""
    
    def __init__(self, core):
        self.core = core
    
    def organizar_jerarquia(self):
        """Organiza todos los elementos en jerarquía limpia"""
        print("📁 Organizando jerarquía...")
        
        try:
            # Grupo principal
            rig_grp = cmds.group(empty=True, name=NOMBRES_ESTANDAR["grupo_rig"]) 
            
            # Grupo de joints
            joints_grp = cmds.group(empty=True, name="JOINTS_GRP")
            self._organizar_joints(joints_grp)
            
            # Grupo de controles
            controles_grp = cmds.group(empty=True, name="CONTROLES_GRP")
            self._organizar_controles(controles_grp)
            
            # Jerarquía final
            cmds.parent(joints_grp, rig_grp)
            cmds.parent(controles_grp, rig_grp)
            
            # Ocultar cadena de deformación
            if cmds.objExists("joint_1"):
                cmds.setAttr("joint_1.visibility", 0)
            
            print("✅ Jerarquía organizada")
            return True
            
        except Exception as e:
            print(f"❌ Error organizando jerarquía: {e}")
            return False
    
    def _organizar_joints(self, joints_grp):
        """Organiza joints en grupo"""
        for obj in ["joint_1", "drv_joint_1"]:
            if cmds.objExists(obj):
                try: cmds.parent(obj, joints_grp)
                except: pass
    
    def _organizar_controles(self, controles_grp):
        """Organiza controles en grupo"""
        if 'global' in self.core.controles:
            try:
                cmds.parent(self.core.controles['global']['grp'], controles_grp)
            except: pass
            
            # Parentear controles individuales al global
            global_ctrl = self.core.controles['global']['ctrl']
            for i in range(1, 12):
                if i in self.core.controles:
                    try:
                        cmds.parent(self.core.controles[i]['grp'], global_ctrl)
                    except: pass