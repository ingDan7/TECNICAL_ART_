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