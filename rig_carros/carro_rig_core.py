import maya.cmds as cmds
from .carro_rig_utils import get_face_center, align_joint_to_position, align_to_object_center, create_control

def crear_rig_carro():
    chasis = "chasis_carro"
    ruedas = [
        "rueda_delantera_izq",
        "rueda_delantera_der",
        "rueda_trasera_izq",
        "rueda_trasera_der"
    ]

    # Validaciones
    if not cmds.objExists(chasis):
        cmds.confirmDialog(
            title="Error",
            message="❌ No se encontró 'chasis_carro' en la escena.",
            button=["OK"]
        )
        return

    for r in ruedas:
        if not cmds.objExists(r):
            cmds.warning(f"⚠️ No se encontró '{r}' en la escena.")

    # Crear joints de la columna (1–5)
    pos_face2 = get_face_center(chasis, 2)
    pos_face0 = get_face_center(chasis, 0)

    columna = []
    for i in range(5):
        j = cmds.joint(name=f"joint_{i+1}")
        columna.append(j)
    cmds.select(clear=True)

    for i, jnt in enumerate(columna):
        t = i / 4.0
        pos = [
            pos_face2[0] + (pos_face0[0] - pos_face2[0]) * t,
            pos_face2[1] + (pos_face0[1] - pos_face2[1]) * t,
            pos_face2[2] + (pos_face0[2] - pos_face2[2]) * t,
        ]
        align_joint_to_position(jnt, pos)

    # Crear locators (3 zonas)
    loc_maletero = cmds.spaceLocator(name="loc_maletero")[0]
    loc_cabina = cmds.spaceLocator(name="loc_cabina")[0]
    loc_capo = cmds.spaceLocator(name="loc_capo")[0]

    cmds.xform(loc_maletero, ws=True, t=cmds.xform(columna[1], q=True, ws=True, t=True))
    cmds.xform(loc_cabina, ws=True, t=cmds.xform(columna[2], q=True, ws=True, t=True))
    cmds.xform(loc_capo, ws=True, t=cmds.xform(columna[4], q=True, ws=True, t=True))

    # Vincular joints con locators
    cmds.parentConstraint(loc_maletero, columna[0], mo=True)
    cmds.parentConstraint(loc_maletero, columna[1], mo=True)
    cmds.parentConstraint(loc_cabina, columna[2], mo=True)
    cmds.parentConstraint(loc_capo, columna[3], mo=True)
    cmds.parentConstraint(loc_capo, columna[4], mo=True)

    # Crear controles principales
    ctrl_mal, grp_mal = create_control("ctrl_maletero", cmds.xform(loc_maletero, q=True, ws=True, t=True), 1.5, 17)
    ctrl_cab, grp_cab = create_control("ctrl_cabina", cmds.xform(loc_cabina, q=True, ws=True, t=True), 1.8, 6)
    ctrl_cap, grp_cap = create_control("ctrl_capo", cmds.xform(loc_capo, q=True, ws=True, t=True), 1.5, 14)

    cmds.parentConstraint(ctrl_mal, loc_maletero, mo=True)
    cmds.parentConstraint(ctrl_cab, loc_cabina, mo=True)
    cmds.parentConstraint(ctrl_cap, loc_capo, mo=True)

    # Ruedas (6–9)
    for i, nombre in enumerate(ruedas, start=6):
        if not cmds.objExists(nombre):
            continue
        pos = align_to_object_center(nombre)
        j = cmds.joint(name=f"joint_{i}")
        cmds.xform(j, ws=True, t=pos)
        if "delantera" in nombre:
            cmds.parent(j, columna[4])
        else:
            cmds.parent(j, columna[1])

        ctrl, grp = create_control(f"ctrl_{nombre}", pos, radius=1.2, color_index=13)
        cmds.parentConstraint(ctrl, j, mo=True)

    cmds.select(clear=True)

    # Control global
    global_ctrl, global_grp = create_control("ctrl_global", pos_face2, radius=5, color_index=22)
    cmds.parent(grp_mal, grp_cab, grp_cap, global_ctrl)

    for nombre in ruedas:
        if cmds.objExists(f"ctrl_{nombre}_GRP"):
            cmds.parent(f"ctrl_{nombre}_GRP", global_ctrl)

    rig_grp = cmds.group(global_grp, name="RIG_CARRO_GRP")

    # Confirmación
    cmds.confirmDialog(
        title="Rig del Carro",
        message="✅ Rig del carro creado correctamente.\n\n- 3 controles de columna\n- 4 controles de ruedas\n- 1 control global",
        button=["OK"]
    )