import maya.cmds as cmds
from .utils import get_curve_shape, get_ordered_nodes, safe_parent

def create_and_connect_locators_to_curve(curve="splineCurve_001"):
    curve_shape = get_curve_shape(curve)
    cmds.setAttr(f"{curve_shape}.dispCV", 1)
    cvs = cmds.ls(f"{curve_shape}.cv[*]", fl=True)
    locators = []
    for i, cv in enumerate(cvs,1):
        loc = cmds.spaceLocator(name=f"spineLoc_ctrl_{i:03d}")[0]
        cmds.xform(loc, ws=True, t=cmds.pointPosition(cv, w=True))
        cmds.connectAttr(f"{loc}.translate", f"{curve_shape}.controlPoints[{i-1}]", f=True)
        locators.append(loc)
    return locators, curve_shape

def connect_locators_with_decompose(curve="splineCurve_001"):
    curve_shape = get_curve_shape(curve)
    locators = get_ordered_nodes("spineLoc_ctrl_*")
    for i, loc in enumerate(locators):
        dm = cmds.createNode("decomposeMatrix", name=f"{loc}_dm")
        cmds.connectAttr(f"{loc}.worldMatrix[0]", f"{dm}.inputMatrix", f=True)
        cmds.connectAttr(f"{dm}.outputTranslate", f"{curve_shape}.controlPoints[{i}]", f=True)
        safe_parent(loc, curve)
    return locators, curve_shape
