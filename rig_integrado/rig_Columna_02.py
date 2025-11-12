import maya.cmds as cmds
import traceback

# -------------------------------
# ESTADO DE PASOS
# -------------------------------
step_status = {}

def update_step_status(step_num, button_name):
    #Marca un paso como completado (verde + check)
    step_status[step_num] = True

    if cmds.control(button_name, exists=True):
        try:
            current_label = cmds.button(button_name, q=True, label=True)
            if "✓" not in current_label:
                cmds.button(button_name, edit=True,
                            backgroundColor=[0.2, 0.5, 0.3],
                            label=current_label + " ✓")
        except Exception:
            cmds.button(button_name, edit=True,
                        backgroundColor=[0.2, 0.5, 0.3])

    # Mensaje sutil en viewport
    try:
        cmds.inViewMessage(amg=f'<span style="color:#7FFF7F;">Paso {step_num} completado</span>',
                           pos='topCenter', fade=True, fst=800, ft=150)
    except Exception:
        pass

def execute_step(step_num, function, button_name):
    #Ejecuta función y actualiza estado
    try:
        result = function()
        # Solo marca como completado si la función devuelve algo válido
        if result:
            update_step_status(step_num, button_name)
        return result
    except Exception as e:
        traceback.print_exc()
        cmds.warning(f"Error en paso {step_num}: {str(e)}")

def reset_all_steps():
    #Reinicia todos los estados y botones
    global step_status
    step_status = {}

    for step in UI_STEPS:
        btn_name = step["btn_name"]
        label = step["label"]
        if cmds.control(btn_name, exists=True):
            bg = step.get("bg", [0.32, 0.32, 0.32])
            try:
                cmds.button(btn_name, edit=True, backgroundColor=bg, label=label)
            except Exception:
                # fallback: borrar y recrear botón más adelante si algo falla
                pass

# -------------------------------
# FUNCIONES DE RIG
# -------------------------------

def use_existing_joints_and_curve():
    existing = cmds.ls("joint*", type="joint") or []
    if not existing:
        try:
            cmds.inViewMessage(amg='<span style="color:#FF7070;">No hay joints en la escena</span>',
                               pos='midCenter', fade=True, fst=800, ft=150)
        except:
            pass
        cmds.warning("⚠️ No se encontraron joints en la escena. Crea joints primero.")
        return None

    existing.sort(key=lambda x: int(''.join(c for c in x if c.isdigit()) or 0))
    joints = [cmds.rename(jnt, f"joint_{i:03d}") for i, jnt in enumerate(existing, start=1)]

    # --- Orientar solo hasta el penúltimo joint ---
    if len(joints) > 1:
        cmds.select(joints[0:joints.index(joints[-1])], r=True)
        cmds.joint(e=True, oj="xyz", sao="zup", ch=True, zso=True)

    # --- Limpiar orientación del último joint ---
    for ax in "XYZ":
        cmds.setAttr(f"{joints[-1]}.jointOrient{ax}", 0)

    # Crear curva basada en sus posiciones
    curve = cmds.curve(p=[cmds.xform(j, q=True, ws=True, t=True) for j in joints],
                       d=3, name="splineCurve_001")
    cmds.rebuildCurve(curve, ch=False, rpo=True, rt=0, end=1, kr=0,
                      kcp=False, kep=True, kt=False, s=2, d=3, tol=0.01)

    print("=== Curva creada y joints existentes orientados correctamente ===")
    return joints, curve


def create_and_connect_locators_to_curve(curve="splineCurve_001"):
    shapes = cmds.listRelatives(curve, shapes=True) or []
    if not shapes:
        cmds.warning(f"No se encontró shape en {curve}")
        return
    curve_shape = shapes[0]
    cmds.setAttr(f"{curve_shape}.dispCV", 1)
    locators = []
    cvs = cmds.ls(f"{curve_shape}.cv[*]", fl=True) or []
    for i, cv in enumerate(cvs, start=1):
        loc = cmds.spaceLocator(name=f"spineLoc_ctrl_{i:03d}")[0]
        cmds.xform(loc, ws=True, t=cmds.pointPosition(cv, w=True))
        cmds.connectAttr(f"{loc}.translate", f"{curve_shape}.controlPoints[{i-1}]", f=True)
        locators.append(loc)
    print("=== Locators creados y conectados ===")
    return locators, curve_shape

def connect_locators_with_decompose(curve="splineCurve_001"):
    shapes = cmds.listRelatives(curve, shapes=True) or []
    if not shapes:
        cmds.warning(f"No se encontró shape en {curve}")
        return
    curve_shape = shapes[0]
    locators = sorted(cmds.ls("spineLoc_ctrl_*", type="transform") or [])
    if not locators:
        cmds.warning("No se encontraron locators")
        return
    for i, loc in enumerate(locators):
        dm_node = cmds.createNode("decomposeMatrix", name=f"{loc}_dm")
        cmds.connectAttr(f"{loc}.worldMatrix[0]", f"{dm_node}.inputMatrix", f=True)
        cmds.connectAttr(f"{dm_node}.outputTranslate", f"{curve_shape}.controlPoints[{i}]", f=True)
        try:
            cmds.parent(loc, curve)
        except:
            pass
    print("=== DecomposeMatrix conectado ===")
    return locators, curve_shape

def organize_spine_ik_controls(curve="splineCurve_001"):
    locators = sorted(cmds.ls("spineLoc_ctrl_*", type="transform") or [])
    if not locators:
        cmds.warning("No se encontraron locators")
        return
    root_groups = []
    for loc in locators:
        root_name = loc.replace("spineLoc_ctrl_", "spineLocRoot_ctrl_")
        root = cmds.group(empty=True, name=root_name)
        try:
            cmds.delete(cmds.parentConstraint(loc, root))
        except: pass
        cmds.parent(loc, root)
        try:
            cmds.setAttr(f"{loc}.translate", 0, 0, 0)
            cmds.setAttr(f"{loc}.rotate", 0, 0, 0)
        except: pass
        try:
            cmds.parent(root, curve)
        except: pass
        root_groups.append(root)
    for i, loc in enumerate(locators, start=1):
        circle = cmds.circle(name=f"spineCtrlShape_{i:03d}", nr=(0,1,0), r=0.5)[0]
        for shp in cmds.listRelatives(circle, shapes=True) or []:
            try:
                cmds.parent(shp, loc, r=True, s=True)
            except:
                pass
        cmds.delete(circle)
    if cmds.objExists("spineLoc_ctrl_001") and cmds.objExists("spineLocRoot_ctrl_002"):
        try: cmds.parent("spineLocRoot_ctrl_002", "spineLoc_ctrl_001")
        except: pass
    if cmds.objExists("spineLoc_ctrl_004") and cmds.objExists("spineLocRoot_ctrl_005"):
        try: cmds.parent("spineLocRoot_ctrl_004", "spineLoc_ctrl_005")
        except: pass
    print("=== Controles IK organizados ===")
    return root_groups, locators

def create_targets_on_curve(curve="splineCurve_001", num_targets=5):
    shapes = cmds.listRelatives(curve, shapes=True) or []
    if not shapes:
        cmds.warning(f"No se encontró shape en {curve}")
        return
    curve_shape = shapes[0]
    targets = []
    for i in range(1, num_targets+1):
        loc = cmds.spaceLocator(name=f"spineTarget_ctrl_{i:03d}")[0]
        pci = cmds.createNode("pointOnCurveInfo", name=f"pointOnCurveInfo_{i:03d}")
        cmds.connectAttr(f"{curve_shape}.worldSpace[0]", f"{pci}.inputCurve", f=True)
        cmds.connectAttr(f"{pci}.position", f"{loc}.translate", f=True)
        cmds.setAttr(f"{pci}.parameter", float(i-1)/(num_targets-1) if num_targets>1 else 0)
        targets.append(loc)
    print("=== Targets creados ===")
    return targets

def redirect_targets_with_aim(num_targets=5):
    targets = [f"spineTarget_ctrl_{i:03d}" for i in range(1, num_targets+1)]
    for i in range(1, num_targets):
        if not cmds.objExists(targets[i]) or not cmds.objExists(targets[i-1]):
            continue
        try:
            cmds.aimConstraint(targets[i], targets[i-1], mo=False, weight=1,
                               aimVector=(1,0,0), upVector=(0,1,0), worldUpType="scene")
        except:
            pass
    print("=== Aim Constraints creados ===")
    return targets

def parent_constraint_joints_to_targets(num_pairs=5):
    created = 0
    for i in range(1, num_pairs+1):
        t, j = f"spineTarget_ctrl_{i:03d}", f"joint_{i:03d}"
        if cmds.objExists(t) and cmds.objExists(j):
            try:
                cmds.parentConstraint(t, j, mo=True, weight=1)
                created += 1
                print(f"Constraint: {t} → {j}")
            except:
                cmds.warning(f"Error en constraint {t} → {j}")
    print("=== ParentConstraints creados ===")
    return created if created else None

# -------------------------------
# FUNCIÓN PARA EJECUCIÓN COMPLETA
# -------------------------------

def execute_all_steps():
    """Ejecuta todos los pasos del rig de columna automáticamente."""
    try:
        print("🚀 INICIANDO EJECUCIÓN COMPLETA DEL RIG DE COLUMNA...")
        
        # Paso 1: Usar Joints Existentes
        print("📝 Paso 1: Usando joints existentes...")
        result1 = use_existing_joints_and_curve()
        if result1:
            update_step_status(1, "step1b_btn")
        
        # Paso 2: Locators + Conectar
        print("📍 Paso 2: Creando y conectando locators...")
        result2 = create_and_connect_locators_to_curve()
        if result2:
            update_step_status(2, "step2_btn")
        
        # Paso 3: DecomposeMatrix
        print("🔗 Paso 3: Conectando decomposeMatrix...")
        result3 = connect_locators_with_decompose()
        if result3:
            update_step_status(3, "step3_btn")
        
        # Paso 4: Organizar Controles IK
        print("🎯 Paso 4: Organizando controles IK...")
        result4 = organize_spine_ik_controls()
        if result4:
            update_step_status(4, "step4_btn")
        
        # Paso 5: Targets
        print("🎯 Paso 5: Creando targets...")
        result5 = create_targets_on_curve()
        if result5:
            update_step_status(5, "step5_btn")
        
        # Paso 6: Aim Constraints
        print("🎯 Paso 6: Aplicando aim constraints...")
        result6 = redirect_targets_with_aim()
        if result6:
            update_step_status(6, "step6_btn")
        
        # Paso 7: Parent Targets → Joints
        print("🔗 Paso 7: Conectando targets a joints...")
        result7 = parent_constraint_joints_to_targets()
        if result7:
            update_step_status(7, "step7_btn")
        
        # Mensaje final
        cmds.inViewMessage(
            amg='<span style="color:#7FFF7F;">✅ Rig de columna completado automáticamente</span>',
            pos='topCenter', fade=True, fst=1500, ft=200
        )
        print("🎉 ¡RIG DE COLUMNA COMPLETADO EXITOSAMENTE!")
        
        return True
        
    except Exception as e:
        cmds.warning(f"❌ Error en ejecución automática: {str(e)}")
        traceback.print_exc()
        return False


# -------------------------------
# INTERFAZ
# -------------------------------
UI_STEPS = [
    {"num": 1, "btn_name": "step1b_btn", "label": "(1) Usar Joints Existentes", "func": use_existing_joints_and_curve},
    {"num": 2, "btn_name": "step2_btn", "label": "(2) Locators + Conectar", "func": create_and_connect_locators_to_curve},
    {"num": 3, "btn_name": "step3_btn", "label": "(3) DecomposeMatrix", "func": connect_locators_with_decompose},
    {"num": 4, "btn_name": "step4_btn", "label": "(4) Organizar Controles IK", "func": organize_spine_ik_controls},
    {"num": 5, "btn_name": "step5_btn", "label": "(5) Targets", "func": create_targets_on_curve},
    {"num": 6, "btn_name": "step6_btn", "label": "(6) Aim Constraints", "func": redirect_targets_with_aim},
    {"num": 7, "btn_name": "step7_btn", "label": "(7) Parent Targets → Joints", "func": parent_constraint_joints_to_targets},
    {"num": 8, "btn_name": "step8_btn", "label": "(8) Rig Columna Completo", "func": execute_all_steps, "bg": [0.28,0.28,0.28]},
]

def open_spine_ui():
    try:
        if cmds.window("spineRigUI", exists=True):
            cmds.deleteUI("spineRigUI")
        win = cmds.window("spineRigUI", title="Spine Rig Builder", w=360, h=420)
        cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnOffset=["both", 12])

        cmds.separator(h=8, style="none")
        cmds.text(label="SPINE RIG - MODULAR", align="center", font="boldLabelFont", h=25)
        cmds.separator(h=12, style="in")

        other_steps = [
            (1, "step1_btn", "(1) Usar Joints Existentes", use_existing_joints_and_curve),
            (2, "step2_btn", "(2) Locators + Conectar", create_and_connect_locators_to_curve),
            (3, "step3_btn", "(3) DecomposeMatrix", connect_locators_with_decompose),
            (4, "step4_btn", "(4) Organizar Controles IK", organize_spine_ik_controls),
            (5, "step5_btn", "(5) Targets", create_targets_on_curve),
            (6, "step6_btn", "(6) Aim Constraints", redirect_targets_with_aim),
            (7, "step7_btn", "(7) Parent Targets → Joints", parent_constraint_joints_to_targets),
        ]

        for num, btn_name, label, func in other_steps:
            cmds.button(btn_name, label=label, h=32,
                        c=(lambda _x, s=num, b=btn_name, f=func: execute_step(s, f, b)),
                        backgroundColor=[0.32, 0.32, 0.32])

        cmds.separator(h=15, style="in")
        cmds.button(label="↻ Reiniciar", h=28, c=lambda _x: reset_all_steps(),
                    backgroundColor=[0.35,0.35,0.38])
        cmds.separator(h=8, style="none")

        cmds.showWindow(win)
    except Exception:
        traceback.print_exc()
        cmds.warning("Ocurrió un error al abrir la UI. Revisa el Script Editor.")


# try:
#     open_spine_ui()
# except Exception:
#     traceback.print_exc()

# En su lugar:
if __name__ == "__main__":
    try:
        open_spine_ui()
    except Exception:
        traceback.print_exc()