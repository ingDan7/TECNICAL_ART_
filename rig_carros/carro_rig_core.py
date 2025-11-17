# import maya.cmds as cmds
# from carro_rig_utils import get_face_center, align_joint_to_position, align_to_object_center, create_control, buscar_objetos_escena

# def limpiar_rig_existente():
#     """Limpia todos los elementos del rig anterior."""
#     elementos_rig = [
#         "RIG_CARRO_GRP", "ctrl_global", "ctrl_global_GRP",
#         "ctrl_maletero", "ctrl_maletero_GRP", "ctrl_cabina", "ctrl_cabina_GRP",
#         "ctrl_capo", "ctrl_capo_GRP", "loc_maletero", "loc_cabina", "loc_capo"
#     ]
    
#     # Agregar joints y controles de ruedas
#     for i in range(1, 10):
#         elementos_rig.append(f"joint_{i}")
    
#     ruedas_tipos = ["delantera_izq", "delantera_der", "trasera_izq", "trasera_der"]
#     for rueda in ruedas_tipos:
#         elementos_rig.extend([f"ctrl_rueda_{rueda}", f"ctrl_rueda_{rueda}_GRP"])
    
#     # Buscar controles de ruedas con nombres específicos
#     ruedas_nombres = [
#         "rueda_delantera_izq", "rueda_delantera_der", 
#         "rueda_trasera_izq", "rueda_trasera_der"
#     ]
#     for rueda in ruedas_nombres:
#         elementos_rig.extend([f"ctrl_{rueda}", f"ctrl_{rueda}_GRP"])
    
#     elementos_eliminados = []
#     for elem in elementos_rig:
#         if cmds.objExists(elem):
#             try:
#                 cmds.delete(elem)
#                 elementos_eliminados.append(elem)
#             except:
#                 pass
    
#     return len(elementos_eliminados)

# def ajustar_rig_existente():
#     """Ajusta el rig existente a la geometría actual del carro."""
#     if not cmds.objExists("RIG_CARRO_GRP"):
#         cmds.confirmDialog(title="Error", message="❌ No hay rig existente para ajustar.", button=["OK"])
#         return False
    
#     chasis, ruedas = buscar_objetos_escena()
    
#     if not chasis:
#         cmds.confirmDialog(title="Error", message="❌ No se encontró chasis en la escena.", button=["OK"])
#         return False
    
#     try:
#         # Actualizar posición de joints de columna
#         pos_face2 = get_face_center(chasis, 2)
#         pos_face0 = get_face_center(chasis, 0)
        
#         for i in range(1, 6):
#             jnt = f"joint_{i}"
#             if cmds.objExists(jnt):
#                 t = (i-1) / 4.0
#                 pos = [
#                     pos_face2[0] + (pos_face0[0] - pos_face2[0]) * t,
#                     pos_face2[1] + (pos_face0[1] - pos_face2[1]) * t,
#                     pos_face2[2] + (pos_face0[2] - pos_face2[2]) * t,
#                 ]
#                 align_joint_to_position(jnt, pos)
        
#         # Actualizar locators
#         if cmds.objExists("loc_maletero"):
#             cmds.xform("loc_maletero", ws=True, t=cmds.xform("joint_2", q=True, ws=True, t=True))
#         if cmds.objExists("loc_cabina"):
#             cmds.xform("loc_cabina", ws=True, t=cmds.xform("joint_3", q=True, ws=True, t=True))
#         if cmds.objExists("loc_capo"):
#             cmds.xform("loc_capo", ws=True, t=cmds.xform("joint_5", q=True, ws=True, t=True))
        
#         # Actualizar controles principales
#         controles_principales = {
#             "ctrl_maletero": "loc_maletero",
#             "ctrl_cabina": "loc_cabina", 
#             "ctrl_capo": "loc_capo"
#         }
        
#         for ctrl, loc in controles_principales.items():
#             if cmds.objExists(ctrl) and cmds.objExists(loc):
#                 pos = cmds.xform(loc, q=True, ws=True, t=True)
#                 cmds.xform(f"{ctrl}_GRP", ws=True, t=pos)
        
#         # Actualizar ruedas
#         for i, nombre_rueda in enumerate(ruedas, start=6):
#             if i <= 9 and cmds.objExists(f"joint_{i}"):
#                 # Buscar objeto de rueda real
#                 rueda_obj = None
#                 for obj in cmds.ls(transforms=True):
#                     if "rueda" in obj.lower() or "llanta" in obj.lower() or "wheel" in obj.lower():
#                         rueda_obj = obj
#                         break
                
#                 if rueda_obj:
#                     pos = align_to_object_center(rueda_obj)
#                     cmds.xform(f"joint_{i}", ws=True, t=pos)
                    
#                     # Actualizar control de rueda
#                     ctrl_name = f"ctrl_{nombre_rueda}"
#                     if cmds.objExists(ctrl_name):
#                         cmds.xform(f"{ctrl_name}_GRP", ws=True, t=pos)
        
#         # Actualizar control global
#         if cmds.objExists("ctrl_global"):
#             cmds.xform("ctrl_global_GRP", ws=True, t=pos_face2)
        
#         cmds.confirmDialog(
#             title="Ajuste Completado", 
#             message="✅ Rig ajustado correctamente al carro actual.", 
#             button=["OK"]
#         )
#         return True
        
#     except Exception as e:
#         cmds.confirmDialog(title="Error", message=f"❌ Error al ajustar rig: {str(e)}", button=["OK"])
#         return False

# def crear_rig_carro(*_):
#     """Crea o regenera el rig completo del carro."""
#     # Limpiar rig existente primero
#     elementos_eliminados = limpiar_rig_existente()
    
#     # Buscar objetos automáticamente
#     chasis, ruedas = buscar_objetos_escena()
    
#     if not chasis:
#         cmds.confirmDialog(
#             title="Error",
#             message="❌ No se encontró chasis en la escena.\n\nNombres sugeridos:\n- chasis_carro\n- chasis\n- car_body",
#             button=["OK"]
#         )
#         return

#     # Renombrar objetos encontrados para consistencia
#     chasis_renombrado = "chasis_carro"
#     if chasis != chasis_renombrado:
#         try:
#             cmds.rename(chasis, chasis_renombrado)
#         except:
#             pass
    
#     ruedas_renombradas = [
#         "rueda_delantera_izq",
#         "rueda_delantera_der", 
#         "rueda_trasera_izq",
#         "rueda_trasera_der"
#     ]
    
#     for i, rueda in enumerate(ruedas):
#         if i < 4 and rueda != ruedas_renombradas[i]:
#             try:
#                 cmds.rename(rueda, ruedas_renombradas[i])
#             except:
#                 pass

#     # Validaciones finales
#     if not cmds.objExists("chasis_carro"):
#         cmds.confirmDialog(title="Error", message="❌ No se pudo configurar chasis_carro.", button=["OK"])
#         return

#     # CREAR SISTEMA DE RIG
#     try:
#         # Crear joints de la columna (1–5)
#         pos_face2 = get_face_center("chasis_carro", 2)
#         pos_face0 = get_face_center("chasis_carro", 0)

#         columna = []
#         for i in range(5):
#             j = cmds.joint(name=f"joint_{i+1}")
#             columna.append(j)
#         cmds.select(clear=True)

#         for i, jnt in enumerate(columna):
#             t = i / 4.0
#             pos = [
#                 pos_face2[0] + (pos_face0[0] - pos_face2[0]) * t,
#                 pos_face2[1] + (pos_face0[1] - pos_face2[1]) * t,
#                 pos_face2[2] + (pos_face0[2] - pos_face2[2]) * t,
#             ]
#             align_joint_to_position(jnt, pos)

#         # Crear locators (3 zonas)
#         loc_maletero = cmds.spaceLocator(name="loc_maletero")[0]
#         loc_cabina = cmds.spaceLocator(name="loc_cabina")[0]
#         loc_capo = cmds.spaceLocator(name="loc_capo")[0]

#         cmds.xform(loc_maletero, ws=True, t=cmds.xform(columna[1], q=True, ws=True, t=True))
#         cmds.xform(loc_cabina, ws=True, t=cmds.xform(columna[2], q=True, ws=True, t=True))
#         cmds.xform(loc_capo, ws=True, t=cmds.xform(columna[4], q=True, ws=True, t=True))

#         # Vincular joints con locators
#         cmds.parentConstraint(loc_maletero, columna[0], mo=True)
#         cmds.parentConstraint(loc_maletero, columna[1], mo=True)
#         cmds.parentConstraint(loc_cabina, columna[2], mo=True)
#         cmds.parentConstraint(loc_capo, columna[3], mo=True)
#         cmds.parentConstraint(loc_capo, columna[4], mo=True)

#         # Crear controles principales
#         ctrl_mal, grp_mal = create_control("ctrl_maletero", cmds.xform(loc_maletero, q=True, ws=True, t=True), 1.5, 17)
#         ctrl_cab, grp_cab = create_control("ctrl_cabina", cmds.xform(loc_cabina, q=True, ws=True, t=True), 1.8, 6)
#         ctrl_cap, grp_cap = create_control("ctrl_capo", cmds.xform(loc_capo, q=True, ws=True, t=True), 1.5, 14)

#         cmds.parentConstraint(ctrl_mal, loc_maletero, mo=True)
#         cmds.parentConstraint(ctrl_cab, loc_cabina, mo=True)
#         cmds.parentConstraint(ctrl_cap, loc_capo, mo=True)

#         # Ruedas (6–9)
#         for i, nombre in enumerate(ruedas_renombradas, start=6):
#             if not cmds.objExists(nombre):
#                 continue
#             pos = align_to_object_center(nombre)
#             j = cmds.joint(name=f"joint_{i}")
#             cmds.xform(j, ws=True, t=pos)
#             if "delantera" in nombre:
#                 cmds.parent(j, columna[4])
#             else:
#                 cmds.parent(j, columna[1])

#             ctrl, grp = create_control(f"ctrl_{nombre}", pos, radius=1.2, color_index=13)
#             cmds.parentConstraint(ctrl, j, mo=True)

#         cmds.select(clear=True)

#         # Control global
#         global_ctrl, global_grp = create_control("ctrl_global", pos_face2, radius=5, color_index=22)
#         cmds.parent(grp_mal, grp_cab, grp_cap, global_ctrl)

#         for nombre in ruedas_renombradas:
#             if cmds.objExists(f"ctrl_{nombre}_GRP"):
#                 cmds.parent(f"ctrl_{nombre}_GRP", global_ctrl)

#         rig_grp = cmds.group(global_grp, name="RIG_CARRO_GRP")

#         # Confirmación
#         cmds.confirmDialog(
#             title="Rig del Carro",
#             message="✅ Rig del carro creado correctamente.\n\n- 3 controles de columna\n- 4 controles de ruedas\n- 1 control global\n\n⚠️ Se renombraron objetos para consistencia",
#             button=["OK"]
#         )
        
#     except Exception as e:
#         cmds.confirmDialog(title="Error", message=f"❌ Error al crear rig: {str(e)}", button=["OK"])


import maya.cmds as cmds
from carro_rig_utils import get_face_center, align_joint_to_position, align_to_object_center, create_control, buscar_objetos_escena

def limpiar_rig_existente():
    """Limpia todos los elementos del rig anterior."""
    elementos_rig = [
        "RIG_CARRO_GRP", "ctrl_global", "ctrl_global_GRP",
        "ctrl_maletero", "ctrl_maletero_GRP", "ctrl_cabina", "ctrl_cabina_GRP",
        "ctrl_capo", "ctrl_capo_GRP", "loc_maletero", "loc_cabina", "loc_capo"
    ]
    
    # Agregar joints y controles de ruedas
    for i in range(1, 10):
        elementos_rig.append(f"joint_{i}")
    
    ruedas_tipos = ["delantera_izq", "delantera_der", "trasera_izq", "trasera_der"]
    for rueda in ruedas_tipos:
        elementos_rig.extend([f"ctrl_rueda_{rueda}", f"ctrl_rueda_{rueda}_GRP"])
    
    # Buscar controles de ruedas con nombres específicos
    ruedas_nombres = [
        "rueda_delantera_izq", "rueda_delantera_der", 
        "rueda_trasera_izq", "rueda_trasera_der"
    ]
    for rueda in ruedas_nombres:
        elementos_rig.extend([f"ctrl_{rueda}", f"ctrl_{rueda}_GRP"])
    
    elementos_eliminados = []
    for elem in elementos_rig:
        if cmds.objExists(elem):
            try:
                cmds.delete(elem)
                elementos_eliminados.append(elem)
            except:
                pass
    
    return len(elementos_eliminados)

def ajustar_rig_existente():
    """Ajusta el rig existente a la geometría actual del carro."""
    if not cmds.objExists("RIG_CARRO_GRP"):
        cmds.confirmDialog(title="Error", message="❌ No hay rig existente para ajustar.", button=["OK"])
        return False
    
    chasis, ruedas = buscar_objetos_escena()
    
    if not chasis:
        cmds.confirmDialog(title="Error", message="❌ No se encontró chasis en la escena.", button=["OK"])
        return False
    
    try:
        # Actualizar posición de joints de columna
        pos_face2 = get_face_center(chasis, 2)
        pos_face0 = get_face_center(chasis, 0)
        
        for i in range(1, 6):
            jnt = f"joint_{i}"
            if cmds.objExists(jnt):
                t = (i-1) / 4.0
                pos = [
                    pos_face2[0] + (pos_face0[0] - pos_face2[0]) * t,
                    pos_face2[1] + (pos_face0[1] - pos_face2[1]) * t,
                    pos_face2[2] + (pos_face0[2] - pos_face2[2]) * t,
                ]
                align_joint_to_position(jnt, pos)
        
        # Actualizar locators
        if cmds.objExists("loc_maletero"):
            cmds.xform("loc_maletero", ws=True, t=cmds.xform("joint_2", q=True, ws=True, t=True))
        if cmds.objExists("loc_cabina"):
            cmds.xform("loc_cabina", ws=True, t=cmds.xform("joint_3", q=True, ws=True, t=True))
        if cmds.objExists("loc_capo"):
            cmds.xform("loc_capo", ws=True, t=cmds.xform("joint_5", q=True, ws=True, t=True))
        
        # Actualizar controles principales
        controles_principales = {
            "ctrl_maletero": "loc_maletero",
            "ctrl_cabina": "loc_cabina", 
            "ctrl_capo": "loc_capo"
        }
        
        for ctrl, loc in controles_principales.items():
            if cmds.objExists(ctrl) and cmds.objExists(loc):
                pos = cmds.xform(loc, q=True, ws=True, t=True)
                cmds.xform(f"{ctrl}_GRP", ws=True, t=pos)
        
        # Actualizar ruedas
        for i, nombre_rueda in enumerate(ruedas, start=6):
            if i <= 9 and cmds.objExists(f"joint_{i}"):
                # Buscar objeto de rueda real
                rueda_obj = None
                for obj in cmds.ls(transforms=True):
                    if "rueda" in obj.lower() or "llanta" in obj.lower() or "wheel" in obj.lower():
                        rueda_obj = obj
                        break
                
                if rueda_obj:
                    pos = align_to_object_center(rueda_obj)
                    cmds.xform(f"joint_{i}", ws=True, t=pos)
                    
                    # Actualizar control de rueda
                    ctrl_name = f"ctrl_{nombre_rueda}"
                    if cmds.objExists(ctrl_name):
                        cmds.xform(f"{ctrl_name}_GRP", ws=True, t=pos)
        
        # Actualizar control global
        if cmds.objExists("ctrl_global"):
            cmds.xform("ctrl_global_GRP", ws=True, t=pos_face2)
        
        cmds.confirmDialog(
            title="Ajuste Completado", 
            message="✅ Rig ajustado correctamente al carro actual.", 
            button=["OK"]
        )
        return True
        
    except Exception as e:
        cmds.confirmDialog(title="Error", message=f"❌ Error al ajustar rig: {str(e)}", button=["OK"])
        return False

def crear_rig_carro(*_):
    """Crea o regenera el rig completo del carro."""
    # Limpiar rig existente primero
    elementos_eliminados = limpiar_rig_existente()
    
    # Buscar objetos automáticamente
    chasis, ruedas = buscar_objetos_escena()
    
    if not chasis:
        cmds.confirmDialog(
            title="Error",
            message="❌ No se encontró chasis en la escena.\n\nNombres sugeridos:\n- chasis_carro\n- chasis\n- car_body",
            button=["OK"]
        )
        return

    # Renombrar objetos encontrados para consistencia
    chasis_renombrado = "chasis_carro"
    if chasis != chasis_renombrado:
        try:
            cmds.rename(chasis, chasis_renombrado)
        except:
            pass
    
    ruedas_renombradas = [
        "rueda_delantera_izq",
        "rueda_delantera_der", 
        "rueda_trasera_izq",
        "rueda_trasera_der"
    ]
    
    for i, rueda in enumerate(ruedas):
        if i < 4 and rueda != ruedas_renombradas[i]:
            try:
                cmds.rename(rueda, ruedas_renombradas[i])
            except:
                pass

    # Validaciones finales
    if not cmds.objExists("chasis_carro"):
        cmds.confirmDialog(title="Error", message="❌ No se pudo configurar chasis_carro.", button=["OK"])
        return

    # CREAR SISTEMA DE RIG
    try:
        # Crear joints de la columna (1–5)
        pos_face2 = get_face_center("chasis_carro", 2)
        pos_face0 = get_face_center("chasis_carro", 0)

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
        for i, nombre in enumerate(ruedas_renombradas, start=6):
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

        for nombre in ruedas_renombradas:
            if cmds.objExists(f"ctrl_{nombre}_GRP"):
                cmds.parent(f"ctrl_{nombre}_GRP", global_ctrl)

        rig_grp = cmds.group(global_grp, name="RIG_CARRO_GRP")

        # Confirmación
        cmds.confirmDialog(
            title="Rig del Carro",
            message="✅ Rig del carro creado correctamente.\n\n- 3 controles de columna\n- 4 controles de ruedas\n- 1 control global\n\n⚠️ Se renombraron objetos para consistencia",
            button=["OK"]
        )
        
    except Exception as e:
        cmds.confirmDialog(title="Error", message=f"❌ Error al crear rig: {str(e)}", button=["OK"])