import maya.cmds as cmds
import maya.mel as mel
import traceback
import maya.api.OpenMaya as om
import math

# =========================================================
# (1) CREAR CADENA IK Y CURVA BASE
# =========================================================
def use_existing_joints(separation=0.5, lateral_push_factor=0.2):
    """
    Usa los joints existentes, crea duplicado IK, orienta y genera la curva base.
    Aplica SIEMPRE la técnica de los dos vértices más cercanos optimizada.
    """

    # 1️⃣ VALIDACIÓN Y PREPARACIÓN INICIAL
    
    existing_joints = cmds.ls("joint*", type="joint")
    if not existing_joints:
        cmds.warning("⚠️ No hay joints en la escena.")
        return None

    # Ordenar y renombrar cadena base
    existing_joints.sort(key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
    joints = [cmds.rename(j, f"joint_{i:03d}") for i, j in enumerate(existing_joints, start=1)]

    # =========================================================
    # 2️⃣ DUPLICADO Y CONFIGURACIÓN DE CADENA IK
    # =========================================================
    # Duplicar cadena completa
    ik_chain = cmds.duplicate(joints[0], renameChildren=True, returnRootsOnly=True)
    ik_joints = cmds.listRelatives(ik_chain[0], allDescendents=True, type="joint") or []
    ik_joints.append(ik_chain[0])
    
    # Renombrar joints IK
    ik_joints.sort(key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
    for i, joint in enumerate(ik_joints, start=1):
        cmds.rename(joint, f"joint_IK_{i:03d}")
    
    ik_joints = sorted(cmds.ls("joint_IK_*", type="joint"), 
                      key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))

    # Orientar cadena IK (operación por lotes)
    if len(ik_joints) > 1:
        cmds.select(ik_joints[:-1], replace=True)
        cmds.joint(edit=True, orientJoint="xyz", secondaryAxisOrient="zup", 
                  children=True, zeroScaleOrient=True)
    
    # Reset orient del último joint
    last_joint = ik_joints[-1]
    for axis in "XYZ":
        cmds.setAttr(f"{last_joint}.jointOrient{axis}", 0)

    # =========================================================
    # 3️⃣ CREACIÓN Y CONFIGURACIÓN DE CURVA CON SPANS DINÁMICOS
    # =========================================================
    # Obtener todas las posiciones de una vez
    ik_positions = [cmds.xform(j, query=True, worldSpace=True, translation=True) 
                   for j in ik_joints]

    # Manejar curva existente
    curve_name = "dynamic_cv_001"
    if cmds.objExists(curve_name):
        cmds.delete(curve_name)

    # Crear curva
    curve = cmds.curve(point=ik_positions, degree=3, name=curve_name)

    # Calcular spans óptimos según cantidad de joints
    optimal_spans = max(8, (len(ik_joints) - 1) * 2)

    # Rebuild curva con spans dinámicos
    cmds.rebuildCurve(
        curve,
        constructionHistory=False,
        replaceOriginal=True,
        rebuildType=0,
        endKnots=1,
        keepRange=0,
        keepControlPoints=False,
        keepEndPoints=True,
        keepTangents=False,
        spans=optimal_spans,
        degree=3,
        tolerance=0.01
    )

    # =========================================================
    # 4️⃣ PRE-CÁLCULO DE DATOS PARA OPTIMIZACIÓN
    # =========================================================
    spans = cmds.getAttr(f"{curve}.spans")
    degree = cmds.getAttr(f"{curve}.degree")
    cv_count = spans + degree
    
    # Pre-calcular todas las posiciones
    joint_positions = [om.MVector(*pos) for pos in ik_positions]
    joint_count = len(joint_positions)
    main_joint_x = joint_positions[0].x
    main_joint_z = joint_positions[0].z

    # Pre-calcular todas las posiciones de CVs y sus alturas Y
    cv_positions = [om.MVector(*cmds.pointPosition(f"{curve}.cv[{i}]", world=True)) 
                   for i in range(cv_count)]
    cv_heights = [cmds.pointPosition(f"{curve}.cv[{i}]", world=True)[1] 
                 for i in range(cv_count)]

    # =========================================================
    # 5️⃣ APLICACIÓN OPTIMIZADA DE TÉCNICA DE DOS VÉRTICES
    # =========================================================
    y_offset = separation * 0.5

    for j_idx in range(1, joint_count - 1):
        j_pos = joint_positions[j_idx]
        parent_pos = joint_positions[j_idx - 1]

        # Calcular desplazamiento lateral respecto al principal
        delta_x = abs(j_pos.x - main_joint_x)
        delta_z = abs(j_pos.z - main_joint_z)
        has_offset = (delta_x > 0.05 or delta_z > 0.05)

        # Calcular vector de empuje si hay offset
        push_vector = om.MVector(0, 0, 0)
        if has_offset:
            offset_direction = (j_pos - parent_pos).normalize()
            push_vector = om.MVector(offset_direction.x, 0, offset_direction.z).normalize() * lateral_push_factor

        # Encontrar los 2 CVs más cercanos (optimizado)
        distances = []
        for i, cv_pos in enumerate(cv_positions):
            distance = (cv_pos - j_pos).length()
            distances.append((distance, i))
        
        distances.sort()
        nearest_indices = [idx for _, idx in distances[:2]]
        
        # Ordenar por altura Y (descendente)
        nearest_indices.sort(key=lambda idx: cv_heights[idx], reverse=True)

        # Aplicar transformaciones a CVs
        y_values = [j_pos.y + y_offset, j_pos.y - y_offset]

        for n, cv_index in enumerate(nearest_indices):
            new_position = om.MVector(cv_positions[cv_index])  # Copiar posición actual
            new_position.x = j_pos.x + push_vector.x
            new_position.z = j_pos.z + push_vector.z
            new_position.y = y_values[n]
            
            cmds.xform(f"{curve}.cv[{cv_index}]", worldSpace=True, 
                      translation=(new_position.x, new_position.y, new_position.z))
            
            # Actualizar posición en cache
            cv_positions[cv_index] = new_position
            cv_heights[cv_index] = new_position.y

    # =========================================================
    # 6️⃣ AJUSTE FINAL DE EXTREMOS
    # =========================================================
    # Primer CV
    first_pos = joint_positions[0]
    cmds.xform(f"{curve}.cv[0]", worldSpace=True, 
              translation=(first_pos.x, first_pos.y, first_pos.z))
    
    # Último CV
    last_pos = joint_positions[-1]
    cmds.xform(f"{curve}.cv[{cv_count - 1}]", worldSpace=True, 
              translation=(last_pos.x, last_pos.y, last_pos.z))

    # =========================================================
    # 7️⃣ MENSAJE FINAL
    # =========================================================
    cmds.inViewMessage(
        amg=f'<span style="color:#7FFF7F;">✅ Curva ajustada con {optimal_spans} spans dinámicos y técnica precisa de dos vértices</span>',
        position='topCenter', fade=True, fadeStayTime=800, fadeOutTime=150
    )

    print(f"✅ Curva ajustada: técnica de dos vértices aplicada con empuje fijo ({lateral_push_factor}).")
    return joints, ik_joints, curve


# =========================================================
# (2) HACER CURVA DINÁMICA CON ESTRUCTURA CORRECTA
# =========================================================

def make_curve_dynamic(*_):
    """Automatiza 'Make Selected Curves Dynamic' con Output: NURBS Curves,
    buscando 'dynamic_cv_001' y renombrando la curva generada a 'dynamic_cv_002'."""
    try:
        # 1️⃣ Buscar y seleccionar solo la curva base dynamic_cv_001
        if not cmds.objExists("dynamic_cv_001"):
            cmds.warning("⚠️ No se encontró 'dynamic_cv_001' en la escena.")
            return None

        cmds.select("dynamic_cv_001", r=True)
        print("🔍 Curva seleccionada: dynamic_cv_001")

        # 2️⃣ Guardar los hijos actuales del grupo de salida (si existe)
        out_group = "hairSystem1OutputCurves"
        if cmds.objExists(out_group):
            pre_children = set(cmds.listRelatives(out_group, children=True) or [])
        else:
            pre_children = set()

        # 3️⃣ Ejecutar el comando MEL interno (idéntico al menú FX)
        mel.eval('makeCurvesDynamic 2 { "1", "0", "1", "1", "0"};')

        # 4️⃣ Comprobar si el grupo de salida existe después de la ejecución
        if not cmds.objExists(out_group):
            cmds.warning("⚠️ El grupo 'hairSystem1OutputCurves' no fue creado por makeCurvesDynamic.")
            return None

        post_children = cmds.listRelatives(out_group, children=True) or []
        new_curves = [c for c in post_children if c not in pre_children]

        if not new_curves:
            cmds.warning("⚠️ No se detectó nueva curva dinámica en hairSystem1OutputCurves.")
            return None

        # 5️⃣ Renombrar la nueva curva a dynamic_cv_002 (reemplazando si existe)
        dyn_curve = new_curves[0]
        target_name = "dynamic_cv_002"

        if cmds.objExists(target_name):
            cmds.delete(target_name)

        renamed = cmds.rename(dyn_curve, target_name)

        # 6️⃣ Confirmación visual
        cmds.inViewMessage(
            amg=f'<span style="color:#7FFF7F;">✅ Curva dinámica creada y renombrada a {renamed}</span>',
            pos='topCenter', fade=True, fst=800, ft=150
        )
        print(f"✅ Curva dinámica renombrada correctamente: {renamed}")

        return renamed

    except Exception:
        traceback.print_exc()
        cmds.warning("❌ Error al intentar hacer la curva dinámica.")

# =========================================================
# (3) CREAR IK SPLINE ENTRE JOINTS IK Y CURVA DINÁMICA
# =========================================================

def create_ik_spline_handle(*_):
    """Crea un IK Spline Handle entre la cadena IK y la curva dinámica,
    y alinea el último joint IK con su versión FK."""
    try:
        # --- Buscar joints IK y curva dinámica ---
        ik_joints = cmds.ls("joint_IK_*", type="joint") or []
        if len(ik_joints) < 2:
            cmds.warning("⚠️ No se encontraron suficientes joints IK (mínimo 2).")
            return

        if not cmds.objExists("dynamic_cv_002"):
            cmds.warning("⚠️ No se encontró la curva dinámica 'dynamic_cv_002'.")
            return

        # --- Ordenar joints por número ---
        ik_joints.sort(key=lambda x: int(''.join(c for c in x if c.isdigit()) or 0))
        start_joint = ik_joints[0]
        end_joint = ik_joints[-1]

        # --- Seleccionar joints y curva ---
        cmds.select(clear=True)
        cmds.select(start_joint)
        cmds.select(end_joint, add=True)
        cmds.select("dynamic_cv_002", add=True)
        print(f"🔗 Creando IK Spline entre: {start_joint} → {end_joint} con dynamic_cv_002")

        # --- Crear IK Spline Handle (sin crear curva automática) ---
        ik_handle, effector = cmds.ikHandle(
            sol="ikSplineSolver",
            ccv=False,
            curve="dynamic_cv_002",
            name="IK_Spine_Handle"
        )

        print(f"✅ IK Handle creado: {ik_handle}")

        # --- ACTIVAR TWIST CONTROL para orientación estable ---
        cmds.setAttr(f"{ik_handle}.dTwistControlEnable", 1)
        cmds.setAttr(f"{ik_handle}.dWorldUpType", 4)
        cmds.setAttr(f"{ik_handle}.dForwardAxis", 0)   # X-forward (ajusta si tu rig usa Z)
        cmds.setAttr(f"{ik_handle}.dWorldUpAxis", 2)   # Y-up (ajusta según tu setup)

        # --- Alinear último joint IK con su equivalente FK ---
        fk_joints = cmds.ls("joint_*", type="joint") or []
        fk_joints = [j for j in fk_joints if not j.startswith("joint_IK_")]
        fk_joints.sort(key=lambda x: int(''.join(c for c in x if c.isdigit()) or 0))

        if fk_joints and len(fk_joints) >= len(ik_joints):
            fk_end_joint = fk_joints[len(ik_joints) - 1]
            ref_pos = cmds.xform(fk_end_joint, q=True, ws=True, t=True)
            ref_rot = cmds.xform(fk_end_joint, q=True, ws=True, ro=True)

            cmds.xform(end_joint, ws=True, t=ref_pos)
            cmds.xform(end_joint, ws=True, ro=ref_rot)

            print(f"🧭 {end_joint} alineado con {fk_end_joint}")
        else:
            cmds.warning("⚠️ No se encontró el joint base FK correspondiente para alinear el final.")

        # --- Mensaje visual en viewport ---
        cmds.inViewMessage(
            amg=f'<span style="color:#7FFF7F;">✅ IK Spline Handle creado y alineado correctamente</span>',
            pos='topCenter', fade=True, fst=800, ft=150
        )

        print("✅ Proceso completado con alineación final correcta.")
        return ik_handle

    except Exception:
        traceback.print_exc()
        cmds.warning("❌ Error al crear o alinear el IK Spline Handle.")


# =========================================================
# (4) CONFIGURAR NUCLEUS Y FOLLICLE 
# =========================================================

def configure_nucleus_and_follicle(*_):
    """Configura nucleus1 y follicleShape1:
    - Establece la gravedad a 98
    - Cambia el Point Lock del follicle a 'Base'."""
    try:
        # --- Configurar gravedad ---
        if cmds.objExists("nucleus1"):
            cmds.setAttr("nucleus1.gravity", 98)
            print("🌍 Gravedad establecida a 98 en nucleus1.")
        else:
            cmds.warning("⚠️ No se encontró 'nucleus1' en la escena.")

        # --- Configurar Point Lock en el follicle ---
        if cmds.objExists("follicleShape1"):
            cmds.setAttr("follicleShape1.pointLock", 1)
            print("🔒 Point Lock del follicleShape1 configurado a 'Base' (1).")
        else:
            cmds.warning("⚠️ No se encontró 'follicleShape1' en la escena.")

        # --- Mensaje visual ---
        cmds.inViewMessage(
            amg='<span style="color:#7FFF7F;">✅ nucleus y follicle configurados correctamente</span>',
            pos='topCenter', fade=True, fst=800, ft=150
        )

    except Exception:
        traceback.print_exc()
        cmds.warning("❌ Error al configurar nucleus o follicle.")

# =========================================================
# (5) CREAR CONTROL DINÁMICO + ROOT
# =========================================================
def create_dynamic_control(*_):
    """Crea el control dinámico, grupo root y emparenta todo con la jerarquía correcta."""

    try:
        # 1️⃣ Control
        ctrl = cmds.circle(name="dynamic_ctrl_001", normal=(0, 1, 0), radius=1, sections=8, degree=3)[0]
        print(f"🎯 Control creado: {ctrl}")

        if cmds.objExists("joint_IK_001"):
            pos = cmds.xform("joint_IK_001", q=True, ws=True, t=True)
            cmds.xform(ctrl, ws=True, t=pos)
            print(f"📍 Control movido a la posición de joint_IK_001: {pos}")

        cmds.select(f"{ctrl}.cv[0:7]", r=True)
        cmds.scale(1.1, 1.1, 1.1, r=True)
        cmds.rotate(30, 0, 0, os=True, r=True)
        cmds.select(clear=True)

        # 2️⃣ Emparentar hairSystem
        if cmds.objExists("hairSystem1Follicles"):
            cmds.parent("hairSystem1Follicles", ctrl)
            print("🔗 'hairSystem1Follicles' emparentado a 'dynamic_ctrl_001'.")
        else:
            cmds.warning("⚠️ No se encontró 'hairSystem1Follicles'.")

        # 3️⃣ Crear root
        root_grp = cmds.group(em=True, name="dynamic_Root_ctrl_001")
        print(f"🧩 Grupo raíz creado: {root_grp}")

        # 4️⃣ Parent control bajo root
        cmds.parent(ctrl, root_grp)
        print("📂 'dynamic_ctrl_001' parentado bajo 'dynamic_Root_ctrl_001'.")

        # 5️⃣ Reset transforms
        for attr in ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"]:
            cmds.setAttr(f"{root_grp}.{attr}", 0)
        print("🎛️ Transforms del root reseteados a 0.")

        # ✅ No más parent -w
        cmds.inViewMessage(
            amg='<span style="color:#7FFF7F;">✅ Dynamic Root & Control creados correctamente</span>',
            pos='topCenter', fade=True, fst=800, ft=150
        )
        print("✅ Proceso completado con jerarquía correcta.")
        return ctrl, root_grp

    except Exception:
        traceback.print_exc()
        cmds.warning("❌ Error al crear el control dinámico con root.")


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


# =========================================================
# (8) CREAR TOROIDE, PLANO DRIVER, LOCATOR, CONTROL Y CONSTRAINTS
# =========================================================
def create_torus_system():
    """
    PASO 8 - Posicionar toroide tangente a dynamic_cv_002 en CVs cercanos a joint_IK_002.
    """
    print("=== PASO 8: Creando toroide tangente a dynamic_cv_002 (CVs cercanos a joint_IK_002) ===")
    try:

        # ---------------------------
        # Parámetros ajustables
        # ---------------------------
        SEPARATION_OFFSET = 0.15
        TORUS_RADIUS = 1.0
        TORUS_SECTION = 0.4
        TORUS_ROT_ADDITIONAL_X = 0
        CV_PREFER = [2, 3]
        CURVE_NAME = "dynamic_cv_002"
        JOINT_REF = "joint_IK_002"

        # ---------------------------
        # Limpieza previa
        # ---------------------------
        for obj in ["polyTorus1", "driverPlane_target_001", "dynamic_target_002",
                    "dynamic_ctrl_002", "dynamic_Root_ctrl_002"]:
            if cmds.objExists(obj):
                cmds.delete(obj)

        # ---------------------------
        # Validar curva
        # ---------------------------
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

        # ---------------------------
        # Determinar parámetro en la curva donde colocar el toroide
        # ---------------------------
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

        # ---------------------------
        # Obtener tangente y estimar normal lateral para separación
        # ---------------------------
        tangent_vec = crv_fn.tangent(param, om.MSpace.kWorld)
        tangent = om.MVector(tangent_vec).normalize()

        world_up = om.MVector(0, 1, 0)
        if abs(tangent * world_up) > 0.99:
            world_up = om.MVector(1, 0, 0)

        axis_x = (world_up ^ tangent).normalize()
        axis_y = (tangent ^ axis_x).normalize()

        # ---------------------------
        # Crear toroide y posicionar
        # ---------------------------
        torus = cmds.polyTorus(r=TORUS_RADIUS, sr=TORUS_SECTION, sx=24, sy=12, ax=(0, 1, 0),
                               cuv=1, ch=1, name="polyTorus1")[0]
        cmds.setAttr("polyTorus1.subdivisionsHeight", 8)
        cmds.setAttr("polyTorus1.subdivisionsAxis", 8)
        cmds.displaySmoothness(torus, divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3)

        # Mover pivote a la base del toroide
        cmds.move(0, -0.45, 0, f"{torus}.scalePivot", f"{torus}.rotatePivot", r=True)
        cmds.move(0, 0.46, 0, torus, r=True)
        cmds.setAttr(f"{torus}.translateY", 0.5)
        cmds.makeIdentity(torus, apply=True, t=True, r=True, s=True, n=False)

        # Construir matriz de transformación
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

        # Posicionar y rotar toroide
        cmds.xform(torus, ws=True, t=(point_on_curve.x, point_on_curve.y, point_on_curve.z))
        cmds.xform(torus, ws=True, rotation=rot_deg)
        
        if TORUS_ROT_ADDITIONAL_X:
            cmds.rotate(TORUS_ROT_ADDITIONAL_X, 0, 0, torus, os=True, r=True)

        # Separar para evitar interpenetración
        world_offset = (axis_x.normalize() * SEPARATION_OFFSET)
        current_pos = om.MVector(point_on_curve.x, point_on_curve.y, point_on_curve.z)
        final_pos = current_pos + world_offset
        cmds.xform(torus, ws=True, t=(final_pos.x, final_pos.y, final_pos.z))
        cmds.makeIdentity(torus, apply=True, t=True, r=True, s=True, n=False)

        print("🌀 Toroide creado y orientado según tangente de dynamic_cv_002.")

        # ---------------------------
        # Crear plano driver - SOLO CAMBIAR ROTACIÓN
        # ---------------------------
        plane = cmds.polyPlane(w=1, h=1, sx=1, sy=1, ax=(0, 1, 0), cuv=2, ch=1)[0]
        plane = cmds.rename(plane, "driverPlane_target_001")
        
        # 🔥 MANTENER POSICIÓN ORIGINAL PERO COPIAR SOLO ROTACIÓN DEL TOROIDE
        plane_pos = [
            (final_pos.x + point_on_curve.x) / 2,  # Posición media entre toroide y curva
            (final_pos.y + point_on_curve.y) / 2,
            (final_pos.z + point_on_curve.z) / 2
        ]
        
        # Aplicar posición media y rotación del toroide
        cmds.xform(plane, ws=True, translation=plane_pos)
        cmds.xform(plane, ws=True, rotation=rot_deg)  # 🔥 SOLO ROTACIÓN
        
        print("📐 Plano driver creado con misma rotación que toroide")

        # Skin bind a joint_001 y copiar pesos
        if cmds.objExists("joint_001"):
            skin_plane = cmds.skinCluster("joint_001", plane, toSelectedBones=True)[0]
            print(f"🦴 Skin Cluster aplicado al plano: {skin_plane}")
            if cmds.objExists("polyTail"):
                try:
                    src_skin = cmds.ls(cmds.listHistory("polyTail"), type="skinCluster")[0]
                    cmds.copySkinWeights(sourceSkin=src_skin, destinationSkin=skin_plane,
                                         noMirror=True, surfaceAssociation="closestPoint",
                                         influenceAssociation="closestJoint")
                    print("📊 Pesos copiados desde polyTail → plane")
                except Exception as e:
                    print(f"⚠ Error copiando pesos: {e}")
        else:
            cmds.warning("⚠ joint_001 no existe: omitiendo bind skin del plano driver.")

        # ---------------------------
        # Locator y pointOnPolyConstraint
        # ---------------------------
        locator = cmds.spaceLocator(name="dynamic_target_002")[0]
        cmds.matchTransform(locator, plane)
        con = cmds.pointOnPolyConstraint(plane, locator, mo=False)[0]
        
        # 🔥 CONFIGURAR LOS 3 ATRIBUTOS DRIVER PLANE TARGET A 0.5
        constraint_attrs = cmds.listAttr(con, userDefined=True) or []
        driver_attrs = [attr for attr in constraint_attrs if "driverPlane" in attr]
        
        for attr in driver_attrs:
            try:
                cmds.setAttr(f"{con}.{attr}", 0.5)
                print(f"⚙️ {attr} = 0.5")
            except:
                pass
        print("🎯 Locator 'dynamic_target_002' creado y pointOnPolyConstraint configurado.")

        # ---------------------------
        # CURVA DE CONTROL
        # ---------------------------
        ctrl = cmds.circle(name="dynamic_ctrl_002", nr=(0, 1, 0), r=1, d=3, s=8)[0]
        
        # Emparentar al locator primero
        cmds.parent(ctrl, locator)
        
        # Transformaciones a 0 y escala a 1.5
        for attr in ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"]:
            cmds.setAttr(f"{ctrl}.{attr}", 0)
        
        cmds.setAttr(f"{ctrl}.scaleX", 1.5)
        cmds.setAttr(f"{ctrl}.scaleY", 1.5)
        cmds.setAttr(f"{ctrl}.scaleZ", 1.5)
        
        print("⭕ Curva de control creada con transformaciones a 0 y escala 1.5")

        # ---------------------------
        # CREAR ROOT DEL CONTROL
        # ---------------------------
        root_grp = cmds.group(empty=True, name="dynamic_Root_ctrl_002")
        
        # Reorganizar jerarquía
        cmds.parent(ctrl, world=True)
        cmds.parent(ctrl, root_grp)
        
        # Resetear transforms del root
        for attr in ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"]:
            cmds.setAttr(f"{root_grp}.{attr}", 0)
        
        # Parentear root al locator
        cmds.parent(root_grp, locator)
        
        print("🧩 Jerarquía final: locator → root → control")

        # ---------------------------
        # CONSTRAINTS
        # ---------------------------
        cmds.parentConstraint(ctrl, torus, mo=True)
        cmds.scaleConstraint(ctrl, torus, mo=True)

        cmds.inViewMessage(amg='<span style="color:#7FFF7F;">✅ Sistema toroide completado</span>',
                           pos='topCenter', fade=True, fst=800, ft=150)
        print("✅ Paso 8 completado correctamente.")
        print(f"  Toroide: {torus}")
        print(f"  Plano: {plane} (misma rotación que toroide)")
        print(f"  Locator: {locator}")
        print(f"  Control: {ctrl}")
        print(f"  Root: {root_grp}")

        cmds.select(clear=True)
        return torus, plane, locator, ctrl, root_grp

    except Exception:
        traceback.print_exc()
        cmds.warning("⚠ Error en create_torus_system()")
        return None


# =========================================================
# (9) FUNCIÓN PARA EJECUTAR TODOS LOS PASOS AUTOMÁTICAMENTE
# =========================================================

def execute_all_steps_Tail():
    """Ejecuta todos los pasos del rig de cola automáticamente."""
    try:
        print("🚀 INICIANDO EJECUCIÓN COMPLETA DEL RIG DE COLA...")
        
        # Paso 1: Crear Curva Base
        print("📝 Paso 1: Creando curva base...")
        result1 = use_existing_joints()
        if result1:
            update_step_status(1, "step1_btn")
        
        # Paso 2: Hacer Curva Dinámica
        print("🌀 Paso 2: Haciendo curva dinámica...")
        result2 = make_curve_dynamic()
        if result2:
            update_step_status(2, "step2_btn")
        
        # Paso 3: Crear IK Spline Handle
        print("🔗 Paso 3: Creando IK Spline Handle...")
        result3 = create_ik_spline_handle()
        if result3:
            update_step_status(3, "step3_btn")
        
        # Paso 4: Configurar Nucleus y Follicle
        print("⚙️ Paso 4: Configurando nucleus y follicle...")
        result4 = configure_nucleus_and_follicle()
        if result4:
            update_step_status(4, "step4_btn")
        
        # Paso 5: Crear Control + Root
        print("🎯 Paso 5: Creando control y root...")
        result5 = create_dynamic_control()
        if result5:
            update_step_status(5, "step5_btn")
        
        # Paso 6: Crear PolyTail + Skin
        print("🧱 Paso 6: Creando polyTail y skin...")
        result6 = create_poly_tail()
        if result6:
            update_step_status(6, "step6_btn")
        
        # Paso 7: Crear Cuerpo + Cabeza + Collider
        print("👤 Paso 7: Creando cuerpo y cabeza...")
        result7 = create_body_and_head()
        if result7:
            update_step_status(7, "step7_btn")
        
        # Paso 8: Crear Toroide + Sistema
        print("🌀 Paso 8: Creando sistema toroide...")
        result8 = create_torus_system()
        if result8:
            update_step_status(8, "step8_btn")
        
        # Mensaje final
        cmds.inViewMessage(
            amg='<span style="color:#7FFF7F;">✅ Rig de cola completado automáticamente</span>',
            pos='topCenter', fade=True, fst=1500, ft=200
        )
        print("🎉 ¡RIG DE COLA COMPLETADO EXITOSAMENTE!")
        
        return True
        
    except Exception as e:
        cmds.warning(f"❌ Error en ejecución automática: {str(e)}")
        traceback.print_exc()
        return False


# =========================================================
# INTERFAZ DE USUARIO (UI) - RIG DE COLA
# =========================================================
step_status = {}

def update_step_status(step_num, button_name):
    """Marca un paso como completado (botón verde + check visual)."""
    step_status[step_num] = True
    if cmds.control(button_name, exists=True):
        cmds.button(button_name, e=True, bgc=(0.2, 0.6, 0.2), label=f"✓ Paso {step_num} completado")

def execute_step(step_num, func, button_name):
    """Ejecuta el paso y actualiza el botón según el resultado."""
    try:
        func()
        update_step_status(step_num, button_name)
    except Exception as e:
        cmds.warning(f"⚠ Error ejecutando paso {step_num}: {e}")
        traceback.print_exc()

def reset_all_steps():
    """Reinicia todos los botones y el estado visual."""
    for step in UI_STEPS:
        btn = step["btn_name"]
        if cmds.control(btn, exists=True):
            cmds.button(btn, e=True, bgc=(0.32, 0.32, 0.32), label=step["label"])
    step_status.clear()
    print("🔁 Progreso reiniciado.")


UI_STEPS = [
    {"num": 1, "btn_name": "step1_btn", "label": "1. Crear Curva Base (8 spans)", "func": use_existing_joints},
    {"num": 2, "btn_name": "step2_btn", "label": "2. Hacer Curva Dinámica (nHair)", "func": make_curve_dynamic},
    {"num": 3, "btn_name": "step3_btn", "label": "3. Crear IK Spline Handle", "func": create_ik_spline_handle},
    {"num": 4, "btn_name": "step4_btn", "label": "4. Configurar Nucleus y Follicle", "func": configure_nucleus_and_follicle},
    {"num": 5, "btn_name": "step5_btn", "label": "5. Crear Control + Root", "func": create_dynamic_control},
    {"num": 6, "btn_name": "step6_btn", "label": "6. Crear PolyTail + Skin", "func": create_poly_tail},
    {"num": 7, "btn_name": "step7_btn", "label": "7. Crear Cuerpo + Cabeza + Collider", "func": create_body_and_head},
    {"num": 8, "btn_name": "step8_btn", "label": "8. Crear Toroide + Plano + Locator + Control", "func": create_torus_system},
    {"num": 9, "btn_name": "step9_btn", "label": "9. Rig Completo", "func": execute_all_steps_Tail},
]


def open_ui():
    """Abre la interfaz de rig de cola (estilo rig_Columna_02.py)."""
    try:
        if cmds.window("tailRigUI", exists=True):
            cmds.deleteUI("tailRigUI")

        win = cmds.window("tailRigUI", title="Rig de Cola - Builder Modular", w=380, h=360)
        cmds.columnLayout(adjustableColumn=True, rowSpacing=6, columnOffset=["both", 12])

        # Encabezado
        cmds.text(label="RIG DE COLA - SISTEMA MODULAR", align="center", font="boldLabelFont", h=25)
        cmds.separator(h=12, style="in")

        # Crear los botones según los pasos definidos
        for step in UI_STEPS:
            num, btn, label, func = step["num"], step["btn_name"], step["label"], step["func"]
            if callable(func):
                cmds.button(
                    btn, label=label, h=34,
                    c=(lambda _x, s=num, b=btn, f=func: execute_step(s, f, b)),
                    bgc=[0.32, 0.32, 0.32]
                )
            else:
                cmds.button(
                    btn, label=f"{label} (no definida)", h=34,
                    enable=False, bgc=[0.25, 0.25, 0.25]
                )

        # Separador y botón reiniciar
        cmds.separator(h=18, style="in")
        cmds.button(label="↻ Reiniciar", h=30, c=lambda _x: reset_all_steps(),
                    bgc=[0.35, 0.35, 0.38])

        cmds.showWindow(win)
        print("🟢 Interfaz de rig de cola lista y operativa.")

    except Exception:
        traceback.print_exc()
        cmds.warning("⚠ Error al crear la interfaz de rig de cola.")


# open_ui()  # ← COMENTA O ELIMINA ESTA LÍNEA

# En su lugar:
if __name__ == "__main__":
    open_ui()
