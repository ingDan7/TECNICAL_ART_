import maya.cmds as cmds
from .utils import get_ordered_nodes, safe_parent

def organize_spine_ik_controls(curve="splineCurve_001"):
    locators = get_ordered_nodes("spineLoc_ctrl_*")
    root_groups = []
    for loc in locators:
        root = cmds.group(empty=True, name=loc.replace("spineLoc_ctrl_", "spineLocRoot_ctrl_"))
        cmds.delete(cmds.parentConstraint(loc, root))  # snap
        cmds.parent(loc, root)
        cmds.setAttr(f"{loc}.t",0,0,0), cmds.setAttr(f"{loc}.r",0,0,0)
        safe_parent(root, curve)
        circle = cmds.circle(nr=(0,1,0), r=0.5)[0]
        for shp in cmds.listRelatives(circle, shapes=True) or []:
            cmds.parent(shp, loc, r=True, s=True)
        cmds.delete(circle)
        root_groups.append(root)
    safe_parent("spineLocRoot_ctrl_002", "spineLoc_ctrl_001")
    safe_parent("spineLocRoot_ctrl_004", "spineLoc_ctrl_005")

    return root_groups, locators
