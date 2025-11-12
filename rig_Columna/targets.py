import maya.cmds as cmds
from .utils import get_curve_shape, get_ordered_nodes

def create_targets_on_curve(curve="splineCurve_001", num_targets=5):
    curve_shape = get_curve_shape(curve)
    targets = []
    for i in range(num_targets):
        loc = cmds.spaceLocator(name=f"spineTarget_ctrl_{i+1:03d}")[0]
        pci = cmds.createNode("pointOnCurveInfo", name=f"pointOnCurveInfo_{i+1:03d}")
        cmds.connectAttr(f"{curve_shape}.worldSpace[0]", f"{pci}.inputCurve", f=True)
        cmds.connectAttr(f"{pci}.position", f"{loc}.translate", f=True)
        cmds.setAttr(f"{pci}.parameter", float(i)/(num_targets-1))
        targets.append(loc)
    return targets

def redirect_targets_with_aim():
    targets = get_ordered_nodes("spineTarget_ctrl_*")
    for i in range(1,len(targets)):
        cmds.aimConstraint(targets[i], targets[i-1], mo=False,
                           aimVector=(1,0,0), upVector=(0,1,0),
                           worldUpType="scene")
    return targets

def parent_constraint_joints_to_targets(num_pairs=5):
    for i in range(1,num_pairs+1):
        t, j = f"spineTarget_ctrl_{i:03d}", f"joint_{i:03d}"
        if cmds.objExists(t) and cmds.objExists(j):
            cmds.parentConstraint(t, j, mo=True)
