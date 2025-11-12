import maya.cmds as cmds
import traceback

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

