import maya.cmds as cmds
import maya.mel as mel
import traceback
import maya.api.OpenMaya as om
import math
import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui


# Importación opcional de PySide para interfaz avanzada
try:
    
    

    PYSIDE_AVAILABLE = True
except ImportError:
    try:
        from PySide2 import QtWidgets, QtCore, QtGui
        from shiboken2 import wrapInstance

        PYSIDE_AVAILABLE = True
    except ImportError:
        PYSIDE_AVAILABLE = False

if PYSIDE_AVAILABLE:
    try:
        import maya.api.OpenMaya as omui
    except ImportError:
        omui = None

    def maya_main_window():
        if omui is None:
            return None
        try:
            main_window_ptr = omui.MQtUtil.mainWindow()
            if main_window_ptr:
                return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
        except:
            return None

# ============================================================================
# VARIABLES GLOBALES
# ============================================================================
_joints = []
_ik_joints = []
_dynamic_curve = None
_dynamic_curve_output = None
_ik_handle = None
_control = None
_poly_tail = None
_poly_body = None
_poly_head = None


# ============================================================================
# FUNCIONES CORE
# ============================================================================

def cleanup_previous_rig():
    """Limpiar rig dinámico anterior si existe"""
    objects_to_delete = [
        "joint_001", "joint_002", "joint_003", "joint_004", "joint_005",
        "joint_IK_001", "joint_IK_002", "joint_IK_003", "joint_IK_004", "joint_IK_005",
        "dynamic_cv_001", "dynamic_cv_002", "temp_revolve_curve",
        "dynamic_ctrl_001", "dynamic_Root_ctrl_001",
        "dynamic_toro_ctrl_001", "dynamic_toro_ctrl_001_root",
        "polyTail", "polyBody", "polyHead", "polyBodyPasiveCollider",
        "temp_cylinder",
        "polyTorus1", "driverPlane_target_001",
        "dynamic_target_002",
        "hairSystem1", "hairSystem1Follicles", "hairSystem1OutputCurves",
        "nucleus1",
        "IK_Spine_Handle"
    ]

    deleted_count = 0
    for obj in objects_to_delete:
        if cmds.objExists(obj):
            try:
                cmds.delete(obj)
                deleted_count += 1
            except:
                pass

    if deleted_count > 0:
        print(f"Limpieza completada: {deleted_count} objetos eliminados")


def step1_create_joints_and_curve():
    """PASO 1: Crea 5 joints y una curva NURBS desde cero"""
    print("=== PASO 1: Creando joints y curva base ===")

    positions = [
        (0, 8, 0),
        (0, 6, -1.5),
        (0, 4, 0),
        (0, 2, 1.5),
        (0, 0, 0)
    ]

    joints = []
    cmds.select(clear=True)

    for i, pos in enumerate(positions, start=1):
        jnt = cmds.joint(p=pos, name=f"joint_{i:03d}")
        joints.append(jnt)

    cmds.joint(joints[0], e=True, oj="xyz", sao="yup", ch=True, zso=True)

    for ax in ["X", "Y", "Z"]:
        cmds.setAttr(f"{joints[-1]}.jointOrient{ax}", 0)

    ik_chain = cmds.duplicate(joints[0], renameChildren=True, returnRootsOnly=True)
    ik_joints = cmds.listRelatives(ik_chain[0], allDescendents=True, type="joint") or []
    ik_joints.append(ik_chain[0])
    ik_joints.sort(key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))

    for i, joint in enumerate(ik_joints, start=1):
        cmds.rename(joint, f"joint_IK_{i:03d}")

    ik_joints = sorted(cmds.ls("joint_IK_*", type="joint"),
                       key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))

    ik_positions = [cmds.xform(j, q=True, ws=True, t=True) for j in ik_joints]
    curve = cmds.curve(point=ik_positions, degree=3, name="dynamic_cv_001")

    optimal_spans = max(8, (len(ik_joints) - 1) * 2)

    cmds.rebuildCurve(
        curve, constructionHistory=False, replaceOriginal=True,
        rebuildType=0, endKnots=1, keepRange=0, keepControlPoints=False,
        keepEndPoints=True, keepTangents=False, spans=optimal_spans,
        degree=3, tolerance=0.01
    )

    print(f"Joints FK: {joints}")
    print(f"Joints IK: {ik_joints}")
    print(f"Curva: {curve}")

    return joints, ik_joints, curve


def step1_use_existing_joints():
    """PASO 1: Usa joints existentes"""
    print("=== PASO 1: Usando joints existentes ===")

    existing_joints = cmds.ls("joint*", type="joint")
    if not existing_joints:
        cmds.warning("No hay joints en la escena.")
        return None, None, None

    existing_joints.sort(key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
    joints = [cmds.rename(j, f"joint_{i:03d}") for i, j in enumerate(existing_joints, start=1)]

    ik_chain = cmds.duplicate(joints[0], renameChildren=True, returnRootsOnly=True)
    ik_joints = cmds.listRelatives(ik_chain[0], allDescendents=True, type="joint") or []
    ik_joints.append(ik_chain[0])
    ik_joints.sort(key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))

    for i, joint in enumerate(ik_joints, start=1):
        cmds.rename(joint, f"joint_IK_{i:03d}")

    ik_joints = sorted(cmds.ls("joint_IK_*", type="joint"),
                       key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))

    if len(ik_joints) > 1:
        cmds.select(ik_joints[:-1], replace=True)
        cmds.joint(edit=True, orientJoint="xyz", secondaryAxisOrient="zup",
                   children=True, zeroScaleOrient=True)

    last_joint = ik_joints[-1]
    for axis in "XYZ":
        cmds.setAttr(f"{last_joint}.jointOrient{axis}", 0)

    ik_positions = [cmds.xform(j, query=True, worldSpace=True, translation=True)
                    for j in ik_joints]

    curve_name = "dynamic_cv_001"
    if cmds.objExists(curve_name):
        cmds.delete(curve_name)

    curve = cmds.curve(point=ik_positions, degree=3, name=curve_name)
    optimal_spans = max(8, (len(ik_joints) - 1) * 2)

    cmds.rebuildCurve(
        curve, constructionHistory=False, replaceOriginal=True,
        rebuildType=0, endKnots=1, keepRange=0, keepControlPoints=False,
        keepEndPoints=True, keepTangents=False, spans=optimal_spans,
        degree=3, tolerance=0.01
    )

    print(f"Joints FK: {joints}")
    print(f"Joints IK: {ik_joints}")
    print(f"Curva: {curve}")

    return joints, ik_joints, curve


def step2_make_curve_dynamic():
    """PASO 2: Hacer curva dinámica con nHair"""
    print("=== PASO 2: Haciendo curva dinámica ===")

    try:
        if not cmds.objExists("dynamic_cv_001"):
            cmds.warning("No se encontró 'dynamic_cv_001'")
            return None

        cmds.select("dynamic_cv_001", r=True)

        out_group = "hairSystem1OutputCurves"
        if cmds.objExists(out_group):
            pre_children = set(cmds.listRelatives(out_group, children=True) or [])
        else:
            pre_children = set()

        mel.eval('makeCurvesDynamic 2 { "1", "0", "1", "1", "0"};')

        if not cmds.objExists(out_group):
            cmds.warning("No se creó hairSystem1OutputCurves")
            return None

        post_children = cmds.listRelatives(out_group, children=True) or []
        new_curves = [c for c in post_children if c not in pre_children]

        if not new_curves:
            cmds.warning("No se detectó nueva curva dinámica")
            return None

        dyn_curve = new_curves[0]
        target_name = "dynamic_cv_002"

        if cmds.objExists(target_name):
            cmds.delete(target_name)

        renamed = cmds.rename(dyn_curve, target_name)
        print(f"Curva dinámica: {renamed}")
        return renamed

    except Exception:
        traceback.print_exc()
        return None


def step3_create_ik_spline():
    """PASO 3: Crear IK Spline Handle"""
    print("=== PASO 3: Creando IK Spline Handle ===")

    try:
        ik_joints = cmds.ls("joint_IK_*", type="joint") or []
        if len(ik_joints) < 2:
            cmds.warning("Faltan joints IK")
            return None

        if not cmds.objExists("dynamic_cv_002"):
            cmds.warning("Falta dynamic_cv_002")
            return None

        ik_joints.sort(key=lambda x: int(''.join(c for c in x if c.isdigit()) or 0))

        ik_handle, effector = cmds.ikHandle(
            sol="ikSplineSolver", ccv=False, curve="dynamic_cv_002",
            name="IK_Spine_Handle", startJoint=ik_joints[0],
            endEffector=ik_joints[-1]
        )

        cmds.setAttr(f"{ik_handle}.dTwistControlEnable", 1)
        cmds.setAttr(f"{ik_handle}.dWorldUpType", 4)
        cmds.setAttr(f"{ik_handle}.dForwardAxis", 0)
        cmds.setAttr(f"{ik_handle}.dWorldUpAxis", 2)

        print(f"IK Handle: {ik_handle}")
        return ik_handle

    except Exception:
        traceback.print_exc()
        return None


def step4_configure_nucleus_and_follicle():
    """PASO 4: Configurar sistema físico"""
    print("=== PASO 4: Configurando Nucleus y Follicle ===")

    try:
        if cmds.objExists("nucleus1"):
            cmds.setAttr("nucleus1.gravity", 98)
            print("Gravedad: 98")

        if cmds.objExists("follicleShape1"):
            cmds.setAttr("follicleShape1.pointLock", 1)
            print("Point Lock: Base")

        print("Sistema configurado")

    except Exception:
        traceback.print_exc()


def step5_create_dynamic_control():
    """PASO 5: Crear control principal"""
    print("=== PASO 5: Creando control dinámico ===")

    try:
        ctrl = cmds.circle(name="dynamic_ctrl_001", normal=(0, 1, 0),
                           radius=1, sections=8, degree=3)[0]

        if cmds.objExists("joint_IK_001"):
            pos = cmds.xform("joint_IK_001", q=True, ws=True, t=True)
            cmds.xform(ctrl, ws=True, t=pos)

        cmds.select(f"{ctrl}.cv[0:7]", r=True)
        cmds.scale(1.1, 1.1, 1.1, r=True)
        cmds.select(clear=True)

        if cmds.objExists("hairSystem1Follicles"):
            cmds.parent("hairSystem1Follicles", ctrl)

        root_grp = cmds.group(em=True, name="dynamic_Root_ctrl_001")
        cmds.parent(ctrl, root_grp)

        for attr in ["translateX", "translateY", "translateZ",
                     "rotateX", "rotateY", "rotateZ"]:
            cmds.setAttr(f"{root_grp}.{attr}", 0)

        print(f"Control: {ctrl}, Root: {root_grp}")
        return ctrl, root_grp

    except Exception:
        traceback.print_exc()
        return None, None


def step6_create_poly_tail():
    """PASO 6: Crear polyTail"""
    print("=== PASO 6: Creando polyTail ===")

    try:
        cyl, cyl_constr = cmds.polyCylinder(
            r=1, h=2, sx=8, sy=1, sz=1, ax=(0, 1, 0),
            rcp=0, cuv=3, ch=1, name="temp_cylinder"
        )

        cmds.move(0, 1, 0, f"{cyl}.scalePivot", f"{cyl}.rotatePivot", r=True)
        cmds.move(0, -1, 0, cyl, r=True)
        cmds.makeIdentity(cyl, apply=True, t=True, r=True, s=True, n=False)

        if cmds.objExists("joint_IK_001"):
            pos = cmds.xform("joint_IK_001", q=True, ws=True, t=True)
            cmds.xform(cyl, ws=True, t=pos)

        cmds.rotate(-145, 0, 0, cyl, os=True, r=True)

        if not cmds.objExists("dynamic_cv_001"):
            cmds.warning("Falta dynamic_cv_001")
            return None

        faces_to_extrude = [f"{cyl}.f[16:23]"]
        cmds.select(faces_to_extrude, r=True)

        extrude = cmds.polyExtrudeFacet(
            faces_to_extrude, ch=True, keepFacesTogether=True,
            divisions=15, twist=0, taper=0.1, thickness=0,
            smoothingAngle=30, inputCurve="dynamic_cv_001"
        )[0]

        cmds.makeIdentity(cyl, apply=True, t=True, r=True, s=True, n=False)
        cmds.delete(cyl, ch=True)
        poly_tail = cmds.rename(cyl, "polyTail")

        fk_joints = [j for j in cmds.ls("joint_*", type="joint") or []
                     if not j.startswith("joint_IK_")]
        fk_joints.sort(key=lambda x: int(''.join(c for c in x if c.isdigit()) or 0))

        if fk_joints:
            cmds.select(fk_joints, r=True)
            cmds.select(poly_tail, add=True)
            skin = cmds.skinCluster(
                fk_joints, poly_tail, maximumInfluences=3,
                skinMethod=0, normalizeWeights=1
            )[0]
            print(f"Skin: {skin}")

        ik_joints = cmds.ls("joint_IK_*", type="joint") or []
        ik_joints.sort(key=lambda x: int(''.join(c for c in x if c.isdigit()) or 0))

        if len(fk_joints) == len(ik_joints):
            for ik, fk in zip(ik_joints, fk_joints):
                cmds.parentConstraint(ik, fk, mo=True)

        print(f"PolyTail: {poly_tail}")
        return poly_tail

    except Exception:
        traceback.print_exc()
        return None


def step7_create_body_and_head():
    """PASO 7: Crear cuerpo y cabeza - Método corregido con pivote en Z"""
    print("=== PASO 7: Creando cuerpo y cabeza ===")

    try:
        if not cmds.objExists("dynamic_cv_002"):
            cmds.warning("Falta dynamic_cv_002")
            return None, None

        # Calcular escala para la cabeza
        parent_scale = 0.8
        if cmds.objExists("joint_IK_001"):
            parent_pos = cmds.xform("joint_IK_001", q=True, ws=True, t=True)
            child_joints = cmds.listRelatives("joint_IK_001", children=True, type="joint") or []
            if child_joints:
                child_pos = cmds.xform(child_joints[0], q=True, ws=True, t=True)
                parent_scale = math.sqrt(sum((child_pos[i] - parent_pos[i]) ** 2 for i in range(3)))

        # 1. Copiar la curva dinámica
        cmds.select("dynamic_cv_002", r=True)
        curve_copy = cmds.duplicate("dynamic_cv_002", name="temp_revolve_curve")[0]

        # 2. PRIMERO mover el pivote 4 unidades en +Z
        curve_pos = cmds.xform(curve_copy, q=True, ws=True, t=True)
        pivot_offset_z = 4.0
        new_pivot = [curve_pos[0], curve_pos[1], curve_pos[2] + pivot_offset_z]

        # Editar el pivote (rotate y scale pivot)
        cmds.xform(curve_copy, ws=True, rotatePivot=new_pivot)
        cmds.xform(curve_copy, ws=True, scalePivot=new_pivot)
        print(f"Pivote editado a: {new_pivot}")

        # 3. AHORA hacer revolve NURBS desde el nuevo pivote
        revolve_result = cmds.revolve(
            curve_copy,
            constructionHistory=True,
            object=True,
            polygon=0,  # NURBS surface
            axis=(0, 1, 0),
            pivot=new_pivot,
            startSweep=0,
            endSweep=360,
            degree=3,
            sections=8
        )

        nurbs_surface = revolve_result[0]
        print(f"Superficie NURBS creada: {nurbs_surface}")

        # 4. Convertir NURBS to Polygons
        poly_body = cmds.nurbsToPoly(
            nurbs_surface,
            name="polyBody",
            matchRenderTessellation=0,
            polygonType=1,  # Quads
            format=2,  # General
            uType=3,  # Per span # of iso params
            vType=3,
            uNumber=3,
            vNumber=3,
            constructionHistory=False
        )[0]

        # Eliminar NURBS y curva temporal
        cmds.delete(nurbs_surface, curve_copy)
        print(f"Convertido a polygons: {poly_body}")

        # 5. Mover el cuerpo hacia adelante en Z (solo 1 unidad)
        cmds.move(0, 0, 1, poly_body, relative=True)
        print("Cuerpo movido hacia adelante en Z")

        # 6. Reverse normals
        cmds.polyNormal(poly_body, normalMode=0, userNormalMode=0, constructionHistory=False)
        print("Normales revertidas")

        # 7. Smooth display
        cmds.displaySmoothness(poly_body, divisionsU=3, divisionsV=3,
                               pointsWire=16, pointsShaded=4, polygonObject=3)

        # 8. Freeze transforms
        cmds.select(poly_body, r=True)
        cmds.makeIdentity(apply=True, translate=True, rotate=True,
                          scale=True, normal=False)
        cmds.delete(constructionHistory=True)

        # 9. Crear passive collider - USANDO LA MISMA GEOMETRÍA
        cmds.select(poly_body, r=True)
        mel.eval('makeCollideNCloth;')

        n_rigid_shapes = cmds.ls(type="nRigid") or []
        if n_rigid_shapes:
            cmds.setAttr(f"{n_rigid_shapes[0]}.thickness", parent_scale * 0.05)
            cmds.setAttr(f"{n_rigid_shapes[0]}.solverDisplay", 0)

        print(f"✓ Collider pasivo aplicado a polyBody")

        # 10. Crear cabeza - ajustar posición en Z usando el pivote
        body_bb = cmds.exactWorldBoundingBox(poly_body)

        head_radius = parent_scale * 1.7
        sphere = cmds.polySphere(
            radius=head_radius,
            subdivisionsAxis=20,
            subdivisionsHeight=20,
            axis=(0, 1, 0),
            constructionHistory=False
        )[0]

        # Calcular Y basado en bounding box + usar Z del pivote ajustado
        head_y_pos = body_bb[4] + (head_radius * 0.5)
        head_final_pos = [new_pivot[0], head_y_pos, new_pivot[2] + 1]  # +1 por el movimiento
        cmds.xform(sphere, ws=True, translation=head_final_pos)

        poly_head = cmds.rename(sphere, "polyHead")
        print(f"Cabeza creada en: {head_final_pos}")

        # 11. Smooth display cabeza
        cmds.displaySmoothness(poly_head, divisionsU=3, divisionsV=3,
                               pointsWire=16, pointsShaded=4, polygonObject=3)

        # 12. Freeze transforms cabeza
        cmds.select(poly_head, r=True)
        cmds.makeIdentity(apply=True, translate=True, rotate=True,
                          scale=True, normal=False)
        cmds.delete(constructionHistory=True)

        print(f"✓ Cuerpo: {poly_body} (con collider pasivo)")
        print(f"✓ Cabeza: {poly_head}")

        # DEBUG: Verificar qué estamos retornando
        print(f"DEBUG: Retornando tupla con {poly_body} y {poly_head}")
        result = (poly_body, poly_head)
        print(f"DEBUG: Tipo de resultado: {type(result)}, Longitud: {len(result)}")

        return poly_body, poly_head, None

    except Exception as e:
        print(f"✗ Error en paso 7: {str(e)}")
        traceback.print_exc()
        return (None, None, None)



def step8_create_torus_system():
    """PASO 8 FINAL - Orientación corregida:
    - Toroide y curva rotados +90° en X
    - Plano rotado -90° en X
    - Alineación completa y sin offset
    """
    print("=== PASO 8: Creando sistema de toroide (alineación final X-axis fix) ===")
    try:
        # Parámetros
        CTRL_RADIUS = 0.9
        PLANE_OFFSET = 0.02
        LOCATOR_OFFSET = 0.04

        # Borrar versiones previas
        for obj in ["polyTorus1", "driverPlane_target_001", "dynamic_target_002",
                    "dynamic_toro_ctrl_001", "dynamic_toro_ctrl_001_root"]:
            if cmds.objExists(obj):
                cmds.delete(obj)

        # ------------------------------------------------------------
        # 1. Crear Toroide
        # ------------------------------------------------------------
        torus = cmds.polyTorus(r=0.5, sr=0.2, sx=24, sy=12, name="polyTorus1")[0]
        cmds.makeIdentity(torus, apply=True, t=True, r=True, s=True, n=False)

        if cmds.objExists("joint_002"):
            jpos = cmds.xform("joint_002", q=True, ws=True, t=True)
            cmds.xform(torus, ws=True, t=jpos)
        else:
            jpos = (0, 0, 0)

        # 🔄 Rotar toroide +90° en X
        cmds.xform(torus, rotation=(0, 90, 0), worldSpace=True)
        cmds.makeIdentity(torus, apply=True, t=True, r=True, s=True, n=False)
        print(f"✓ Toroide creado y orientado en {jpos}")

        # ------------------------------------------------------------
        # 2. Crear plano driver (rotar -90° en X)
        # ------------------------------------------------------------
        plane = cmds.polyPlane(w=1, h=1, sx=1, sy=1, name="driverPlane_target_001")[0]
        cmds.matchTransform(plane, torus)
        cmds.xform(plane, rotation=(-90, 0, 0), worldSpace=True)
        cmds.xform(plane, relative=True, objectSpace=True, translation=(0, 0, PLANE_OFFSET))
        cmds.makeIdentity(plane, apply=True, t=True, r=True, s=True, n=False)
        print("✓ Plano alineado (rotado -90° en X)")

        # ------------------------------------------------------------
        # 3. Bind Skin y Copy Skin Weights
        # ------------------------------------------------------------
        if cmds.objExists("joint_001"):
            skin = cmds.skinCluster("joint_001", plane, toSelectedBones=True)[0]
            print(f"✓ Skin Cluster aplicado: {skin}")
        else:
            print("⚠ No se encontró joint_001, omitiendo bind skin.")

        if cmds.objExists("polyTail"):
            try:
                cmds.copySkinWeights(
                    sourceSkin="polyTail",
                    destinationSkin=plane,
                    noMirror=True,
                    surfaceAssociation="closestPoint",
                    influenceAssociation="closestJoint"
                )
                print("✓ Pesos copiados desde polyTail → plano")
            except Exception as e:
                print(f"⚠ Error copiando pesos: {e}")

        # ------------------------------------------------------------
        # 4. Locator y Constraint
        # ------------------------------------------------------------
        locator = cmds.spaceLocator(name="dynamic_target_002")[0]
        cmds.matchTransform(locator, plane)
        cmds.xform(locator, relative=True, objectSpace=True, translation=(0, 0, LOCATOR_OFFSET))
        cmds.makeIdentity(locator, apply=True, t=True, r=True, s=True, n=False)

        con = cmds.pointOnPolyConstraint(plane, locator, mo=False)[0]
        try:
            for attr in ["U0", "V0"]:
                if cmds.objExists(f"{con}.{attr}"):
                    cmds.setAttr(f"{con}.{attr}", 0.5)
        except:
            pass
        print("✓ Locator creado y vinculado al plano")

        # ------------------------------------------------------------
        # 5. Curva de control (+90° en X)
        # ------------------------------------------------------------
        ctrl = cmds.circle(name="dynamic_toro_ctrl_001", nr=(0, 0, 1), r=CTRL_RADIUS, sections=16)[0]
        cmds.matchTransform(ctrl, torus)
        cmds.xform(ctrl, rotation=(0, 0, 90), worldSpace=True)
        cmds.makeIdentity(ctrl, apply=True, t=True, r=True, s=True, n=False)
        print("✓ Curva de control creada y alineada (+90° en X)")

        # ------------------------------------------------------------
        # 6. Crear root del control y jerarquía
        # ------------------------------------------------------------
        root_grp = cmds.group(empty=True, name="dynamic_toro_ctrl_001_root")
        cmds.matchTransform(root_grp, ctrl)
        cmds.parent(ctrl, root_grp)
        cmds.parent(root_grp, locator)
        cmds.makeIdentity(root_grp, apply=True, t=True, r=True, s=True, n=False)
        print("✓ Root y jerarquía configurados")

        # ------------------------------------------------------------
        # 7. Constraints finales (sin offset)
        # ------------------------------------------------------------
        cmds.parentConstraint(ctrl, torus, mo=False)
        cmds.scaleConstraint(ctrl, torus, mo=False)
        print("✓ Constraints aplicados sin maintain offset")

        # --- AJUSTE FINAL DE POSICIÓN GLOBAL ---
        offset_z = -0.2  # 🔹 ajusta este valor según la distancia que necesites
        for obj in [torus, plane, ctrl]:
            if cmds.objExists(obj):
                cmds.move(0, 0, offset_z, obj, relative=True, worldSpace=True)
        print(f"Todos los objetos desplazados {offset_z} unidades en -Z para evitar intersección.")

        print("\n✅ Sistema de toroide COMPLETADO y perfectamente alineado.")
        print(f"  Toroide: {torus}\n  Plano: {plane}\n  Locator: {locator}\n  Control: {ctrl}\n  Root: {root_grp}")

        cmds.select(clear=True)
        return torus, plane, locator, ctrl, root_grp

    except Exception:
        traceback.print_exc()
        cmds.warning("⚠ Error general en el paso 8.")
        return None



def create_complete_dynamic_rig():
    """Crear rig dinámico completo"""
    print("\n" + "=" * 60)
    print("CREANDO RIG DINÁMICO COMPLETO")
    print("=" * 60 + "\n")

    cleanup_previous_rig()

    joints, ik_joints, curve = step1_use_existing_joints()
    if not all([joints, ik_joints, curve]):
        print("Error en Paso 1")
        return None

    output_curve = step2_make_curve_dynamic()
    if not output_curve:
        print("Error en Paso 2")
        return None

    ik_handle = step3_create_ik_spline()
    if not ik_handle:
        print("Error en Paso 3")
        return None

    step4_configure_nucleus_and_follicle()

    ctrl, root = step5_create_dynamic_control()
    if not ctrl:
        print("Error en Paso 5")
        return None

    poly_tail = step6_create_poly_tail()
    if not poly_tail:
        print("Error en Paso 6")
        return None

    body, head = step7_create_body_and_head()
    torus_system = step8_create_torus_system()

    print("\n" + "=" * 60)
    print("RIG DINÁMICO COMPLETADO")
    print("=" * 60 + "\n")

    return {
        'joints': joints,
        'ik_joints': ik_joints,
        'curve': curve,
        'output_curve': output_curve,
        'ik_handle': ik_handle,
        'control': ctrl,
        'control_root': root,
        'poly_tail': poly_tail,
        'body': body,
        'head': head,
        'torus_system': torus_system
    }


# =========================================================
# UTILIDADES
# =========================================================

def adjust_hair_system_settings(stiffness=0.5, damping=0.1, gravity=98):
    """Ajustar física"""
    if cmds.objExists("hairSystemShape1"):
        cmds.setAttr("hairSystemShape1.stiffness", stiffness)
        cmds.setAttr("hairSystemShape1.damp", damping)
        print(f"Stiffness={stiffness}, Damping={damping}")

    if cmds.objExists("nucleus1"):
        cmds.setAttr("nucleus1.gravity", gravity)
        print(f"Gravedad={gravity}")


def reset_simulation():
    """Resetear simulación"""
    cmds.currentTime(1)
    if cmds.objExists("nucleus1"):
        cmds.setAttr("nucleus1.startFrame", 1)
    print("Simulación reseteada")


def bake_simulation(start_frame=1, end_frame=100):
    """Bakear simulación"""
    try:
        fk_joints = [j for j in cmds.ls("joint_*", type="joint") or []
                     if not j.startswith("joint_IK_")]

        if not fk_joints:
            cmds.warning("No hay joints FK")
            return

        cmds.select(fk_joints, r=True)
        cmds.bakeResults(
            simulation=True, time=(start_frame, end_frame),
            sampleBy=1, oversamplingRate=1,
            disableImplicitControl=True,
            preserveOutsideKeys=False,
            sparseAnimCurveBake=False,
            removeBakedAttributeFromLayer=False,
            bakeOnOverrideLayer=False,
            minimizeRotation=True,
            controlPoints=False,
            shape=False
        )

        print(f"Bakeado: frames {start_frame}-{end_frame}")

    except Exception as e:
        cmds.warning(f"Error: {str(e)}")


# =========================================================
# INTERFAZ PYSIDE
# =========================================================

if PYSIDE_AVAILABLE:
    class DynamicRigUI(QtWidgets.QDialog):
        def __init__(self, parent=maya_main_window()):
            super(DynamicRigUI, self).__init__(parent)

            self.setWindowTitle("Dynamic Rig Builder")
            self.setMinimumSize(500, 700)
            self.current_step = 0

            self.create_widgets()
            self.create_layouts()
            self.create_connections()
            self.update_step_status()

        def create_widgets(self):
            self.title_label = QtWidgets.QLabel("Dynamic Rig Builder")
            self.title_label.setAlignment(QtCore.Qt.AlignCenter)
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            self.title_label.setFont(font)

            self.info_text = QtWidgets.QTextEdit()
            self.info_text.setMaximumHeight(150)
            self.info_text.setReadOnly(True)
            self.info_text.setText(
                "PROCESO:\n\n"
                "1. Crear joints y curva base\n"
                "2. Hacer curva dinámica (nHair)\n"
                "3. Crear IK Spline Handle\n"
                "4. Configurar Nucleus y Follicle\n"
                "5. Crear control dinámico\n"
                "6. Crear polyTail con skin\n"
                "7. Crear cuerpo y cabeza\n"
                "8. Crear sistema toroide"
            )

            self.step1a_btn = QtWidgets.QPushButton("PASO 1: Crear Joints + Curva")
            self.step1b_btn = QtWidgets.QPushButton("PASO 1: Usar Joints Existentes")
            self.step2_btn = QtWidgets.QPushButton("PASO 2: Curva Dinámica")
            self.step3_btn = QtWidgets.QPushButton("PASO 3: IK Spline")
            self.step4_btn = QtWidgets.QPushButton("PASO 4: Configurar Nucleus")
            self.step5_btn = QtWidgets.QPushButton("PASO 5: Control Dinámico")
            self.step6_btn = QtWidgets.QPushButton("PASO 6: PolyTail")
            self.step7_btn = QtWidgets.QPushButton("PASO 7: Cuerpo y Cabeza")
            self.step8_btn = QtWidgets.QPushButton("PASO 8: Sistema Toroide")

            self.complete_btn = QtWidgets.QPushButton("CREAR RIG COMPLETO")
            self.complete_btn.setStyleSheet(
                "QPushButton { background-color: #4CAF50; color: white; "
                "font-weight: bold; padding: 12px; font-size: 14px; }"
            )

            self.cleanup_btn = QtWidgets.QPushButton("Limpiar Rig Anterior")
            self.cleanup_btn.setStyleSheet("background-color: #f44336; color: white;")

            self.gravity_label = QtWidgets.QLabel("Gravedad:")
            self.gravity_spinbox = QtWidgets.QDoubleSpinBox()
            self.gravity_spinbox.setRange(0, 200)
            self.gravity_spinbox.setValue(98)
            self.gravity_spinbox.setSingleStep(10)

            self.stiffness_label = QtWidgets.QLabel("Stiffness:")
            self.stiffness_spinbox = QtWidgets.QDoubleSpinBox()
            self.stiffness_spinbox.setRange(0, 1)
            self.stiffness_spinbox.setValue(0.5)
            self.stiffness_spinbox.setSingleStep(0.05)

            self.damping_label = QtWidgets.QLabel("Damping:")
            self.damping_spinbox = QtWidgets.QDoubleSpinBox()
            self.damping_spinbox.setRange(0, 1)
            self.damping_spinbox.setValue(0.1)
            self.damping_spinbox.setSingleStep(0.05)

            self.apply_physics_btn = QtWidgets.QPushButton("Aplicar Física")

            self.log_text = QtWidgets.QTextEdit()
            self.log_text.setMaximumHeight(180)
            self.log_text.setReadOnly(True)

            self.clear_log_btn = QtWidgets.QPushButton("Limpiar Log")
            self.close_btn = QtWidgets.QPushButton("Cerrar")

        def create_layouts(self):
            main_layout = QtWidgets.QVBoxLayout(self)

            main_layout.addWidget(self.title_label)
            main_layout.addWidget(self.info_text)

            line = QtWidgets.QFrame()
            line.setFrameShape(QtWidgets.QFrame.HLine)
            line.setFrameShadow(QtWidgets.QFrame.Sunken)
            main_layout.addWidget(line)

            steps_group = QtWidgets.QGroupBox("Proceso Paso a Paso")
            steps_layout = QtWidgets.QVBoxLayout(steps_group)

            step1_layout = QtWidgets.QHBoxLayout()
            step1_layout.addWidget(self.step1a_btn)
            step1_layout.addWidget(self.step1b_btn)
            steps_layout.addLayout(step1_layout)

            steps_layout.addWidget(self.step2_btn)
            steps_layout.addWidget(self.step3_btn)
            steps_layout.addWidget(self.step4_btn)
            steps_layout.addWidget(self.step5_btn)
            steps_layout.addWidget(self.step6_btn)
            steps_layout.addWidget(self.step7_btn)
            steps_layout.addWidget(self.step8_btn)

            main_layout.addWidget(steps_group)
            main_layout.addWidget(self.complete_btn)
            main_layout.addWidget(self.cleanup_btn)

            physics_group = QtWidgets.QGroupBox("Parámetros de Física")
            physics_layout = QtWidgets.QFormLayout(physics_group)
            physics_layout.addRow(self.gravity_label, self.gravity_spinbox)
            physics_layout.addRow(self.stiffness_label, self.stiffness_spinbox)
            physics_layout.addRow(self.damping_label, self.damping_spinbox)
            physics_layout.addRow(self.apply_physics_btn)
            main_layout.addWidget(physics_group)

            log_group = QtWidgets.QGroupBox("Log de Progreso")
            log_layout = QtWidgets.QVBoxLayout(log_group)
            log_layout.addWidget(self.log_text)

            log_buttons = QtWidgets.QHBoxLayout()
            log_buttons.addWidget(self.clear_log_btn)
            log_buttons.addStretch()
            log_buttons.addWidget(self.close_btn)
            log_layout.addLayout(log_buttons)

            main_layout.addWidget(log_group)

        def create_connections(self):
            self.step1a_btn.clicked.connect(self.execute_step1_create)
            self.step1b_btn.clicked.connect(self.execute_step1_existing)
            self.step2_btn.clicked.connect(self.execute_step2)
            self.step3_btn.clicked.connect(self.execute_step3)
            self.step4_btn.clicked.connect(self.execute_step4)
            self.step5_btn.clicked.connect(self.execute_step5)
            self.step6_btn.clicked.connect(self.execute_step6)
            self.step7_btn.clicked.connect(self.execute_step7)
            self.step8_btn.clicked.connect(self.execute_step8)
            self.complete_btn.clicked.connect(self.create_complete)
            self.cleanup_btn.clicked.connect(self.cleanup_rig)
            self.apply_physics_btn.clicked.connect(self.apply_physics)
            self.clear_log_btn.clicked.connect(lambda: self.log_text.clear())
            self.close_btn.clicked.connect(self.close)

        def update_step_status(self):
            buttons = [
                self.step1a_btn, self.step1b_btn, self.step2_btn,
                self.step3_btn, self.step4_btn, self.step5_btn,
                self.step6_btn, self.step7_btn, self.step8_btn
            ]

            for i, btn in enumerate(buttons):
                step_index = i if i < 2 else i - 1

                if step_index < self.current_step:
                    btn.setStyleSheet("QPushButton { background-color: #2E7D32; color: white; }")
                elif step_index == self.current_step:
                    btn.setStyleSheet("QPushButton { background-color: #1976D2; color: white; font-weight: bold; }")
                else:
                    btn.setStyleSheet("")

        def log_message(self, message):
            self.log_text.append(message)
            self.log_text.verticalScrollBar().setValue(
                self.log_text.verticalScrollBar().maximum()
            )

        def execute_step1_create(self):
            try:
                global _joints, _ik_joints, _dynamic_curve
                self.log_message("\n" + "=" * 50)
                self.log_message("Ejecutando PASO 1: Crear Joints...")
                _joints, _ik_joints, _dynamic_curve = step1_create_joints_and_curve()
                if all([_joints, _ik_joints, _dynamic_curve]):
                    self.current_step = 1
                    self.update_step_status()
                    self.log_message("✓ PASO 1 completado")
                else:
                    self.log_message("✗ Error en PASO 1")
            except Exception as e:
                self.log_message(f"✗ Error: {str(e)}")

        def execute_step1_existing(self):
            try:
                global _joints, _ik_joints, _dynamic_curve
                self.log_message("\n" + "=" * 50)
                self.log_message("Ejecutando PASO 1: Usar Existentes...")
                _joints, _ik_joints, _dynamic_curve = step1_use_existing_joints()
                if all([_joints, _ik_joints, _dynamic_curve]):
                    self.current_step = 1
                    self.update_step_status()
                    self.log_message("✓ PASO 1 completado")
                else:
                    self.log_message("✗ No se encontraron joints")
            except Exception as e:
                self.log_message(f"✗ Error: {str(e)}")

        def execute_step2(self):
            if self.current_step < 1:
                self.log_message("✗ Primero ejecuta PASO 1")
                return
            try:
                global _dynamic_curve_output
                self.log_message("\nEjecutando PASO 2...")
                _dynamic_curve_output = step2_make_curve_dynamic()
                if _dynamic_curve_output:
                    self.current_step = 2
                    self.update_step_status()
                    self.log_message("✓ PASO 2 completado")
                else:
                    self.log_message("✗ Error en PASO 2")
            except Exception as e:
                self.log_message(f"✗ Error: {str(e)}")

        def execute_step3(self):
            if self.current_step < 2:
                self.log_message("✗ Primero ejecuta PASOS 1-2")
                return
            try:
                global _ik_handle
                self.log_message("\nEjecutando PASO 3...")
                _ik_handle = step3_create_ik_spline()
                if _ik_handle:
                    self.current_step = 3
                    self.update_step_status()
                    self.log_message("✓ PASO 3 completado")
                else:
                    self.log_message("✗ Error en PASO 3")
            except Exception as e:
                self.log_message(f"✗ Error: {str(e)}")

        def execute_step4(self):
            if self.current_step < 3:
                self.log_message("✗ Primero ejecuta PASOS 1-3")
                return
            try:
                self.log_message("\nEjecutando PASO 4...")
                step4_configure_nucleus_and_follicle()
                self.current_step = 4
                self.update_step_status()
                self.log_message("✓ PASO 4 completado")
            except Exception as e:
                self.log_message(f"✗ Error: {str(e)}")

        def execute_step5(self):
            if self.current_step < 4:
                self.log_message("✗ Primero ejecuta PASOS 1-4")
                return
            try:
                global _control
                self.log_message("\nEjecutando PASO 5...")
                _control, root = step5_create_dynamic_control()
                if _control:
                    self.current_step = 5
                    self.update_step_status()
                    self.log_message("✓ PASO 5 completado")
                else:
                    self.log_message("✗ Error en PASO 5")
            except Exception as e:
                self.log_message(f"✗ Error: {str(e)}")

        def execute_step6(self):
            if self.current_step < 5:
                self.log_message("✗ Primero ejecuta PASOS 1-5")
                return
            try:
                global _poly_tail
                self.log_message("\nEjecutando PASO 6...")
                _poly_tail = step6_create_poly_tail()
                if _poly_tail:
                    self.current_step = 6
                    self.update_step_status()
                    self.log_message("✓ PASO 6 completado")
                else:
                    self.log_message("✗ Error en PASO 6")
            except Exception as e:
                self.log_message(f"✗ Error: {str(e)}")

        def execute_step7(self):
            if self.current_step < 6:
                self.log_message("✗ Primero ejecuta PASOS 1-6")
                return
            try:
                global _poly_body, _poly_head
                self.log_message("\nEjecutando PASO 7...")
                _poly_body, _poly_head, collider = step7_create_body_and_head()
                if _poly_body:
                    self.current_step = 7
                    self.update_step_status()
                    self.log_message("✓ PASO 7 completado")
                else:
                    self.log_message("✗ Error en PASO 7")
            except Exception as e:
                self.log_message(f"✗ Error: {str(e)}")

        def execute_step8(self):
            if self.current_step < 7:
                self.log_message("✗ Primero ejecuta PASOS 1-7")
                return
            try:
                self.log_message("\nEjecutando PASO 8...")
                result = step8_create_torus_system()
                if result:
                    self.current_step = 8
                    self.update_step_status()
                    self.log_message("✓ PASO 8 completado")
                    self.log_message("\n*** RIG COMPLETADO ***")
                else:
                    self.log_message("✗ Error en PASO 8")
            except Exception as e:
                self.log_message(f"✗ Error: {str(e)}")

        def create_complete(self):
            try:
                self.log_message("\n" + "=" * 50)
                self.log_message("CREANDO RIG COMPLETO...")

                result = create_complete_dynamic_rig()

                if result:
                    global _joints, _ik_joints, _dynamic_curve
                    global _dynamic_curve_output, _ik_handle, _control
                    global _poly_tail, _poly_body, _poly_head

                    _joints = result['joints']
                    _ik_joints = result['ik_joints']
                    _dynamic_curve = result['curve']
                    _dynamic_curve_output = result['output_curve']
                    _ik_handle = result['ik_handle']
                    _control = result['control']
                    _poly_tail = result['poly_tail']
                    _poly_body = result['body']
                    _poly_head = result['head']

                    self.current_step = 8
                    self.update_step_status()

                    self.log_message("\n*** RIG COMPLETO EXITOSO ***")
                    self.log_message(f"Joints FK: {len(_joints)}")
                    self.log_message(f"Joints IK: {len(_ik_joints)}")
                else:
                    self.log_message("\n✗ Error creando rig")

            except Exception as e:
                self.log_message(f"\n✗ Error: {str(e)}")

        def cleanup_rig(self):
            self.log_message("\nLimpiando rig...")
            cleanup_previous_rig()
            self.current_step = 0
            self.update_step_status()
            self.log_message("✓ Limpieza completada")

        def apply_physics(self):
            try:
                gravity = self.gravity_spinbox.value()
                stiffness = self.stiffness_spinbox.value()
                damping = self.damping_spinbox.value()

                if cmds.objExists("nucleus1"):
                    cmds.setAttr("nucleus1.gravity", gravity)
                    self.log_message(f"\n✓ Gravedad: {gravity}")

                if cmds.objExists("hairSystemShape1"):
                    cmds.setAttr("hairSystemShape1.stiffness", stiffness)
                    cmds.setAttr("hairSystemShape1.damp", damping)
                    self.log_message(f"✓ Stiffness: {stiffness}")
                    self.log_message(f"✓ Damping: {damping}")
                else:
                    self.log_message("\n✗ hairSystem no existe")

            except Exception as e:
                self.log_message(f"\n✗ Error: {str(e)}")


    def show_dynamic_rig_ui():
        """Mostrar interfaz PySide"""
        global dynamic_rig_ui_window

        try:
            dynamic_rig_ui_window.close()
            dynamic_rig_ui_window.deleteLater()
        except:
            pass

        dynamic_rig_ui_window = DynamicRigUI()
        dynamic_rig_ui_window.show()
        return dynamic_rig_ui_window


# =========================================================
# FUNCIONES PRINCIPALES
# =========================================================

def show_rig_ui():
    """Mostrar UI PySide"""
    if PYSIDE_AVAILABLE:
        print("Abriendo interfaz...")
        return show_dynamic_rig_ui()
    else:
        print("ERROR: PySide no disponible.")
        print("Usa: create_complete_dynamic_rig()")
        return None


# =========================================================
# PUNTO DE ENTRADA
# =========================================================

if __name__ == "__main__":
    show_rig_ui()
else:
    print("\n" + "=" * 60)
    print("DYNAMIC RIG BUILDER - nHair")
    print("=" * 60)
    print("\nFUNCIONES PRINCIPALES:")
    print("  show_rig_ui()                   # Interfaz PySide")
    print("  create_complete_dynamic_rig()   # Rig completo")
    print("  cleanup_previous_rig()          # Limpiar")
    print("\nPASO A PASO:")
    print("  step1_create_joints_and_curve()      # Nuevos")
    print("  step1_use_existing_joints()          # Existentes")
    print("  step2_make_curve_dynamic()           # nHair")
    print("  step3_create_ik_spline()             # IK Spline")
    print("  step4_configure_nucleus_and_follicle()  # Física")
    print("  step5_create_dynamic_control()       # Control")
    print("  step6_create_poly_tail()             # Cola")
    print("  step7_create_body_and_head()         # Cuerpo")
    print("  step8_create_torus_system()          # Toroide")
    print("\nUTILIDADES:")
    print("  adjust_hair_system_settings(stiffness, damping, gravity)")
    print("  reset_simulation()")
    print("  bake_simulation(start_frame, end_frame)")
    print("=" * 60)

    if PYSIDE_AVAILABLE:
        print("LISTO - Ejecuta: show_rig_ui()")
    else:
        print("LISTO - Ejecuta: create_complete_dynamic_rig()")
    print("=" * 60)