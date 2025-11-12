# File: root_auto.py
import maya.cmds as cmds

def create_root_auto(joint, version="001"):
    """
    Crea los grupos root y auto para un joint FK y los alinea.
    Retorna (root_grp, auto_grp, joint).
    """
    if not cmds.objExists(joint):
        cmds.warning(f"❌ No existe el joint: {joint}")
        return None

    # Extraer prefijo base
    parts = joint.split("_")
    segment = parts[0]            # upperLeg, middleLeg, etc.
    base = "_".join(parts[1:-3])  # practice_L
    side = parts[-2]              # L o R

    # Nombres
    root_name = f"{segment}_{base}_FK_root_{version}"
    auto_name = f"{segment}_{base}_FK_auto_{version}"

    # Crear grupos vacíos
    root_grp = cmds.group(em=True, name=root_name)
    auto_grp = cmds.group(em=True, name=auto_name, parent=root_grp)

    # Alinear a joint
    cmds.delete(cmds.parentConstraint(joint, root_grp))
    cmds.delete(cmds.scaleConstraint(joint, root_grp))

    # Parentear joint dentro del auto
    cmds.parent(joint, auto_grp)

    return root_grp, auto_grp, joint
