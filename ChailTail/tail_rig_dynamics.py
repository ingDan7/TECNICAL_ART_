import maya.cmds as cmds
import traceback

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