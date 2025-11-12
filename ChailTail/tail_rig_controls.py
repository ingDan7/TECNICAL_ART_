import maya.cmds as cmds
import traceback

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