from maya import cmds

def apply_aiToon_calligraphic(shader_name="aiToon_CalligraphicLine"):
    """
    Crea y asigna un shader aiToon con efecto Calligraphic Line
    a la selección actual en Maya.
    """

    # 1️⃣ Verificar selección
    selection = cmds.ls(sl=True, long=True)
    if not selection:
        cmds.warning("⚠️ Selecciona al menos una geometría para asignar el shader.")
        return

    # 2️⃣ Crear o reutilizar el shader
    if not cmds.objExists(shader_name):
        shader = cmds.shadingNode("aiToon", asShader=True, name=shader_name)
    else:
        shader = shader_name

    # 3️⃣ Crear o reutilizar el shading group
    sg_name = shader_name + "_SG"
    if not cmds.objExists(sg_name):
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=sg_name)
        cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader", force=True)
    else:
        sg = sg_name

    # 4️⃣ Configurar parámetros tipo "Calligraphic Line"
    # Activar línea caligráfica
    cmds.setAttr(shader + ".lineEnabled", 1)
    cmds.setAttr(shader + ".lineWidth", 0.8)
    cmds.setAttr(shader + ".lineColor", 0, 0, 0, type="double3")
    cmds.setAttr(shader + ".lineWidthModulation", 1)  # activa modulación del grosor
    cmds.setAttr(shader + ".lineProfileControl", 1)    # controla el perfil de variación

    # Opcional: efectos de sombra tipo tinta
    cmds.setAttr(shader + ".base", 0.8)
    cmds.setAttr(shader + ".baseColor", 1.0, 0.95, 0.85, type="double3")
    cmds.setAttr(shader + ".diffuse", 0.0)
    cmds.setAttr(shader + ".specular", 0.0)
    cmds.setAttr(shader + ".edgeDetection", 1)
    cmds.setAttr(shader + ".angleThreshold", 50)

    # 5️⃣ Asignar el shader a la selección
    for obj in selection:
        cmds.sets(obj, e=True, forceElement=sg)

    print(f"✅ Shader '{shader_name}' (Calligraphic Line) asignado a {len(selection)} objeto(s).")

# Ejecutar
apply_aiToon_calligraphic()
