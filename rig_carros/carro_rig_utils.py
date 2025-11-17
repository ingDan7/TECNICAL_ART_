# # import maya.cmds as cmds
# # from carro_rig_utils import get_face_center, align_joint_to_position, align_to_object_center, create_control

# # def crear_rig_carro(*_):
# #     chasis = "chasis_carro"
# #     ruedas = [
# #         "rueda_delantera_izq",
# #         "rueda_delantera_der",
# #         "rueda_trasera_izq",
# #         "rueda_trasera_der"
# #     ]

# #     # -----------------------------
# #     # Validaciones
# #     # -----------------------------
# #     if not cmds.objExists(chasis):
# #         cmds.confirmDialog(
# #             title="Error",
# #             message="❌ No se encontró 'chasis_carro' en la escena.",
# #             button=["OK"]
# #         )
# #         return

# #     for r in ruedas:
# #         if not cmds.objExists(r):
# #             cmds.warning(f"⚠️ No se encontró '{r}' en la escena.")

# #     # -----------------------------
# #     # Crear joints de la columna (1–5)
# #     # -----------------------------
# #     pos_face2 = get_face_center(chasis, 2)
# #     pos_face0 = get_face_center(chasis, 0)

# #     columna = []
# #     for i in range(5):
# #         j = cmds.joint(name=f"joint_{i+1}")
# #         columna.append(j)
# #     cmds.select(clear=True)

# #     for i, jnt in enumerate(columna):
# #         t = i / 4.0
# #         pos = [
# #             pos_face2[0] + (pos_face0[0] - pos_face2[0]) * t,
# #             pos_face2[1] + (pos_face0[1] - pos_face2[1]) * t,
# #             pos_face2[2] + (pos_face0[2] - pos_face2[2]) * t,
# #         ]
# #         align_joint_to_position(jnt, pos)

# #     # -----------------------------
# #     # Crear locators (3 zonas)
# #     # -----------------------------
# #     loc_maletero = cmds.spaceLocator(name="loc_maletero")[0]
# #     loc_cabina = cmds.spaceLocator(name="loc_cabina")[0]
# #     loc_capo = cmds.spaceLocator(name="loc_capo")[0]

# #     cmds.xform(loc_maletero, ws=True, t=cmds.xform(columna[1], q=True, ws=True, t=True))
# #     cmds.xform(loc_cabina, ws=True, t=cmds.xform(columna[2], q=True, ws=True, t=True))
# #     cmds.xform(loc_capo, ws=True, t=cmds.xform(columna[4], q=True, ws=True, t=True))

# #     # -----------------------------
# #     # Vincular joints con locators
# #     # -----------------------------
# #     cmds.parentConstraint(loc_maletero, columna[0], mo=True)
# #     cmds.parentConstraint(loc_maletero, columna[1], mo=True)
# #     cmds.parentConstraint(loc_cabina, columna[2], mo=True)
# #     cmds.parentConstraint(loc_capo, columna[3], mo=True)
# #     cmds.parentConstraint(loc_capo, columna[4], mo=True)

# #     # -----------------------------
# #     # Crear controles principales
# #     # -----------------------------
# #     ctrl_mal, grp_mal = create_control("ctrl_maletero", cmds.xform(loc_maletero, q=True, ws=True, t=True), 1.5, 17)
# #     ctrl_cab, grp_cab = create_control("ctrl_cabina", cmds.xform(loc_cabina, q=True, ws=True, t=True), 1.8, 6)
# #     ctrl_cap, grp_cap = create_control("ctrl_capo", cmds.xform(loc_capo, q=True, ws=True, t=True), 1.5, 14)

# #     cmds.parentConstraint(ctrl_mal, loc_maletero, mo=True)
# #     cmds.parentConstraint(ctrl_cab, loc_cabina, mo=True)
# #     cmds.parentConstraint(ctrl_cap, loc_capo, mo=True)

# #     # -----------------------------
# #     # Ruedas (6–9)
# #     # -----------------------------
# #     for i, nombre in enumerate(ruedas, start=6):
# #         if not cmds.objExists(nombre):
# #             continue
# #         pos = align_to_object_center(nombre)
# #         j = cmds.joint(name=f"joint_{i}")
# #         cmds.xform(j, ws=True, t=pos)
# #         if "delantera" in nombre:
# #             cmds.parent(j, columna[4])
# #         else:
# #             cmds.parent(j, columna[1])

# #         ctrl, grp = create_control(f"ctrl_{nombre}", pos, radius=1.2, color_index=13)
# #         cmds.parentConstraint(ctrl, j, mo=True)

# #     cmds.select(clear=True)

# #     # -----------------------------
# #     # Control global
# #     # -----------------------------
# #     global_ctrl, global_grp = create_control("ctrl_global", pos_face2, radius=5, color_index=22)
# #     cmds.parent(grp_mal, grp_cab, grp_cap, global_ctrl)

# #     for nombre in ruedas:
# #         if cmds.objExists(f"ctrl_{nombre}_GRP"):
# #             cmds.parent(f"ctrl_{nombre}_GRP", global_ctrl)

# #     rig_grp = cmds.group(global_grp, name="RIG_CARRO_GRP")

# #     # -----------------------------
# #     # Confirmación
# #     # -----------------------------
# #     cmds.confirmDialog(
# #         title="Rig del Carro",
# #         message="✅ Rig del carro creado correctamente.\n\n- 3 controles de columna\n- 4 controles de ruedas\n- 1 control global",
# #         button=["OK"]
# #     )


# import maya.cmds as cmds
# import maya.api.OpenMaya as om

# def get_face_center(obj, face_index):
#     """Devuelve el centro de una cara dada de un objeto."""
#     try:
#         sel_list = om.MSelectionList()
#         sel_list.add(f"{obj}.f[{face_index}]")
#         dag_path, comp = sel_list.getComponent(0)
#         mfn_mesh = om.MFnMesh(dag_path)
#         face_points = mfn_mesh.getPolygonVertices(face_index)
#         points = [mfn_mesh.getPoint(vtx, om.MSpace.kWorld) for vtx in face_points]
#         avg_point = om.MPoint(
#             sum(p.x for p in points) / len(points),
#             sum(p.y for p in points) / len(points),
#             sum(p.z for p in points) / len(points)
#         )
#         return [avg_point.x, avg_point.y, avg_point.z]
#     except:
#         # Fallback: usar bounding box
#         bb = cmds.exactWorldBoundingBox(obj)
#         return [(bb[0]+bb[3])/2, (bb[1]+bb[4])/2, (bb[2]+bb[5])/2]

# def align_joint_to_position(joint, position):
#     cmds.xform(joint, ws=True, t=position)

# def align_to_object_center(obj):
#     """Devuelve el centro de un objeto."""
#     bb = cmds.exactWorldBoundingBox(obj)
#     return [(bb[0]+bb[3])/2, (bb[1]+bb[4])/2, (bb[2]+bb[5])/2]

# def create_control(name, position, radius=1.0, color_index=6):
#     """Crea un control circular en la posición dada."""
#     ctrl = cmds.circle(name=name, nr=(0,1,0), r=radius)[0]
#     grp = cmds.group(ctrl, name=f"{name}_GRP")
#     cmds.xform(grp, ws=True, t=position)
#     shape = cmds.listRelatives(ctrl, s=True)[0]
#     cmds.setAttr(shape + ".overrideEnabled", 1)
#     cmds.setAttr(shape + ".overrideColor", color_index)
#     return ctrl, grp

# def buscar_objetos_escena():
#     """Busca automáticamente chasis y ruedas en la escena por nombre."""
#     objetos = cmds.ls(transforms=True)
    
#     chasis = None
#     ruedas = []
    
#     # Buscar chasis
#     for obj in objetos:
#         if "chasis" in obj.lower() and "carro" in obj.lower():
#             chasis = obj
#             break
    
#     # Si no encuentra, buscar cualquier objeto con "chasis"
#     if not chasis:
#         for obj in objetos:
#             if "chasis" in obj.lower():
#                 chasis = obj
#                 break
    
#     # Buscar ruedas
#     for obj in objetos:
#         if "rueda" in obj.lower() or "llanta" in obj.lower() or "wheel" in obj.lower():
#             ruedas.append(obj)
    
#     # Ordenar ruedas por posición para determinar delanteras/traseras
#     if len(ruedas) >= 4:
#         ruedas_ordenadas = sorted(ruedas, key=lambda x: cmds.xform(x, q=True, ws=True, t=True)[2])
#         ruedas_delanteras = ruedas_ordenadas[:2]
#         ruedas_traseras = ruedas_ordenadas[2:4]
        
#         # Asignar nombres específicos
#         ruedas_nombradas = [
#             f"rueda_delantera_izq",
#             f"rueda_delantera_der", 
#             f"rueda_trasera_izq",
#             f"rueda_trasera_der"
#         ]
        
#         return chasis, ruedas_nombradas
    
#     return chasis, ruedas[:4]  # Máximo 4 ruedas


import maya.cmds as cmds
import maya.api.OpenMaya as om

def get_face_center(obj, face_index):
    """Devuelve el centro de una cara dada de un objeto."""
    try:
        sel_list = om.MSelectionList()
        sel_list.add(f"{obj}.f[{face_index}]")
        dag_path, comp = sel_list.getComponent(0)
        mfn_mesh = om.MFnMesh(dag_path)
        face_points = mfn_mesh.getPolygonVertices(face_index)
        points = [mfn_mesh.getPoint(vtx, om.MSpace.kWorld) for vtx in face_points]
        avg_point = om.MPoint(
            sum(p.x for p in points) / len(points),
            sum(p.y for p in points) / len(points),
            sum(p.z for p in points) / len(points)
        )
        return [avg_point.x, avg_point.y, avg_point.z]
    except:
        # Fallback: usar bounding box
        bb = cmds.exactWorldBoundingBox(obj)
        return [(bb[0]+bb[3])/2, (bb[1]+bb[4])/2, (bb[2]+bb[5])/2]

def align_joint_to_position(joint, position):
    cmds.xform(joint, ws=True, t=position)

def align_to_object_center(obj):
    """Devuelve el centro de un objeto."""
    bb = cmds.exactWorldBoundingBox(obj)
    return [(bb[0]+bb[3])/2, (bb[1]+bb[4])/2, (bb[2]+bb[5])/2]

def create_control(name, position, radius=1.0, color_index=6):
    """Crea un control circular en la posición dada."""
    ctrl = cmds.circle(name=name, nr=(0,1,0), r=radius)[0]
    grp = cmds.group(ctrl, name=f"{name}_GRP")
    cmds.xform(grp, ws=True, t=position)
    shape = cmds.listRelatives(ctrl, s=True)[0]
    cmds.setAttr(shape + ".overrideEnabled", 1)
    cmds.setAttr(shape + ".overrideColor", color_index)
    return ctrl, grp

def buscar_objetos_escena():
    """Busca automáticamente chasis y ruedas en la escena por nombre."""
    objetos = cmds.ls(transforms=True)
    
    chasis = None
    ruedas = []
    
    # Buscar chasis
    for obj in objetos:
        if "chasis" in obj.lower() and "carro" in obj.lower():
            chasis = obj
            break
    
    # Si no encuentra, buscar cualquier objeto con "chasis"
    if not chasis:
        for obj in objetos:
            if "chasis" in obj.lower():
                chasis = obj
                break
    
    # Buscar ruedas
    for obj in objetos:
        if "rueda" in obj.lower() or "llanta" in obj.lower() or "wheel" in obj.lower():
            ruedas.append(obj)
    
    # Ordenar ruedas por posición para determinar delanteras/traseras
    if len(ruedas) >= 4:
        ruedas_ordenadas = sorted(ruedas, key=lambda x: cmds.xform(x, q=True, ws=True, t=True)[2])
        ruedas_delanteras = ruedas_ordenadas[:2]
        ruedas_traseras = ruedas_ordenadas[2:4]
        
        # Asignar nombres específicos
        ruedas_nombradas = [
            f"rueda_delantera_izq",
            f"rueda_delantera_der", 
            f"rueda_trasera_izq",
            f"rueda_trasera_der"
        ]
        
        return chasis, ruedas_nombradas
    
    return chasis, ruedas[:4]  # Máximo 4 ruedas