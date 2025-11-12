# import maya.cmds as cmds
# import maya.mel as mel
# import traceback
# import maya.api.OpenMaya as om
# import math

# # =========================================================
# # (6) CREAR POLYTAIL, SKIN BIND Y CONSTRAINTS  
# # =========================================================
# def create_poly_tail(*_):
#     """Crea un cilindro extruido a lo largo de la curva dinámica, lo skinea y aplica constraints entre joints."""
#     try:
#         # ===================================================
#         # 1️⃣ CREAR CILINDRO BASE
#         # ===================================================
#         cyl, cyl_constr = cmds.polyCylinder(
#             r=1, h=2, sx=8, sy=1, sz=1,
#             ax=(0, 1, 0), rcp=0, cuv=3, ch=1,
#             name="temp_cylinder"
#         )
#         print(f"🧱 Cilindro creado: {cyl}")

#         # Mover pivote al vértice superior central (aprox)
#         cmds.move(0, 1, 0, f"{cyl}.scalePivot", f"{cyl}.rotatePivot", r=True)
#         print("🎯 Pivote movido al vértice superior.")

#         # ---------------------------------------------------
#         # Posicionar el cilindro para que el pivote quede en el origen
#         # Mover -1 en Y para que el pivote (que está en la parte superior) quede en el origen
#         # ---------------------------------------------------
#         cmds.move(0, -1, 0, cyl, r=True)
#         print("📍 Cilindro movido -1 en Y para que el pivote esté en el origen.")

#         # Freeze transformaciones para normalizar el pivote (0,0,0)
#         cmds.makeIdentity(cyl, apply=True, t=True, r=True, s=True, n=False)
#         print("🧊 Transformaciones freezeadas (pivote fijo en el origen).")

#         # ===================================================
#         # 2️⃣ SNAP AL PRIMER JOINT Y ORIENTAR HACIA CURVA
#         # ===================================================
#         if cmds.objExists("joint_IK_001"):
#             pos = cmds.xform("joint_IK_001", q=True, ws=True, t=True)
#             cmds.xform(cyl, ws=True, t=pos)
#             print("📍 Cilindro snappeado al primer joint.")
#         else:
#             cmds.warning("⚠️ No se encontró 'joint_IK_001' para hacer el snap.")

#         # Orientar hacia la curva (ajuste aproximado)
#         cmds.rotate(-145, 0, 0, cyl, os=True, r=True)

#         # ===================================================
#         # 3️⃣ EXTRUIR A LO LARGO DE LA CURVA
#         # ===================================================
#         if not cmds.objExists("dynamic_cv_001"):
#             cmds.warning("⚠️ No se encontró 'dynamic_cv_001'. No se puede extruir.")
#             return

#         # Seleccionar las caras superiores (mitad superior)
#         faces_to_extrude = [f"{cyl}.f[16:23]"]
#         cmds.select(faces_to_extrude, r=True)

#         extrude = cmds.polyExtrudeFacet(
#             faces_to_extrude,
#             ch=True,
#             keepFacesTogether=True,
#             divisions=15,
#             twist=0,
#             taper=0.1,
#             thickness=0,
#             smoothingAngle=30,
#             inputCurve="dynamic_cv_001"
#         )[0]

#         print(f"✨ Extrusión creada: {extrude}")

#         # ===================================================
#         # 4️⃣ FREEZE + DELETE HISTORY + RENAME
#         # ===================================================
#         cmds.makeIdentity(cyl, apply=True, t=True, r=True, s=True, n=False)
#         cmds.delete(cyl, ch=True)
#         poly_tail = cmds.rename(cyl, "polyTail")
#         print("🎨 Cilindro renombrado a 'polyTail' y limpiado.")

#         # ===================================================
#         # 5️⃣ SKIN BIND A TODA LA CADENA FK (CORRECCIÓN CLAVE)
#         # ===================================================
#         # Obtener TODOS los joints FK, no solo el primero
#         fk_joints = [j for j in cmds.ls("joint_*", type="joint") or [] if not j.startswith("joint_IK_")]
#         fk_joints.sort(key=lambda x: int(''.join(c for c in x if c.isdigit()) or 0))
        
#         if fk_joints:
#             # Seleccionar todos los joints FK y el polyTail
#             cmds.select(fk_joints, r=True)
#             cmds.select(poly_tail, add=True)
            
#             # Crear skinCluster con TODA la cadena
#             skin = cmds.skinCluster(
#                 fk_joints, 
#                 poly_tail, 
#                 maximumInfluences=3,
#                 skinMethod=0,
#                 normalizeWeights=1
#             )[0]
#             print(f"🦴 SkinCluster creado con {len(fk_joints)} joints: {skin}")
            
#             # Opcional: Normalizar pesos para mejor deformación
#             cmds.skinPercent(skin, poly_tail, normalize=True)
#             print("📊 Pesos de skin normalizados automáticamente.")
#         else:
#             cmds.warning("⚠️ No se encontraron joints FK para el Skin Bind.")

#         # ===================================================
#         # 6️⃣ PARENT CONSTRAINT ENTRE JOINTS Y JOINTS IK
#         # ===================================================
#         ik_joints = cmds.ls("joint_IK_*", type="joint") or []
#         ik_joints.sort(key=lambda x: int(''.join(c for c in x if c.isdigit()) or 0))

#         if len(fk_joints) == len(ik_joints):
#             constraints_created = 0
#             for ik, fk in zip(ik_joints, fk_joints):
#                 try:
#                     # Crear constraint sin necesidad de selección previa
#                     constraint = cmds.parentConstraint(ik, fk, mo=True)
#                     print(f"🔗 ParentConstraint aplicado: {ik} → {fk}")
#                     constraints_created += 1
#                 except Exception as e:
#                     cmds.warning(f"⚠️ No se pudo crear constraint entre {ik} y {fk}: {str(e)}")
            
#             print(f"✅ {constraints_created}/{len(ik_joints)} constraints creados exitosamente.")
#         else:
#             cmds.warning(f"⚠️ El número de joints FK ({len(fk_joints)}) e IK ({len(ik_joints)}) no coincide. No se aplicaron constraints.")

#         # ===================================================
#         # 7️⃣ MENSAJE VISUAL
#         # ===================================================
#         cmds.inViewMessage(
#             amg='<span style="color:#7FFF7F;">✅ polyTail creado, skineado a TODA la cadena FK y con constraints aplicados</span>',
#             pos='topCenter', fade=True, fst=800, ft=150
#         )
#         print("✅ Proceso completado correctamente: polyTail + skin + constraints.")

#         return poly_tail

#     except Exception:
#         traceback.print_exc()
#         cmds.warning("❌ Error al crear el polyTail.")


# # =========================================================
# # (7) CREAR CUERPO + CABEZA + COLLIDER
# # =========================================================
# def create_body_and_head(*_):
#     """
#     Automatiza la creación del cuerpo y cabeza a partir de la curva dinámica:
#     - Enfocado en alinear perfectamente en Z
#     """
#     try:
#         # ===================================================
#         # 1️⃣ VALIDAR CURVA DINÁMICA
#         # ===================================================
#         if not cmds.objExists("dynamic_cv_002"):
#             cmds.warning("⚠️ No se encontró 'dynamic_cv_002'.")
#             return None

#         # Buscar joint padre para referencia de escala
#         parent_joint = None
#         if cmds.objExists("joint_IK_001"):
#             parent_joint = "joint_IK_001"
#         elif cmds.objExists("joint_001"):
#             parent_joint = "joint_001"

#         parent_scale = 1.0
#         if parent_joint:
#             parent_pos = cmds.xform(parent_joint, query=True, worldSpace=True, translation=True)
#             child_joints = cmds.listRelatives(parent_joint, children=True, type="joint") or []
#             if child_joints:
#                 child_pos = cmds.xform(child_joints[0], query=True, worldSpace=True, translation=True)
#                 parent_scale = math.sqrt(
#                     (child_pos[0] - parent_pos[0])**2 +
#                     (child_pos[1] - parent_pos[1])**2 +
#                     (child_pos[2] - parent_pos[2])**2
#                 )
#             print(f"🎯 Referencia: {parent_joint}, escala: {parent_scale}")

#         # ===================================================
#         # 2️⃣ CREAR CUERPO CON REVOLVE
#         # ===================================================
#         cmds.select("dynamic_cv_002", replace=True)
        
#         # Mover pivote de la curva
#         pivot_offset = parent_scale * 0.5
#         cmds.move(0, 0, pivot_offset, 
#                  "dynamic_cv_002.scalePivot", 
#                  "dynamic_cv_002.rotatePivot", 
#                  relative=True)
        
#         pivot_pos = cmds.xform("dynamic_cv_002", query=True, worldSpace=True, rotatePivot=True)

#         # Aplicar revolve
#         revolve_result = cmds.revolve(
#             "dynamic_cv_002",
#             constructionHistory=True,
#             polygon=1,
#             pivot=(pivot_pos[0], pivot_pos[1], pivot_pos[2]),
#             range=0,
#             startSweep=0,
#             endSweep=360,
#             degree=3,
#             sections=8,
#             axis=(0, 1, 0),
#             tolerance=0.01
#         )
        
#         revolved_surface = revolve_result[0]
        
#         # Ajustar pivote del cuerpo sin mover geometría
#         body_pos = cmds.xform(revolved_surface, query=True, worldSpace=True, translation=True)
#         cmds.CenterPivot()
#         pivot_y_offset = -body_pos[1]
#         cmds.move(0, pivot_y_offset, 0, 
#                  f"{revolved_surface}.scalePivot", 
#                  f"{revolved_surface}.rotatePivot", 
#                  relative=True)
        
#         cmds.polyNormal(revolved_surface, normalMode=0, userNormalMode=0, constructionHistory=True)

#         # ===================================================
#         # 3️⃣ CREAR CABEZA Y ALINEAR PERFECTAMENTE EN Z
#         # ===================================================
#         cmds.select(clear=True)
        
#         # Crear esfera en el origen
#         sphere = cmds.polySphere(
#             radius=parent_scale * 0.3,
#             subdivisionsAxis=10,
#             subdivisionsHeight=10,
#             axis=(0, 1, 0),
#             createUVs=2,
#             constructionHistory=True
#         )[0]

#         # 🔥 OBTENER LA POSICIÓN Z DEL PIVOTE DEL CUERPO
#         body_pivot_pos = cmds.xform(revolved_surface, query=True, worldSpace=True, rotatePivot=True)
#         body_z = body_pivot_pos[2]  # Usar la Z del pivote del cuerpo
        
#         # Obtener bounding box del cuerpo para posición Y
#         body_bb = cmds.exactWorldBoundingBox(revolved_surface)
#         head_y_pos = body_bb[4] + (parent_scale * 0.5)
        
#         # 🔥 SOLO CORREGIR LA Z - mantener X e Y como estaban
#         head_current_pos = cmds.xform(sphere, query=True, worldSpace=True, translation=True)
#         head_final_pos = [head_current_pos[0], head_y_pos, body_z]  # Solo cambiar la Z
        
#         # Mover la cabeza a la posición corregida
#         cmds.xform(sphere, worldSpace=True, translation=head_final_pos)
        
#         # Aplicar escala
#         head_scale = parent_scale * 0.7
#         cmds.scale(head_scale, head_scale, head_scale, sphere, absolute=True)
        
#         print(f"📍 Cabeza alineada en Z: pivote cuerpo Z={body_z}, cabeza Z={head_final_pos[2]}")

#         # ===================================================
#         # 4️⃣ RENOMBRAR Y PREPARAR
#         # ===================================================
#         poly_body = cmds.rename(revolved_surface, "polyBody")
#         poly_head = cmds.rename(sphere, "polyHead")

#         # Aplicar smooth display
#         for obj in [poly_body, poly_head, "polyTail"]:
#             if cmds.objExists(obj):
#                 cmds.displaySmoothness(
#                     obj,
#                     divisionsU=3,
#                     divisionsV=3,
#                     pointsWire=16,
#                     pointsShaded=4,
#                     polygonObject=3
#                 )

#         # ===================================================
#         # 5️⃣ MOVER AMBOS JUNTOS EN Z Y FREEZE
#         # ===================================================
#         z_offset = parent_scale * 0.2
        
#         cmds.select([poly_body, poly_head], replace=True)
#         cmds.move(0, 0, z_offset, relative=True)
        
#         # Freeze transforms
#         cmds.makeIdentity(apply=True, translate=True, rotate=True, scale=True, normal=False)
#         cmds.delete(constructionHistory=True)

#         # ===================================================
#         # 6️⃣ CREAR PASSIVE COLLIDER
#         # ===================================================
#         cmds.select(poly_body, replace=True)
#         collider = cmds.duplicate(returnRootsOnly=True)[0]
#         poly_collider = cmds.rename(collider, "polyBodyPasiveCollider")
        
#         cmds.select(poly_collider, replace=True)
#         mel.eval('makeCollideNCloth;')
        
#         n_rigid_shapes = cmds.ls(type="nRigid") or []
#         if n_rigid_shapes:
#             thickness = parent_scale * 0.05
#             cmds.setAttr(f"{n_rigid_shapes[0]}.thickness", thickness)
#             cmds.setAttr(f"{n_rigid_shapes[0]}.solverDisplay", 0)

#         cmds.inViewMessage(
#             amg='<span style="color:#7FFF7F;">✅ Cuerpo y cabeza creados y alineados</span>',
#             pos='topCenter', fade=True, fst=800, ft=150
#         )

#         return poly_body, poly_head, poly_collider

#     except Exception:
#         traceback.print_exc()
#         cmds.warning("❌ Error al crear cuerpo y cabeza.")


# # =========================================================
# # (8) CREAR TOROIDE, PLANO DRIVER, LOCATOR, CONTROL Y CONSTRAINTS
# # =========================================================
# def create_torus_system():
#     """
#     PASO 8 - Posicionar toroide tangente a dynamic_cv_002 en CVs cercanos a joint_IK_002.
#     """
#     print("=== PASO 8: Creando toroide tangente a dynamic_cv_002 (CVs cercanos a joint_IK_002) ===")
#     try:

#         # ---------------------------
#         # Parámetros ajustables
#         # ---------------------------
#         SEPARATION_OFFSET = 0.15
#         TORUS_RADIUS = 1.0
#         TORUS_SECTION = 0.4
#         TORUS_ROT_ADDITIONAL_X = 0
#         CV_PREFER = [2, 3]
#         CURVE_NAME = "dynamic_cv_002"
#         JOINT_REF = "joint_IK_002"

#         # ---------------------------
#         # Limpieza previa
#         # ---------------------------
#         for obj in ["polyTorus1", "driverPlane_target_001", "dynamic_target_002",
#                     "dynamic_ctrl_002", "dynamic_Root_ctrl_002"]:
#             if cmds.objExists(obj):
#                 cmds.delete(obj)

#         # ---------------------------
#         # Validar curva
#         # ---------------------------
#         if not cmds.objExists(CURVE_NAME):
#             cmds.warning(f"⚠️ No se encontró la curva '{CURVE_NAME}'. Ejecuta make_curve_dynamic antes.")
#             return None

#         shapes = cmds.listRelatives(CURVE_NAME, shapes=True) or []
#         if not shapes:
#             cmds.warning(f"⚠️ '{CURVE_NAME}' no tiene shape.")
#             return None
#         crv_shape = shapes[0]

#         sel = om.MSelectionList()
#         sel.add(crv_shape)
#         dag = sel.getDagPath(0)
#         crv_fn = om.MFnNurbsCurve(dag)

#         # ---------------------------
#         # Determinar parámetro en la curva donde colocar el toroide
#         # ---------------------------
#         param = None
#         point_on_curve = None

#         if cmds.objExists(JOINT_REF):
#             jpos = cmds.xform(JOINT_REF, q=True, ws=True, t=True)
#             jvec = om.MPoint(jpos[0], jpos[1], jpos[2])
#             length = crv_fn.length()
#             samples = 200
#             best_param = None
#             best_dist = float('inf')
#             for i in range(samples + 1):
#                 u = crv_fn.findParamFromLength(length * (i / float(samples)))
#                 p = crv_fn.getPointAtParam(u, om.MSpace.kWorld)
#                 d = (p - jvec).length()
#                 if d < best_dist:
#                     best_dist = d
#                     best_param = u
#             param = best_param
#             point_on_curve = crv_fn.getPointAtParam(param, om.MSpace.kWorld)
#         else:
#             spans = crv_fn.numSpans
#             degree = crv_fn.degree
#             cv_count = spans + degree
#             chosen_cv = None
#             for cv_idx in CV_PREFER:
#                 if 0 <= cv_idx < cv_count:
#                     chosen_cv = cv_idx
#                     break
#             if chosen_cv is not None:
#                 cv_pos = cmds.pointPosition(f"{CURVE_NAME}.cv[{chosen_cv}]", world=True)
#                 p_cv = om.MPoint(cv_pos[0], cv_pos[1], cv_pos[2])
#                 length = crv_fn.length()
#                 samples = 200
#                 best_param = None
#                 best_dist = float('inf')
#                 for i in range(samples + 1):
#                     u = crv_fn.findParamFromLength(length * (i / float(samples)))
#                     p = crv_fn.getPointAtParam(u, om.MSpace.kWorld)
#                     d = (p - p_cv).length()
#                     if d < best_dist:
#                         best_dist = d
#                         best_param = u
#                 param = best_param
#                 point_on_curve = crv_fn.getPointAtParam(param, om.MSpace.kWorld)
#             else:
#                 param = crv_fn.findParamFromLength(crv_fn.length() * 0.5)
#                 point_on_curve = crv_fn.getPointAtParam(param, om.MSpace.kWorld)

#         # ---------------------------
#         # Obtener tangente y estimar normal lateral para separación
#         # ---------------------------
#         tangent_vec = crv_fn.tangent(param, om.MSpace.kWorld)
#         tangent = om.MVector(tangent_vec).normalize()

#         world_up = om.MVector(0, 1, 0)
#         if abs(tangent * world_up) > 0.99:
#             world_up = om.MVector(1, 0, 0)

#         axis_x = (world_up ^ tangent).normalize()
#         axis_y = (tangent ^ axis_x).normalize()

#         # ---------------------------
#         # Crear toroide y posicionar
#         # ---------------------------
#         torus = cmds.polyTorus(r=TORUS_RADIUS, sr=TORUS_SECTION, sx=24, sy=12, ax=(0, 1, 0),
#                                cuv=1, ch=1, name="polyTorus1")[0]
#         cmds.setAttr("polyTorus1.subdivisionsHeight", 8)
#         cmds.setAttr("polyTorus1.subdivisionsAxis", 8)
#         cmds.displaySmoothness(torus, divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3)

#         # Mover pivote a la base del toroide
#         cmds.move(0, -0.45, 0, f"{torus}.scalePivot", f"{torus}.rotatePivot", r=True)
#         cmds.move(0, 0.46, 0, torus, r=True)
#         cmds.setAttr(f"{torus}.translateY", 0.5)
#         cmds.makeIdentity(torus, apply=True, t=True, r=True, s=True, n=False)

#         # Construir matriz de transformación
#         mat_list = [
#             axis_x.x, axis_x.y, axis_x.z, 0.0,
#             axis_y.x, axis_y.y, axis_y.z, 0.0,
#             tangent.x, tangent.y, tangent.z, 0.0,
#             point_on_curve.x, point_on_curve.y, point_on_curve.z, 1.0
#         ]
#         m = om.MMatrix(mat_list)
#         mtx = om.MTransformationMatrix(m)
#         rot = mtx.rotation()
#         if hasattr(rot, "asEulerRotation"):
#             rot = rot.asEulerRotation()
#         rot_deg = (math.degrees(rot.x), math.degrees(rot.y), math.degrees(rot.z))

#         # Posicionar y rotar toroide
#         cmds.xform(torus, ws=True, t=(point_on_curve.x, point_on_curve.y, point_on_curve.z))
#         cmds.xform(torus, ws=True, rotation=rot_deg)
        
#         if TORUS_ROT_ADDITIONAL_X:
#             cmds.rotate(TORUS_ROT_ADDITIONAL_X, 0, 0, torus, os=True, r=True)

#         # Separar para evitar interpenetración
#         world_offset = (axis_x.normalize() * SEPARATION_OFFSET)
#         current_pos = om.MVector(point_on_curve.x, point_on_curve.y, point_on_curve.z)
#         final_pos = current_pos + world_offset
#         cmds.xform(torus, ws=True, t=(final_pos.x, final_pos.y, final_pos.z))
#         cmds.makeIdentity(torus, apply=True, t=True, r=True, s=True, n=False)

#         print("🌀 Toroide creado y orientado según tangente de dynamic_cv_002.")

#         # ---------------------------
#         # Crear plano driver - SOLO CAMBIAR ROTACIÓN
#         # ---------------------------
#         plane = cmds.polyPlane(w=1, h=1, sx=1, sy=1, ax=(0, 1, 0), cuv=2, ch=1)[0]
#         plane = cmds.rename(plane, "driverPlane_target_001")
        
#         # 🔥 MANTENER POSICIÓN ORIGINAL PERO COPIAR SOLO ROTACIÓN DEL TOROIDE
#         plane_pos = [
#             (final_pos.x + point_on_curve.x) / 2,  # Posición media entre toroide y curva
#             (final_pos.y + point_on_curve.y) / 2,
#             (final_pos.z + point_on_curve.z) / 2
#         ]
        
#         # Aplicar posición media y rotación del toroide
#         cmds.xform(plane, ws=True, translation=plane_pos)
#         cmds.xform(plane, ws=True, rotation=rot_deg)  # 🔥 SOLO ROTACIÓN
        
#         print("📐 Plano driver creado con misma rotación que toroide")

#         # Skin bind a joint_001 y copiar pesos
#         if cmds.objExists("joint_001"):
#             skin_plane = cmds.skinCluster("joint_001", plane, toSelectedBones=True)[0]
#             print(f"🦴 Skin Cluster aplicado al plano: {skin_plane}")
#             if cmds.objExists("polyTail"):
#                 try:
#                     src_skin = cmds.ls(cmds.listHistory("polyTail"), type="skinCluster")[0]
#                     cmds.copySkinWeights(sourceSkin=src_skin, destinationSkin=skin_plane,
#                                          noMirror=True, surfaceAssociation="closestPoint",
#                                          influenceAssociation="closestJoint")
#                     print("📊 Pesos copiados desde polyTail → plane")
#                 except Exception as e:
#                     print(f"⚠ Error copiando pesos: {e}")
#         else:
#             cmds.warning("⚠ joint_001 no existe: omitiendo bind skin del plano driver.")

#         # ---------------------------
#         # Locator y pointOnPolyConstraint
#         # ---------------------------
#         locator = cmds.spaceLocator(name="dynamic_target_002")[0]
#         cmds.matchTransform(locator, plane)
#         con = cmds.pointOnPolyConstraint(plane, locator, mo=False)[0]
        
#         # 🔥 CONFIGURAR LOS 3 ATRIBUTOS DRIVER PLANE TARGET A 0.5
#         constraint_attrs = cmds.listAttr(con, userDefined=True) or []
#         driver_attrs = [attr for attr in constraint_attrs if "driverPlane" in attr]
        
#         for attr in driver_attrs:
#             try:
#                 cmds.setAttr(f"{con}.{attr}", 0.5)
#                 print(f"⚙️ {attr} = 0.5")
#             except:
#                 pass
#         print("🎯 Locator 'dynamic_target_002' creado y pointOnPolyConstraint configurado.")

#         # ---------------------------
#         # CURVA DE CONTROL
#         # ---------------------------
#         ctrl = cmds.circle(name="dynamic_ctrl_002", nr=(0, 1, 0), r=1, d=3, s=8)[0]
        
#         # Emparentar al locator primero
#         cmds.parent(ctrl, locator)
        
#         # Transformaciones a 0 y escala a 1.5
#         for attr in ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"]:
#             cmds.setAttr(f"{ctrl}.{attr}", 0)
        
#         cmds.setAttr(f"{ctrl}.scaleX", 1.5)
#         cmds.setAttr(f"{ctrl}.scaleY", 1.5)
#         cmds.setAttr(f"{ctrl}.scaleZ", 1.5)
        
#         print("⭕ Curva de control creada con transformaciones a 0 y escala 1.5")

#         # ---------------------------
#         # CREAR ROOT DEL CONTROL
#         # ---------------------------
#         root_grp = cmds.group(empty=True, name="dynamic_Root_ctrl_002")
        
#         # Reorganizar jerarquía
#         cmds.parent(ctrl, world=True)
#         cmds.parent(ctrl, root_grp)
        
#         # Resetear transforms del root
#         for attr in ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"]:
#             cmds.setAttr(f"{root_grp}.{attr}", 0)
        
#         # Parentear root al locator
#         cmds.parent(root_grp, locator)
        
#         print("🧩 Jerarquía final: locator → root → control")

#         # ---------------------------
#         # CONSTRAINTS
#         # ---------------------------
#         cmds.parentConstraint(ctrl, torus, mo=True)
#         cmds.scaleConstraint(ctrl, torus, mo=True)

#         cmds.inViewMessage(amg='<span style="color:#7FFF7F;">✅ Sistema toroide completado</span>',
#                            pos='topCenter', fade=True, fst=800, ft=150)
#         print("✅ Paso 8 completado correctamente.")
#         print(f"  Toroide: {torus}")
#         print(f"  Plano: {plane} (misma rotación que toroide)")
#         print(f"  Locator: {locator}")
#         print(f"  Control: {ctrl}")
#         print(f"  Root: {root_grp}")

#         cmds.select(clear=True)
#         return torus, plane, locator, ctrl, root_grp

#     except Exception:
#         traceback.print_exc()
#         cmds.warning("⚠ Error en create_torus_system()")
#         return None



import maya.cmds as cmds 
import maya.mel as mel
import traceback
import maya.api.OpenMaya as om
import math

# ---------------------------------------------------------
# Fix: asegurar orientación consistente de la cadena de joints
# ---------------------------------------------------------
# def fix_tail_joint_orientation(chain_root):
#     """
#     Reorienta los joints del chain_root para que el orientation
#     sea consistente (orientJoint='xyz', secondaryAxisOrient='yup').
#     No rompe si el joint no existe. Silent-fail en errores.
#     """
#     try:
#         if not cmds.objExists(chain_root):
#             return

#         joints = cmds.listRelatives(chain_root, allDescendents=True, type='joint') or []
#         # incluir el root
#         joints.append(chain_root)
#         # invertir para procesar de raíz a extremo correctamente cuando se aplica orient
#         joints = list(reversed(joints))

#         for jnt in joints:
#             try:
#                 # limpiar transforms antes de orientar para evitar acumulados raros
#                 cmds.makeIdentity(jnt, apply=True, t=True, r=True, s=True, n=False)
#                 cmds.joint(jnt, e=True, orientJoint='xyz', secondaryAxisOrient='yup', zeroScaleOrient=True)
#             except Exception:
#                 # No queremos que un joint malforme detenga todo el proceso
#                 pass

#         cmds.select(clear=True)
#         print(f"[TailRig] Orientación corregida para el chain '{chain_root}'.")
#     except Exception:
#         # proteger por si algo falla inesperadamente
#         try:
#             traceback.print_exc()
#         except:
#             pass
#         return


def fix_tail_joint_orientation(chain_root):
    """
    Reorienta los joints del chain_root para que el orientation
    sea consistente (orientJoint='xyz', secondaryAxisOrient='yup').
    No rompe si el joint no existe. Silent-fail en errores.
    """
    try:
        if not cmds.objExists(chain_root):
            return

        joints = cmds.listRelatives(chain_root, allDescendents=True, type='joint') or []
        # incluir el root
        joints.append(chain_root)
        # invertir para procesar de raíz a extremo correctamente cuando se aplica orient
        joints = list(reversed(joints))

        for jnt in joints:
            try:
                # limpiar transforms antes de orientar para evitar acumulados raros
                cmds.makeIdentity(jnt, apply=True, t=True, r=True, s=True, n=False)
                cmds.joint(jnt, e=True, orientJoint='xyz', secondaryAxisOrient='yup', zeroScaleOrient=True)
            except Exception:
                # No queremos que un joint malforme detenga todo el proceso
                pass

        cmds.select(clear=True)
        print(f"[TailRig] Orientación corregida para el chain '{chain_root}'.")
    except Exception:
        # proteger por si algo falla inesperadamente
        try:
            traceback.print_exc()
        except:
            pass
        return

# =========================================================
# (6) CREAR POLYTAIL, SKIN BIND Y CONSTRAINTS  
# =========================================================
def create_poly_tail(*_):
    """Crea un cilindro extruido a lo largo de la curva dinámica, lo skinea y aplica constraints entre joints."""
    try:
        # ===================================================
        # 1️⃣ CREAR CILINDRO BASE
        # ===================================================
        cyl, cyl_constr = cmds.polyCylinder(
            r=1, h=2, sx=8, sy=1, sz=1,
            ax=(0, 1, 0), rcp=0, cuv=3, ch=1,
            name="temp_cylinder"
        )
        print(f"🧱 Cilindro creado: {cyl}")

        # Mover pivote al vértice superior central (aprox)
        cmds.move(0, 1, 0, f"{cyl}.scalePivot", f"{cyl}.rotatePivot", r=True)
        print("🎯 Pivote movido al vértice superior.")

        # ---------------------------------------------------
        # Posicionar el cilindro para que el pivote quede en el origen
        # Mover -1 en Y para que el pivote (que está en la parte superior) quede en el origen
        # ---------------------------------------------------
        cmds.move(0, -1, 0, cyl, r=True)
        print("📍 Cilindro movido -1 en Y para que el pivote esté en el origen.")

        # Freeze transformaciones para normalizar el pivote (0,0,0)
        cmds.makeIdentity(cyl, apply=True, t=True, r=True, s=True, n=False)
        print("🧊 Transformaciones freezeadas (pivote fijo en el origen).")

        # ===================================================
        # 2️⃣ SNAP AL PRIMER JOINT Y ORIENTAR HACIA CURVA
        # ===================================================
        if cmds.objExists("joint_IK_001"):
            pos = cmds.xform("joint_IK_001", q=True, ws=True, t=True)
            cmds.xform(cyl, ws=True, t=pos)
            print("📍 Cilindro snappeado al primer joint.")
        else:
            cmds.warning("⚠️ No se encontró 'joint_IK_001' para hacer el snap.")

        # Orientar hacia la curva (ajuste aproximado)
        cmds.rotate(-145, 0, 0, cyl, os=True, r=True)

        # ===================================================
        # 3️⃣ EXTRUIR A LO LARGO DE LA CURVA
        # ===================================================
        if not cmds.objExists("dynamic_cv_001"):
            cmds.warning("⚠️ No se encontró 'dynamic_cv_001'. No se puede extruir.")
            return

        # Seleccionar las caras superiores (mitad superior)
        faces_to_extrude = [f"{cyl}.f[16:23]"]
        cmds.select(faces_to_extrude, r=True)

        extrude = cmds.polyExtrudeFacet(
            faces_to_extrude,
            ch=True,
            keepFacesTogether=True,
            divisions=15,
            twist=0,
            taper=0.1,
            thickness=0,
            smoothingAngle=30,
            inputCurve="dynamic_cv_001"
        )[0]

        print(f"✨ Extrusión creada: {extrude}")

        # ===================================================
        # 4️⃣ FREEZE + DELETE HISTORY + RENAME
        # ===================================================
        cmds.makeIdentity(cyl, apply=True, t=True, r=True, s=True, n=False)
        cmds.delete(cyl, ch=True)
        poly_tail = cmds.rename(cyl, "polyTail")
        print("🎨 Cilindro renombrado a 'polyTail' y limpiado.")

        # ===================================================
        # 5️⃣ SKIN BIND A TODA LA CADENA FK (CORRECCIÓN CLAVE)
        # ===================================================
        # Obtener TODOS los joints FK, no solo el primero
        fk_joints = [j for j in cmds.ls("joint_*", type="joint") or [] if not j.startswith("joint_IK_")]
        fk_joints.sort(key=lambda x: int(''.join(c for c in x if c.isdigit()) or 0))
        
        if fk_joints:
            # Seleccionar todos los joints FK y el polyTail
            cmds.select(fk_joints, r=True)
            cmds.select(poly_tail, add=True)
            
            # Crear skinCluster con TODA la cadena
            skin = cmds.skinCluster(
                fk_joints, 
                poly_tail, 
                maximumInfluences=3,
                skinMethod=0,
                normalizeWeights=1
            )[0]
            print(f"🦴 SkinCluster creado con {len(fk_joints)} joints: {skin}")
            
            # Opcional: Normalizar pesos para mejor deformación
            cmds.skinPercent(skin, poly_tail, normalize=True)
            print("📊 Pesos de skin normalizados automáticamente.")
        else:
            cmds.warning("⚠️ No se encontraron joints FK para el Skin Bind.")

        # ===================================================
        # 6️⃣ PARENT CONSTRAINT ENTRE JOINTS Y JOINTS IK
        # ===================================================
        ik_joints = cmds.ls("joint_IK_*", type="joint") or []
        ik_joints.sort(key=lambda x: int(''.join(c for c in x if c.isdigit()) or 0))

        if len(fk_joints) == len(ik_joints):
            constraints_created = 0
            for ik, fk in zip(ik_joints, fk_joints):
                try:
                    # Crear constraint sin necesidad de selección previa
                    constraint = cmds.parentConstraint(ik, fk, mo=True)
                    print(f"🔗 ParentConstraint aplicado: {ik} → {fk}")
                    constraints_created += 1
                except Exception as e:
                    cmds.warning(f"⚠️ No se pudo crear constraint entre {ik} y {fk}: {str(e)}")
            
            print(f"✅ {constraints_created}/{len(ik_joints)} constraints creados exitosamente.")
        else:
            cmds.warning(f"⚠️ El número de joints FK ({len(fk_joints)}) e IK ({len(ik_joints)}) no coincide. No se aplicaron constraints.")

        # ===================================================
        # 7️⃣ MENSAJE VISUAL
        # ===================================================
        cmds.inViewMessage(
            amg='<span style="color:#7FFF7F;">✅ polyTail creado, skineado a TODA la cadena FK y con constraints aplicados</span>',
            pos='topCenter', fade=True, fst=800, ft=150
        )
        print("✅ Proceso completado correctamente: polyTail + skin + constraints.")

        return poly_tail

    except Exception:
        traceback.print_exc()
        cmds.warning("❌ Error al crear el polyTail.")


# =========================================================
# (7) CREAR CUERPO + CABEZA + COLLIDER
# =========================================================
def create_body_and_head(*_):
    """
    Automatiza la creación del cuerpo y cabeza a partir de la curva dinámica:
    - Enfocado en alinear perfectamente en Z
    """
    try:
        # ===================================================
        # 1️⃣ VALIDAR CURVA DINÁMICA
        # ===================================================
        if not cmds.objExists("dynamic_cv_002"):
            cmds.warning("⚠️ No se encontró 'dynamic_cv_002'.")
            return None

        # Buscar joint padre para referencia de escala
        parent_joint = None
        if cmds.objExists("joint_IK_001"):
            parent_joint = "joint_IK_001"
        elif cmds.objExists("joint_001"):
            parent_joint = "joint_001"

        parent_scale = 1.0
        if parent_joint:
            parent_pos = cmds.xform(parent_joint, query=True, worldSpace=True, translation=True)
            child_joints = cmds.listRelatives(parent_joint, children=True, type="joint") or []
            if child_joints:
                child_pos = cmds.xform(child_joints[0], query=True, worldSpace=True, translation=True)
                parent_scale = math.sqrt(
                    (child_pos[0] - parent_pos[0])**2 +
                    (child_pos[1] - parent_pos[1])**2 +
                    (child_pos[2] - parent_pos[2])**2
                )
            print(f"🎯 Referencia: {parent_joint}, escala: {parent_scale}")

        # ===================================================
        # 2️⃣ CREAR CUERPO CON REVOLVE
        # ===================================================
        cmds.select("dynamic_cv_002", replace=True)
        
        # Mover pivote de la curva
        pivot_offset = parent_scale * 0.5
        cmds.move(0, 0, pivot_offset, 
                 "dynamic_cv_002.scalePivot", 
                 "dynamic_cv_002.rotatePivot", 
                 relative=True)
        
        pivot_pos = cmds.xform("dynamic_cv_002", query=True, worldSpace=True, rotatePivot=True)

        # Aplicar revolve
        revolve_result = cmds.revolve(
            "dynamic_cv_002",
            constructionHistory=True,
            polygon=1,
            pivot=(pivot_pos[0], pivot_pos[1], pivot_pos[2]),
            range=0,
            startSweep=0,
            endSweep=360,
            degree=3,
            sections=8,
            axis=(0, 1, 0),
            tolerance=0.01
        )
        
        revolved_surface = revolve_result[0]
        
        # Ajustar pivote del cuerpo sin mover geometría
        body_pos = cmds.xform(revolved_surface, query=True, worldSpace=True, translation=True)
        cmds.CenterPivot()
        pivot_y_offset = -body_pos[1]
        cmds.move(0, pivot_y_offset, 0, 
                 f"{revolved_surface}.scalePivot", 
                 f"{revolved_surface}.rotatePivot", 
                 relative=True)
        
        cmds.polyNormal(revolved_surface, normalMode=0, userNormalMode=0, constructionHistory=True)

        # ===================================================
        # 3️⃣ CREAR CABEZA Y ALINEAR PERFECTAMENTE EN Z
        # ===================================================
        cmds.select(clear=True)
        
        # Crear esfera en el origen
        sphere = cmds.polySphere(
            radius=parent_scale * 0.3,
            subdivisionsAxis=10,
            subdivisionsHeight=10,
            axis=(0, 1, 0),
            createUVs=2,
            constructionHistory=True
        )[0]

        # 🔥 OBTENER LA POSICIÓN Z DEL PIVOTE DEL CUERPO
        body_pivot_pos = cmds.xform(revolved_surface, query=True, worldSpace=True, rotatePivot=True)
        body_z = body_pivot_pos[2]  # Usar la Z del pivote del cuerpo
        
        # Obtener bounding box del cuerpo para posición Y
        body_bb = cmds.exactWorldBoundingBox(revolved_surface)
        head_y_pos = body_bb[4] + (parent_scale * 0.5)
        
        # 🔥 SOLO CORREGIR LA Z - mantener X e Y como estaban
        head_current_pos = cmds.xform(sphere, query=True, worldSpace=True, translation=True)
        head_final_pos = [head_current_pos[0], head_y_pos, body_z]  # Solo cambiar la Z
        
        # Mover la cabeza a la posición corregida
        cmds.xform(sphere, worldSpace=True, translation=head_final_pos)
        
        # Aplicar escala
        head_scale = parent_scale * 0.7
        cmds.scale(head_scale, head_scale, head_scale, sphere, absolute=True)
        
        print(f"📍 Cabeza alineada en Z: pivote cuerpo Z={body_z}, cabeza Z={head_final_pos[2]}")

        # ===================================================
        # 4️⃣ RENOMBRAR Y PREPARAR
        # ===================================================
        poly_body = cmds.rename(revolved_surface, "polyBody")
        poly_head = cmds.rename(sphere, "polyHead")

        # Aplicar smooth display
        for obj in [poly_body, poly_head, "polyTail"]:
            if cmds.objExists(obj):
                cmds.displaySmoothness(
                    obj,
                    divisionsU=3,
                    divisionsV=3,
                    pointsWire=16,
                    pointsShaded=4,
                    polygonObject=3
                )

        # ===================================================
        # 5️⃣ MOVER AMBOS JUNTOS EN Z Y FREEZE
        # ===================================================
        z_offset = parent_scale * 0.2
        
        cmds.select([poly_body, poly_head], replace=True)
        cmds.move(0, 0, z_offset, relative=True)
        
        # Freeze transforms
        cmds.makeIdentity(apply=True, translate=True, rotate=True, scale=True, normal=False)
        cmds.delete(constructionHistory=True)

        # ===================================================
        # 6️⃣ CREAR PASSIVE COLLIDER
        # ===================================================
        cmds.select(poly_body, replace=True)
        collider = cmds.duplicate(returnRootsOnly=True)[0]
        poly_collider = cmds.rename(collider, "polyBodyPasiveCollider")
        
        cmds.select(poly_collider, replace=True)
        mel.eval('makeCollideNCloth;')
        
        n_rigid_shapes = cmds.ls(type="nRigid") or []
        if n_rigid_shapes:
            thickness = parent_scale * 0.05
            cmds.setAttr(f"{n_rigid_shapes[0]}.thickness", thickness)
            cmds.setAttr(f"{n_rigid_shapes[0]}.solverDisplay", 0)

        cmds.inViewMessage(
            amg='<span style="color:#7FFF7F;">✅ Cuerpo y cabeza creados y alineados</span>',
            pos='topCenter', fade=True, fst=800, ft=150
        )

        return poly_body, poly_head, poly_collider

    except Exception:
        traceback.print_exc()
        cmds.warning("❌ Error al crear cuerpo y cabeza.")


def create_torus_system():
    """
    PASO 8 - Posicionar toroide SIEMPRE en la CARA EXTERIOR de la cola (corrección robusta).
    """
    print("=== PASO 8: Creando toroide en CARA EXTERIOR de la cola (fix side selection) ===")
    try:
        # Parámetros
        SEPARATION_OFFSET = 0.35
        MIN_CLEARANCE = 0.08
        MAX_ATTEMPTS = 12
        STEP_FACTOR = 0.15
        TORUS_RADIUS = 1.0
        TORUS_SECTION = 0.4
        TORUS_ROT_ADDITIONAL_X = 0
        CV_PREFER = [2, 3]
        CURVE_NAME = "dynamic_cv_002"
        JOINT_REF = "joint_IK_002"

        # limpieza
        for obj in ["polyTorus1", "driverPlane_target_001", "dynamic_target_002",
                    "dynamic_ctrl_002", "dynamic_Root_ctrl_002"]:
            if cmds.objExists(obj):
                cmds.delete(obj)

        # validar curva
        if not cmds.objExists(CURVE_NAME):
            cmds.warning(f"⚠️ No se encontró la curva '{CURVE_NAME}'. Ejecuta make_curve_dynamic antes.")
            return None

        shapes = cmds.listRelatives(CURVE_NAME, shapes=True) or []
        if not shapes:
            cmds.warning(f"⚠️ '{CURVE_NAME}' no tiene shape.")
            return None
        crv_shape = shapes[0]

        sel = om.MSelectionList()
        sel.add(crv_shape)
        dag = sel.getDagPath(0)
        crv_fn = om.MFnNurbsCurve(dag)

        # encontrar param / point_on_curve
        param = None
        point_on_curve = None
        if cmds.objExists(JOINT_REF):
            jpos = cmds.xform(JOINT_REF, q=True, ws=True, t=True)
            jvec = om.MPoint(jpos[0], jpos[1], jpos[2])
            length = crv_fn.length()
            samples = 200
            best_param = None
            best_dist = float('inf')
            for i in range(samples + 1):
                u = crv_fn.findParamFromLength(length * (i / float(samples)))
                p = crv_fn.getPointAtParam(u, om.MSpace.kWorld)
                d = (p - jvec).length()
                if d < best_dist:
                    best_dist = d
                    best_param = u
            param = best_param
            point_on_curve = crv_fn.getPointAtParam(param, om.MSpace.kWorld)
        else:
            spans = crv_fn.numSpans
            degree = crv_fn.degree
            cv_count = spans + degree
            chosen_cv = None
            for cv_idx in CV_PREFER:
                if 0 <= cv_idx < cv_count:
                    chosen_cv = cv_idx
                    break
            if chosen_cv is not None:
                cv_pos = cmds.pointPosition(f"{CURVE_NAME}.cv[{chosen_cv}]", world=True)
                p_cv = om.MPoint(cv_pos[0], cv_pos[1], cv_pos[2])
                length = crv_fn.length()
                samples = 200
                best_param = None
                best_dist = float('inf')
                for i in range(samples + 1):
                    u = crv_fn.findParamFromLength(length * (i / float(samples)))
                    p = crv_fn.getPointAtParam(u, om.MSpace.kWorld)
                    d = (p - p_cv).length()
                    if d < best_dist:
                        best_dist = d
                        best_param = u
                param = best_param
                point_on_curve = crv_fn.getPointAtParam(param, om.MSpace.kWorld)
            else:
                param = crv_fn.findParamFromLength(crv_fn.length() * 0.5)
                point_on_curve = crv_fn.getPointAtParam(param, om.MSpace.kWorld)

        # tangente y axis_x inicial
        tangent_vec = crv_fn.tangent(param, om.MSpace.kWorld)
        tangent = om.MVector(tangent_vec).normalize()
        world_up = om.MVector(0, 1, 0)
        if abs(tangent * world_up) > 0.99:
            world_up = om.MVector(1, 0, 0)
        axis_x = (world_up ^ tangent).normalize()

        # prefijo por dirección de curva (mantener heurística, pero no reemplaza comparación final)
        ik_joints = cmds.ls("joint_IK_*", type="joint") or []
        ik_joints.sort(key=lambda x: int(''.join(c for c in x if c.isdigit()) or 0))
        if len(ik_joints) >= 3:
            j1_pos = cmds.xform(ik_joints[0], q=True, ws=True, t=True)
            j2_pos = cmds.xform(ik_joints[1], q=True, ws=True, t=True)
            j3_pos = cmds.xform(ik_joints[2], q=True, ws=True, t=True)
            v1 = om.MVector(j1_pos[0], j1_pos[1], j1_pos[2])
            v2 = om.MVector(j2_pos[0], j2_pos[1], j2_pos[2])
            v3 = om.MVector(j3_pos[0], j3_pos[1], j3_pos[2])
            dir1 = (v2 - v1).normalize()
            dir2 = (v3 - v2).normalize()
            cross_result = dir1 ^ dir2
            curve_direction = cross_result.y
            if curve_direction > 0:
                axis_x = axis_x * -1

        # AABB del body (si existe)
        body_bb = None
        if cmds.objExists("polyBody"):
            try:
                body_bb = cmds.exactWorldBoundingBox("polyBody")
            except Exception:
                body_bb = None

        def aabb_distance(point_vec, bb):
            minx, miny, minz, maxx, maxy, maxz = bb
            cx = max(minx, min(point_vec.x, maxx))
            cy = max(miny, min(point_vec.y, maxy))
            cz = max(minz, min(point_vec.z, maxz))
            clamped = om.MVector(cx, cy, cz)
            return (point_vec - clamped).length()

        # --- AQUÍ: probar ambos lados y elegir el que da MÁS separación ---
        curve_pt = om.MVector(point_on_curve.x, point_on_curve.y, point_on_curve.z)
        out_dir = axis_x.normalize()
        in_dir  = (-axis_x).normalize()

        def measure_candidate(dir_vec, off):
            cand = curve_pt + (dir_vec * off)
            if body_bb:
                return aabb_distance(cand, body_bb)
            else:
                # fallback a joint pivot
                if cmds.objExists("joint_001"):
                    jp = cmds.xform("joint_001", q=True, ws=True, t=True)
                    body_center = om.MVector(jp[0], jp[1], jp[2])
                elif cmds.objExists("joint_IK_001"):
                    jp = cmds.xform("joint_IK_001", q=True, ws=True, t=True)
                    body_center = om.MVector(jp[0], jp[1], jp[2])
                else:
                    return SEPARATION_OFFSET + 1.0
                return (cand - body_center).length()

        # medir con offset base
        dist_out = measure_candidate(out_dir, SEPARATION_OFFSET)
        dist_in  = measure_candidate(in_dir, SEPARATION_OFFSET)
        if dist_out >= dist_in:
            chosen_dir = out_dir
            chosen_side = "OUT"
        else:
            chosen_dir = in_dir
            chosen_side = "IN"

        print(f"🔍 Candidate distances -> OUT: {dist_out:.3f}, IN: {dist_in:.3f}  -> Chosen side: {chosen_side}")

        # ahora incrementar SOLO en chosen_dir hasta MIN_CLEARANCE
        chosen_offset = SEPARATION_OFFSET
        attempt = 0
        final_pos = curve_pt + (chosen_dir * chosen_offset)
        while attempt < MAX_ATTEMPTS:
            cand = curve_pt + (chosen_dir * chosen_offset)
            dist = measure_candidate(chosen_dir, chosen_offset)
            print(f"🔎 Intento {attempt+1}: offset={chosen_offset:.3f} -> clearance={dist:.3f}")
            if dist >= MIN_CLEARANCE:
                final_pos = cand
                break
            chosen_offset += max(STEP_FACTOR * SEPARATION_OFFSET, 0.02)
            attempt += 1
        else:
            final_pos = curve_pt + (chosen_dir * chosen_offset)
            print("⚠️ Max attempts alcanzado; usando offset forzado:", chosen_offset)

        # Si por alguna razón final_pos sigue demasiado cerca e intentos fallaron, invertir y probar rápido
        if body_bb:
            dist_final = aabb_distance(final_pos, body_bb)
            if dist_final < MIN_CLEARANCE:
                # invertir y probar 6 intentos rápido
                chosen_dir = (-chosen_dir).normalize()
                chosen_offset = SEPARATION_OFFSET
                attempt2 = 0
                while attempt2 < 6:
                    cand2 = curve_pt + (chosen_dir * chosen_offset)
                    dist2 = aabb_distance(cand2, body_bb)
                    print(f"🔁 Re-inv Intent {attempt2+1}: offset={chosen_offset:.3f} -> clearance={dist2:.3f}")
                    if dist2 >= MIN_CLEARANCE:
                        final_pos = cand2
                        break
                    chosen_offset += max(STEP_FACTOR * SEPARATION_OFFSET, 0.02)
                    attempt2 += 1

        # reconstruir axis_y y crear/colocar torus en final_pos
        axis_x = chosen_dir
        axis_y = (tangent ^ axis_x).normalize()

        torus = cmds.polyTorus(r=TORUS_RADIUS, sr=TORUS_SECTION, sx=24, sy=12, ax=(0, 1, 0),
                               cuv=1, ch=1, name="polyTorus1")[0]
        cmds.setAttr("polyTorus1.subdivisionsHeight", 8)
        cmds.setAttr("polyTorus1.subdivisionsAxis", 8)
        cmds.displaySmoothness(torus, divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3)

        cmds.move(0, -0.45, 0, f"{torus}.scalePivot", f"{torus}.rotatePivot", r=True)
        cmds.move(0, 0.46, 0, torus, r=True)
        cmds.setAttr(f"{torus}.translateY", 0.5)
        cmds.makeIdentity(torus, apply=True, t=True, r=True, s=True, n=False)

        mat_list = [
            axis_x.x, axis_x.y, axis_x.z, 0.0,
            axis_y.x, axis_y.y, axis_y.z, 0.0,
            tangent.x, tangent.y, tangent.z, 0.0,
            point_on_curve.x, point_on_curve.y, point_on_curve.z, 1.0
        ]
        m = om.MMatrix(mat_list)
        mtx = om.MTransformationMatrix(m)
        rot = mtx.rotation()
        if hasattr(rot, "asEulerRotation"):
            rot = rot.asEulerRotation()
        rot_deg = (math.degrees(rot.x), math.degrees(rot.y), math.degrees(rot.z))

        cmds.xform(torus, ws=True, t=(point_on_curve.x, point_on_curve.y, point_on_curve.z))
        cmds.xform(torus, ws=True, rotation=rot_deg)
        if TORUS_ROT_ADDITIONAL_X:
            cmds.rotate(TORUS_ROT_ADDITIONAL_X, 0, 0, torus, os=True, r=True)

        cmds.xform(torus, ws=True, t=(final_pos.x, final_pos.y, final_pos.z))
        cmds.makeIdentity(torus, apply=True, t=True, r=True, s=True, n=False)

        print("🌀 Toroide creado en CARA EXTERIOR de la cola (pos final aplicada)")

        # parenting al FK
        fk_joints = [j for j in cmds.ls("joint_*", type="joint") or [] if not j.startswith("joint_IK_")]
        fk_joints.sort(key=lambda x: int(''.join(c for c in x if c.isdigit()) or 0))
        target_fk_joint = None
        if len(fk_joints) >= 2:
            target_fk_joint = fk_joints[1]
        elif fk_joints:
            target_fk_joint = fk_joints[0]
        if target_fk_joint:
            cmds.parent(torus, target_fk_joint)
            print(f"🔗 Toroide parenteado al joint FK: {target_fk_joint}")

        # crear plane, locator, ctrl, root (igual)
        plane = cmds.polyPlane(w=1, h=1, sx=1, sy=1, ax=(0, 1, 0), cuv=2, ch=1)[0]
        plane = cmds.rename(plane, "driverPlane_target_001")
        plane_pos = [
            (final_pos.x + point_on_curve.x) / 2,
            (final_pos.y + point_on_curve.y) / 2,
            (final_pos.z + point_on_curve.z) / 2
        ]
        cmds.xform(plane, ws=True, translation=plane_pos)
        cmds.xform(plane, ws=True, rotation=rot_deg)

        if cmds.objExists("joint_001"):
            skin_plane = cmds.skinCluster("joint_001", plane, toSelectedBones=True)[0]
            if cmds.objExists("polyTail"):
                try:
                    src_skin = cmds.ls(cmds.listHistory("polyTail"), type="skinCluster")[0]
                    cmds.copySkinWeights(sourceSkin=src_skin, destinationSkin=skin_plane,
                                         noMirror=True, surfaceAssociation="closestPoint",
                                         influenceAssociation="closestJoint")
                except Exception:
                    pass
        else:
            cmds.warning("⚠ joint_001 no existe: omitiendo bind skin del plano driver.")

        locator = cmds.spaceLocator(name="dynamic_target_002")[0]
        cmds.matchTransform(locator, plane)
        con = cmds.pointOnPolyConstraint(plane, locator, mo=False)[0]
        constraint_attrs = cmds.listAttr(con, userDefined=True) or []
        driver_attrs = [attr for attr in constraint_attrs if "driverPlane" in attr]
        for attr in driver_attrs:
            try:
                cmds.setAttr(f"{con}.{attr}", 0.5)
            except:
                pass

        ctrl = cmds.circle(name="dynamic_ctrl_002", nr=(0, 1, 0), r=1, d=3, s=8)[0]
        cmds.parent(ctrl, locator)
        for attr in ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"]:
            cmds.setAttr(f"{ctrl}.{attr}", 0)
        cmds.setAttr(f"{ctrl}.scaleX", 1.5)
        cmds.setAttr(f"{ctrl}.scaleY", 1.5)
        cmds.setAttr(f"{ctrl}.scaleZ", 1.5)

        root_grp = cmds.group(empty=True, name="dynamic_Root_ctrl_002")
        cmds.parent(ctrl, world=True)
        cmds.parent(ctrl, root_grp)
        for attr in ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"]:
            cmds.setAttr(f"{root_grp}.{attr}", 0)
        cmds.parent(root_grp, locator)

        cmds.parentConstraint(ctrl, torus, mo=True)
        cmds.scaleConstraint(ctrl, torus, mo=True)

        cmds.inViewMessage(amg='<span style="color:#7FFF7F;">✅ Toroide en CARA EXTERIOR</span>',
                           pos='topCenter', fade=True, fst=800, ft=150)
        print("✅ Paso 8 completado - TOROIDE EN CARA EXTERIOR")

        cmds.select(clear=True)
        return torus, plane, locator, ctrl, root_grp

    except Exception:
        traceback.print_exc()
        cmds.warning("⚠ Error en create_torus_system()")
        return None
