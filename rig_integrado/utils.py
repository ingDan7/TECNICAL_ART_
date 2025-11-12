import maya.cmds as cmds
import re

def get_curve_shape(curve):
    shapes = cmds.listRelatives(curve, shapes=True, f=True) or []
    return shapes[0] if shapes else None

def get_ordered_nodes(pattern, node_type="transform"):
    nodes = cmds.ls(pattern, type=node_type) or []
    def sort_key(x):
        digits = re.findall(r"\d+", x)
        return int(digits[-1]) if digits else 0
    return sorted(nodes, key=sort_key)

def safe_parent(child, parent):
    if cmds.objExists(child) and cmds.objExists(parent):
        try: cmds.parent(child, parent)
        except: pass
