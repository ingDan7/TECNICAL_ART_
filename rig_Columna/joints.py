import maya.cmds as cmds
from .utils import get_curve_shape, get_ordered_nodes, safe_parent


def create_spine_joints_and_curve(open_curve=False):
    positions = [(0,8,0),(0,6,-2),(0,4,0),(0,2,2),(0,0,0)]
    joints = [cmds.joint(p=pos, name=f"joint_{i:03d}") for i,pos in enumerate(positions,1)]

    cmds.joint(joints[0], e=True, oj="xyz", sao="yup", ch=True, zso=True)
    for ax in "XYZ":
        cmds.setAttr(f"{joints[-1]}.jointOrient{ax}", 0)

    jnt_positions = [cmds.xform(j, q=True, ws=True, t=True) for j in joints]
    curve = cmds.curve(p=jnt_positions, d=3, name="splineCurve_001")

    cmds.rebuildCurve(curve, ch=False, rpo=True, rt=0, end=1, kr=0,
                      kcp=False, kep=True, kt=False,
                      s=(2 if open_curve else 10), d=6, tol=0.01)
    return joints, curve
