import maya.cmds as cmds
import maya.mel as mel

def aplicar_shader_toon_ciudad():
    """Aplica el material y toon de PencilScribble al grupo ciudad_futurista"""
    material = "PencilScribble:layeredShader3"
    grupo = "ciudad_futurista"
    toon_shape = "PencilScribble:pfxToonShape1"

    # Asignar material
    if cmds.objExists(material) and cmds.objExists(grupo):
        cmds.select(grupo, r=True)
        cmds.hyperShade(assign=material)
        print(f"✅ Material {material} asignado a {grupo}")
    else:
        cmds.warning("⚠️ No existe el material o el grupo en la escena")

    # Asignar Toon outline
    if cmds.objExists(toon_shape) and cmds.objExists(grupo):
        cmds.select(grupo, r=True)
        mel.eval(f"assignPfxToon {toon_shape} 0;")
        print(f"✅ PfxToon {toon_shape} asignado a {grupo}")
    else:
        cmds.warning("⚠️ No existe toon shape o grupo en la escena")


def aplicar_shader_toon_carro():
    """Aplica el material y toon de Pastel al carro y sus ruedas"""
    objetos = [
        "axioma_carro",
        "rueda_trasera_der",
        "rueda_trasera_izq",
        "rueda_delantera_der",
        "rueda_delantera_izq"
    ]

    material = "Pastel:lambert2"
    toon_shape = "Pastel:pfxToonShape1"

    # Asignar material
    if cmds.objExists(material):
        for obj in objetos:
            if cmds.objExists(obj):
                cmds.select(obj, r=True)
                cmds.hyperShade(assign=material)
                print(f"✅ Material {material} asignado a {obj}")
            else:
                cmds.warning(f"⚠️ No existe el objeto {obj}")
    else:
        cmds.warning("⚠️ No existe el material Pastel:lambert2")

    # Asignar Toon outline
    if cmds.objExists(toon_shape):
        for obj in objetos:
            if cmds.objExists(obj):
                cmds.select(obj, r=True)
                mel.eval(f"assignPfxToon {toon_shape} 0;")
                print(f"✅ Toon {toon_shape} asignado a {obj}")
            else:
                cmds.warning(f"⚠️ No existe el objeto {obj}")
    else:
        cmds.warning("⚠️ No existe el toon shape Pastel:pfxToonShape1")


def aplicar_toon():
    """Pipeline completo: aplica shaders y toon a ciudad y carro"""
    aplicar_shader_toon_ciudad()
    aplicar_shader_toon_carro()


# Ejecutar todo
aplicar_toon()
