# File: fk_setup.py
import maya.cmds as cmds
from .root_auto import create_root_auto

def setup_fk_chain(fk_chain, version="001"):
    """
    Crea la jerarquía FK con estructura anidada root > auto > joint > ctrl.
    """
    if not fk_chain:
        cmds.warning("❌ No hay joints FK disponibles.")
        return

    root_groups = []
    prev_joint = None

    for i, joint in enumerate(fk_chain):
        result = create_root_auto(joint, version)
        if not result:
            continue

        root_grp, auto_grp, joint = result
        root_groups.append(root_grp)

        # Crear control FK
        ctrl_name = joint.replace("_joint_", "_ctrl_")
        if not cmds.objExists(ctrl_name):
            ctrl = cmds.circle(name=ctrl_name, normal=[1, 0, 0], radius=1.5)[0]
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.parent(shape, joint, r=True, s=True)
            cmds.delete(ctrl)

        # 🔥 Parentar root actual dentro del joint anterior
        if prev_joint:
            cmds.parent(root_grp, prev_joint)

        prev_joint = joint

    print("✅ Jerarquía FK conectada correctamente.")
