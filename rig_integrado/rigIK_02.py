import re
import maya.cmds as cmds
import traceback

# 1. BUILD CHAINS

def build_chains():
    """
    Detecta joints base, los renombra como FK, orienta la cadena correctamente,
    y duplica para IK y MAIN.
    """
    # 1. Detectar joints raíz
    all_joints = cmds.ls(type="joint")
    root_candidates = [j for j in all_joints if not cmds.listRelatives(j, parent=True)]

    if not root_candidates:
        cmds.error("No se encontró ningún joint raíz.")

    root = root_candidates[0]
    chain = cmds.listRelatives(root, ad=True, type="joint") or []
    chain = [root] + chain[::-1]

    if len(chain) < 3:
        cmds.error("Se necesitan al menos 3 joints para la pierna.")

    # 2. Generar nombres dinámicos para la cadena
    names = []
    if len(chain) == 3:
        names = ["upperLeg", "middleLeg", "endLeg"]
    else:
        # Para cadenas más largas: root, middle1, middle2..., end
        names.append("upperLeg")
        for i in range(1, len(chain)-1):
            names.append(f"middleLeg_{i:02d}")
        names.append("endLeg")

    fk_chain = []
    for j, name in zip(chain, names):
        new_name = f"{name}_practice_L_FK_joint_001"
        if cmds.objExists(new_name):
            cmds.delete(new_name)
        renamed = cmds.rename(j, new_name)
        fk_chain.append(renamed)

    # 3. Orientar solo hasta el penúltimo joint
    if len(fk_chain) > 1:
        cmds.select(fk_chain[:-1], r=True)
        cmds.joint(e=True, oj="xyz", sao="zup", ch=True, zso=True)

    # 4. Limpiar orientación del último joint
    for ax in "XYZ":
        cmds.setAttr(f"{fk_chain[-1]}.jointOrient{ax}", 0)

    # 5. Duplicar FK para crear IK y MAIN
    def duplicate_chain(source_chain, ctype, version):
        dup_root = cmds.duplicate(source_chain[0], rc=True)[0]
        children = cmds.listRelatives(dup_root, ad=True, type="joint") or []
        full_chain = [dup_root] + children[::-1]
        renamed_chain = []
        for j, name in zip(full_chain, names):
            new_name = f"{name}_practice_L_{ctype}_joint_{version}"
            renamed = cmds.rename(j, new_name)
            renamed_chain.append(renamed)
        return renamed_chain

    ik_chain = duplicate_chain(fk_chain, "IK", "002")
    main_chain = duplicate_chain(fk_chain, "MAIN", "003")

    return fk_chain, ik_chain, main_chain

# 2. SETUP FK CHAIN
def setup_fk_chain(fk_chain):
    """
    Configura la jerarquía FK: root/auto, controles y reconstrucción de jerarquía.
    """
    for i, joint in enumerate(fk_chain):
        # root/auto
        base_name = joint.replace("_joint_", "_")
        auto = cmds.group(empty=True, name=base_name+"auto_001")
        root = cmds.group(empty=True, name=base_name+"root_001")
        pos = cmds.xform(joint, q=True, ws=True, t=True)
        rot = cmds.xform(joint, q=True, ws=True, ro=True)
        cmds.xform(auto, ws=True, t=pos, ro=rot)
        cmds.xform(root, ws=True, t=pos, ro=rot)
        cmds.parent(joint, auto)
        cmds.parent(auto, root)

        # control
        if i == 0:  # Primer joint - plano YZ
            nr = (1,0,0)
        else:       # Resto de joints - plano XZ
            nr = (0,1,0)
        ctrl = cmds.circle(name=joint.replace("_joint_", "_ctrl_"), nr=nr, r=1)[0]
        shape = cmds.listRelatives(ctrl, shapes=True)[0]
        cmds.parent(shape, joint, r=True, s=True)
        cmds.delete(ctrl)

    # reconstruir jerarquía
    for i in range(len(fk_chain)-1):
        nxt_root = fk_chain[i+1].replace("_joint_", "_")+"root_001"
        cmds.parent(nxt_root, fk_chain[i])

# 3. SETUP IK CHAIN
# 3. SETUP IK CHAIN
def setup_ik_chain(ik_chain):
    """
    Configura la cadena IK con IK handle, pole vector y control IK.
    """
    # Usar el primer y último joint para el IK handle
    start_joint = ik_chain[0]
    end_joint = ik_chain[-1]
    
    ik_handle = cmds.ikHandle(sj=start_joint, ee=end_joint, sol="ikRPsolver",
                              n="middleLeg_practice_L_IKhandle_001")[0]
    eff = cmds.listConnections(f"{ik_handle}.endEffector") or []
    if eff: cmds.rename(eff[0], "middleLeg_practice_L_effector_001")

    # Pole vector - encontrar el joint con mayor desplazamiento en Z
    max_z_offset = 0
    max_z_joint = ik_chain[1]  # Por defecto usar el segundo joint
    
    for joint in ik_chain[1:-1]:  # Excluir el primero y el último
        pos = cmds.xform(joint, q=True, ws=True, t=True)
        z_offset = abs(pos[2])  # Valor absoluto del desplazamiento en Z
        if z_offset > max_z_offset:
            max_z_offset = z_offset
            max_z_joint = joint

    # Obtener posición del joint con mayor Z
    pv_pos = cmds.xform(max_z_joint, q=True, ws=True, t=True)
    
    # Crear pole vector group en la posición del joint
    pv_group = cmds.group(empty=True, n="middleLeg_practice_L_IKpoleVector_001")
    cmds.xform(pv_group, ws=True, t=pv_pos)
    
    # Reflejar en Z - mover en dirección opuesta al desplazamiento original
    z_direction = 1 if pv_pos[2] >= 0 else -1
    cmds.move(0, 0, 5 * z_direction, pv_group, r=True, os=True)

    pv_ctrl = cmds.circle(n="middleLeg_practice_L_IKpoleVectorCtrl_001", nr=(0,0,1), r=1)[0]
    shp = cmds.listRelatives(pv_ctrl, s=True)[0]
    cmds.parent(shp, pv_group, r=True, s=True)
    cmds.delete(pv_ctrl)
    
    pv_root = cmds.group(pv_group, n="middleLeg_practice_L_IKpoleVectorRoot_001")
    cmds.poleVectorConstraint(pv_group, ik_handle)

    # IK control
    ik_ctrl = cmds.curve(d=1, p=[(-1,0,-1),(1,0,-1),(1,0,1),(-1,0,1),(-1,0,-1)],
                         n="endLeg_practice_L_IKctrl_001")
    end_pos = cmds.xform(end_joint, q=True, ws=True, t=True)
    cmds.xform(ik_ctrl, ws=True, t=end_pos)
    cmds.parent(ik_handle, ik_ctrl)

    return ik_handle, pv_group

# 4. SETUP MAIN CHAIN (CONSTRAINTS + SWITCH)
def setup_main_chain(fk_chain, ik_chain, main_chain):
    """
    Crea constraints de MAIN a FK/IK y añade el switch FKIK.
    """
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

# 5. EJECUCIÓN AUTOMÁTICA DE TODOS LOS PASOS

def execute_all_steps_IK():
    """Ejecuta todos los pasos del rig de pierna automáticamente."""
    try:
        print("🚀 INICIANDO EJECUCIÓN COMPLETA DEL RIG DE PIERNA...")
        
        # Limpiar rig anterior
        print("🧹 Limpiando rig anterior...")
        cleanup_previous_rig()
        
        # Paso 1: Detectar Joints Base
        print("📝 Paso 1: Detectando joints base...")
        global _fk_chain, _ik_chain, _main_chain
        _fk_chain, _ik_chain, _main_chain = build_chains()
        update_step_status(1, "step1_btn")
        
        # Paso 2: Configurar Cadena FK
        print("🎯 Paso 2: Configurando cadena FK...")
        setup_fk_chain(_fk_chain)
        update_step_status(2, "step2_btn")
        
        # Paso 3: Configurar Cadena IK
        print("🔗 Paso 3: Configurando cadena IK...")
        setup_ik_chain(_ik_chain)
        update_step_status(3, "step3_btn")
        
        # Paso 4: Configurar Cadena MAIN
        print("⚙️ Paso 4: Configurando cadena MAIN...")
        setup_main_chain(_fk_chain, _ik_chain, _main_chain)
        update_step_status(4, "step4_btn")
        
        # Mensaje final
        cmds.inViewMessage(
            amg='<span style="color:#7FFF7F;">✅ Rig de pierna completado automáticamente</span>',
            pos='topCenter', fade=True, fst=1500, ft=200
        )
        print("🎉 ¡RIG DE PIERNA COMPLETADO EXITOSAMENTE!")
        
        return True
        
    except Exception as e:
        cmds.warning(f"❌ Error en ejecución automática: {str(e)}")
        traceback.print_exc()
        return False

# Función para limpiar nombres dinámicamente
def cleanup_previous_rig():
    # Buscar y eliminar todos los objetos relacionados con el rig
    patterns = [
        "*_practice_L_FK_joint_*",
        "*_practice_L_IK_joint_*", 
        "*_practice_L_MAIN_joint_*",
        "*_practice_L_IKhandle_*",
        "*_practice_L_effector_*",
        "*_practice_L_IKpoleVector_*",
        "*_practice_L_IKpoleVectorRoot_*",
        "*_practice_L_IKctrl_*",
        "Leg_practice_L_attributes_*",
        "FKIK_reverse"
    ]
    
    for pattern in patterns:
        objs = cmds.ls(pattern)
        for obj in objs:
            try:
                cmds.delete(obj)
            except:
                pass

def main():
    cleanup_previous_rig()
    fk_chain, ik_chain, main_chain = build_chains()
    setup_fk_chain(fk_chain)
    setup_ik_chain(ik_chain)
    setup_main_chain(fk_chain, ik_chain, main_chain)
    print("=== Rig FK/IK creado ===")

_fk_chain = []
_ik_chain = []
_main_chain = []

def ui_build_chains(*args):
    global _fk_chain, _ik_chain, _main_chain
    cleanup_previous_rig()
    _fk_chain, _ik_chain, _main_chain = build_chains()
    print("Cadenas creadas")

def ui_setup_fk(*args):
    if _fk_chain:
        setup_fk_chain(_fk_chain)
        print("FK configurado")
    else:
        cmds.warning("Primero crea las cadenas.")

def ui_setup_ik(*args):
    if _ik_chain:
        setup_ik_chain(_ik_chain)
        print("IK configurado")
    else:
        cmds.warning("Primero crea las cadenas.")

def ui_setup_main(*args):
    if _fk_chain and _ik_chain and _main_chain:
        setup_main_chain(_fk_chain, _ik_chain, _main_chain)
        print("MAIN configurado")
    else:
        cmds.warning("Primero crea las cadenas.")


# Estado de los pasos
step_status = {}

def update_step_status(step_num, button_name):
    """Marca un paso como completado (botón verde + check visual)."""
    step_status[step_num] = True
    if cmds.control(button_name, exists=True):
        cmds.button(button_name, e=True, bgc=(0.2, 0.5, 0.2), label=f"✓ Paso {step_num} completado")

def execute_step(step_num, func, button_name):
    """Ejecuta el paso y actualiza el botón según el resultado."""
    try:
        func()
        update_step_status(step_num, button_name)
    except Exception as e:
        cmds.warning(f"⚠ Error ejecutando paso {step_num}: {e}")
        traceback.print_exc()

def reset_all_steps():
    """Reinicia los botones a su color original."""
    for step in UI_STEPS:
        btn = step["btn_name"]
        if cmds.control(btn, exists=True):
            cmds.button(btn, e=True, bgc=(0.32, 0.32, 0.32), label=step["label"])
    step_status.clear()
    print("🔁 Progreso reiniciado.")

# ============================================================
# 🧩 DEFINICIÓN DE PASOS DE INTERFAZ
# ============================================================

UI_STEPS = [
    {"num": 1, "btn_name": "step1_btn", "label": "(1) Detectar Joints Base", "func": ui_build_chains},
    {"num": 2, "btn_name": "step2_btn", "label": "(2) Configurar Cadena FK", "func": ui_setup_fk},
    {"num": 3, "btn_name": "step3_btn", "label": "(3) Configurar Cadena IK", "func": ui_setup_ik},
    {"num": 4, "btn_name": "step4_btn", "label": "(4) Configurar Cadena MAIN", "func": ui_setup_main},
    {"num": 5, "btn_name": "step5_btn", "label": "(5) Rig Completo", "func": execute_all_steps_IK, "bg": [0.28,0.28,0.28]},
]

# ============================================================
# 🪶 CREACIÓN DE LA INTERFAZ
# ============================================================

def open_leg_rig_ui():
    """Abre la interfaz estilo rig_Columna_02, sin modificar la lógica interna."""
    try:
        if cmds.window("legRigUI", exists=True):
            cmds.deleteUI("legRigUI")

        win = cmds.window("legRigUI", title="Rig Pierna FK/IK - Modular", w=360, h=280)
        cmds.columnLayout(adjustableColumn=True, rowSpacing=6, columnOffset=["both", 12])

        cmds.text(label="RIG DE PIERNA - SISTEMA FK/IK", align="center", font="boldLabelFont", h=25)
        cmds.separator(h=12, style="in")

        for step in UI_STEPS:
            num, btn, label, func = step["num"], step["btn_name"], step["label"], step["func"]
            cmds.button(btn, label=label, h=32,
                        c=(lambda _x, s=num, b=btn, f=func: execute_step(s, f, b)),
                        bgc=[0.32, 0.32, 0.32])

        cmds.separator(h=15, style="in")
        cmds.button(label="↻ Reiniciar", h=30, c=lambda _x: reset_all_steps(),
                    bgc=[0.35, 0.35, 0.38])

        cmds.showWindow(win)
        print("🟢 Interfaz de rig de pierna lista.")

    except Exception:
        traceback.print_exc()
        cmds.warning("⚠ Error al crear la interfaz de rig de pierna.")

if __name__ == "__main__":
    open_leg_rig_ui()