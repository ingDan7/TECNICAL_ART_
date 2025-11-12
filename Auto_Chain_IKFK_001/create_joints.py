# File: create_joints.py
import maya.cmds as cmds

def duplicate_chain(chain, ctype, version):
    new_chain = []
    for j in chain:
        dup = cmds.duplicate(j, po=True)[0]
        new_name = j.replace("_joint", f"_{ctype}_joint_{version}")
        new_joint = cmds.rename(dup, new_name)
        new_chain.append(new_joint)
    for i in range(len(new_chain)-1):
        cmds.parent(new_chain[i+1], new_chain[i])
    return new_chain


def build_chains():
    """ Crea la cadena base y duplica para FK, IK y MAIN. Elimina la cadena base después. """
    cmds.select(clear=True)
    upper = cmds.joint(p=(0, 8, 0), name="upperLeg_practice_L_joint")
    middle = cmds.joint(p=(0, 4, 0.5), name="middleLeg_practice_L_joint")
    end = cmds.joint(p=(0, 0, 0), name="endLeg_practice_L_joint")
    cmds.joint(upper, e=True, oj="xyz", sao="yup")
    for ax in ["X","Y","Z"]:
        cmds.setAttr(f"{end}.jointOrient{ax}", 0)
    base_chain = [upper, middle, end]

    fk_chain = duplicate_chain(base_chain, "FK", "001")
    ik_chain = duplicate_chain(base_chain, "IK", "002")
    main_chain = duplicate_chain(base_chain, "MAIN", "003")

    # Eliminar base
    if cmds.objExists(base_chain[0]):
        cmds.delete(base_chain[0])
    return fk_chain, ik_chain, main_chain
