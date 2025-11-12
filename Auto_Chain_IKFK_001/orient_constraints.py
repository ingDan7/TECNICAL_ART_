

# File: orient_constraints.py
import maya.cmds as cmds


def setup_main_chain(fk_chain, ik_chain, main_chain):
    """ Crea constraints de MAIN a FK/IK y añade el switch FKIK. """
    constraints_info = []
    for fk, ik, main in zip(fk_chain, ik_chain, main_chain):
        pos = cmds.xform(fk, q=True, ws=True, t=True)
        rot = cmds.xform(fk, q=True, ws=True, ro=True)
        cmds.xform(main, ws=True, t=pos, ro=rot)
        cns = cmds.parentConstraint(fk, ik, main, mo=False)[0]
        constraints_info.append({"constraint":cns,"fk":fk,"ik":ik})

    # Locator con atributo FKIK
    loc = cmds.spaceLocator(n="Leg_practice_L_attributes_001")[0]
    if not cmds.attributeQuery("FKIK", n=loc, ex=True):
        cmds.addAttr(loc, ln="FKIK", at="double", min=0, max=1, dv=0, k=True)
    rev = cmds.createNode("reverse", n="FKIK_reverse")
    cmds.connectAttr(f"{loc}.FKIK", f"{rev}.inputX", f=True)

    # Parentar locator al primer joint FK
    try:
        cmds.parent(loc, fk_chain[0])
    except:
        pass

    # Conexiones
    for info in constraints_info:
        cns = info["constraint"]
        weights = cmds.parentConstraint(cns, q=True, wal=True)
        if len(weights) >= 2:
            fk_attr = f"{cns}.{weights[0]}"
            ik_attr = f"{cns}.{weights[1]}"
            cmds.connectAttr(f"{loc}.FKIK", ik_attr, f=True)
            cmds.connectAttr(f"{rev}.outputX", fk_attr, f=True)