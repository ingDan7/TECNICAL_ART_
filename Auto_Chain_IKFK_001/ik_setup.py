
# File: ik_setup.py
import maya.cmds as cmds


def setup_ik_chain(ik_chain):
    """ Configura la cadena IK con IK handle, pole vector y control IK. """
    upper, middle, end = ik_chain
    ik_handle = cmds.ikHandle(sj=upper, ee=end, sol="ikRPsolver", n="middleLeg_practice_L_IKhandle_001")[0]
    eff = cmds.listConnections(f"{ik_handle}.endEffector") or []
    if eff:
        cmds.rename(eff[0], "middleLeg_practice_L_effector_001")

    # Pole vector
    pv_group = cmds.group(empty=True, n="middleLeg_practice_L_IKpoleVector_001")
    pos = cmds.xform(middle, q=True, ws=True, t=True)
    cmds.xform(pv_group, ws=True, t=pos)
    pv_ctrl = cmds.circle(n="middleLeg_practice_L_IKpoleVectorCtrl_001", nr=(0,0,1), r=1)[0]
    shp = cmds.listRelatives(pv_ctrl, s=True)[0]
    cmds.parent(shp, pv_group, r=True, s=True)
    cmds.delete(pv_ctrl)
    cmds.move(0,0,5,pv_group, r=True, os=True)  # delante de la rodilla
    pv_root = cmds.group(pv_group, n="middleLeg_practice_L_IKpoleVectorRoot_001")
    cmds.poleVectorConstraint(pv_group, ik_handle)

    # IK control
    ik_ctrl = cmds.curve(d=1, p=[(-1,0,-1),(1,0,-1),(1,0,1),(-1,0,1),(-1,0,-1)], n="endLeg_practice_L_IKctrl_001")
    end_pos = cmds.xform(end, q=True, ws=True, t=True)
    cmds.xform(ik_ctrl, ws=True, t=end_pos)
    cmds.parent(ik_handle, ik_ctrl)
    return ik_handle, pv_group
