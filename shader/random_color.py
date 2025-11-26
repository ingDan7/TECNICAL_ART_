import maya.cmds as cmds
import random
import colorsys
from shader.shader import ejecutar_pipeline 
from shader.aplicar_shader import aplicar_toon

import maya.cmds as cmds
import random


# ---------------------------------------------------------
# Asegurar shading group válido para cualquier material
# ---------------------------------------------------------
def get_or_create_shading_group(material):
    sg = cmds.listConnections(material, type="shadingEngine")
    if sg:
        return sg[0]

    # Crear shading group si no existe
    sg_name = material.replace(":", "_") + "SG"
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=sg_name)

    # Conectar shader → SG
    if cmds.attributeQuery("outColor", node=material, exists=True):
        cmds.connectAttr(material + ".outColor", sg + ".surfaceShader", force=True)

    print(f"🔧 Se creó shading group para {material}: {sg}")
    return sg


# ---------------------------------------------------------
# Poner Lambert1 negro (como pediste)
# ---------------------------------------------------------
def poner_lambert_negro():
    material = "lambert1"

    if cmds.objExists(material) and cmds.attributeQuery("color", node=material, exists=True):
        cmds.setAttr(material + ".color", 0, 0, 0, type="double3")
        print("✔ lambert1 ahora es negro.")


# ---------------------------------------------------------
# Aplicar material aleatorio entre los 3 pedidos
# ---------------------------------------------------------
def aplicar_material_random():
    poner_lambert_negro()  # Solo afecta lambert1

    # Lista de materiales válidos
    materiales = [
        "lambert1",
        "PencilScribble:layeredShader3",
        "Pastel:lambert2"
    ]

    # Filtrar solo los que existen
    materiales = [m for m in materiales if cmds.objExists(m)]

    if not materiales:
        cmds.warning("⚠️ Ninguno de los materiales existe en la escena.")
        return

    # Elegir aleatoriamente
    material_elegido = random.choice(materiales)
    print(f"🎲 Material elegido: {material_elegido}")

    # Asegurar SG
    sg = get_or_create_shading_group(material_elegido)

    # Grupos detectados
    grupos = []
    if cmds.objExists("ciudad_futurista"):
        grupos.append("ciudad_futurista")
    if cmds.objExists("carro"):
        grupos.append("carro")

    if not grupos:
        cmds.warning("⚠️ No existen ni 'ciudad_futurista' ni 'carro'.")
        return

    # Nunca permitir solo carro
    if grupos == ["carro"] and cmds.objExists("ciudad_futurista"):
        grupos.append("ciudad_futurista")

    # Si existen ambos, puede elegir aplicar a ciudad o ambos
    if "ciudad_futurista" in grupos and "carro" in grupos:
        opcion = random.choice(["ciudad_futurista", "ambos"])
    else:
        opcion = "ciudad_futurista"

    # Aplicación
    if opcion in ["ciudad_futurista", "ambos"]:
        cmds.sets("ciudad_futurista", e=True, forceElement=sg)
        print("🟦 Material aplicado a ciudad_futurista")

    if opcion == "ambos":
        cmds.sets("carro", e=True, forceElement=sg)
        print("🟦 Material aplicado también a carro (ambos)")


def randomizar_rampa_y_toon():
    ramp = "Pastel:rampShader1"
    pastel_toon = "Pastel:pfxToonShape1"
    pencil_toon = "PencilScribble:pfxToonShape1"

    if not cmds.objExists(ramp) or not cmds.objExists(pastel_toon) or not cmds.objExists(pencil_toon):
        cmds.warning("⚠️ No existe alguno de los nodos ramp o toon en la escena")
        return

    # -------------------------------
    # 1. Randomizar rampa Pastel
    # -------------------------------
    h = random.random()
    s = random.uniform(0.8, 1.0)
    v = random.uniform(0.6, 0.9)
    fuerte_rgb = colorsys.hsv_to_rgb(h, s, v)

    h_complementario = (h + 0.5) % 1.0
    s_claro = random.uniform(0.2, 0.5)
    v_claro = random.uniform(0.8, 1.0)
    claro_rgb = colorsys.hsv_to_rgb(h_complementario, s_claro, v_claro)

    puente1_rgb = tuple((f + c) / 2.0 for f, c in zip(fuerte_rgb, claro_rgb))
    puente2_rgb = tuple((f*0.7 + c*0.3) for f, c in zip(fuerte_rgb, claro_rgb))

    ambos_fuertes = random.choice([True, False])

    if ambos_fuertes:
        fuerte2_rgb = colorsys.hsv_to_rgb(h_complementario, s, v)
        cmds.setAttr(f"{ramp}.color[1].color_Color", *fuerte_rgb, type="double3")
        cmds.setAttr(f"{ramp}.color[3].color_Color", *fuerte2_rgb, type="double3")
        cmds.setAttr(f"{ramp}.color[0].color_Color", *puente1_rgb, type="double3")
        cmds.setAttr(f"{ramp}.color[2].color_Color", *puente2_rgb, type="double3")
        print("🎨 Rampa: ambos extremos fuertes (color[1] y color[3])")
    else:
        if random.choice([True, False]):
            cmds.setAttr(f"{ramp}.color[1].color_Color", *fuerte_rgb, type="double3")
            cmds.setAttr(f"{ramp}.color[3].color_Color", *claro_rgb, type="double3")
            cmds.setAttr(f"{ramp}.color[0].color_Color", *puente1_rgb, type="double3")
            cmds.setAttr(f"{ramp}.color[2].color_Color", *puente2_rgb, type="double3")
            print("🎨 Rampa: fuerte en [1], claro en [3]")
        else:
            cmds.setAttr(f"{ramp}.color[3].color_Color", *fuerte_rgb, type="double3")
            cmds.setAttr(f"{ramp}.color[1].color_Color", *claro_rgb, type="double3")
            cmds.setAttr(f"{ramp}.color[0].color_Color", *puente1_rgb, type="double3")
            cmds.setAttr(f"{ramp}.color[2].color_Color", *puente2_rgb, type="double3")
            print("🎨 Rampa: fuerte en [3], claro en [1]")

    # -------------------------------
    # 2. Toon Pastel basado en color fuerte
    # -------------------------------
    profile_width = random.uniform(0.8, 3.0)
    crease_width = random.uniform(0.45, 2.0)
    cmds.setAttr(f"{pastel_toon}.profileLineWidth", profile_width)
    cmds.setAttr(f"{pastel_toon}.creaseLineWidth", crease_width)

    if ambos_fuertes:
        ref_rgb = fuerte_rgb
        ref_h = h
        print("🔥 Toon Pastel: usando color[1] como referencia (ambos fuertes)")
    else:
        ref_rgb = fuerte_rgb
        ref_h = h
        print("🎨 Toon Pastel: usando color fuerte de rampa como referencia")

    cmds.setAttr(f"{pastel_toon}.profileColor", *ref_rgb, type="double3")

    h_comp = (ref_h + 0.5) % 1.0
    crease_rgb = colorsys.hsv_to_rgb(h_comp, random.uniform(0.7, 1.0), random.uniform(0.6, 1.0))
    cmds.setAttr(f"{pastel_toon}.creaseColor", *crease_rgb, type="double3")

    print("✅ Toon Pastel randomizado:")
    print(f"  profileLineWidth: {profile_width}")
    print(f"  creaseLineWidth: {crease_width}")
    print(f"  profileColor: {ref_rgb}")
    print(f"  creaseColor (complementario): {crease_rgb}")

    # -------------------------------
    # 3. Toon PencilScribble en esquema cuadrado
    # -------------------------------
    # Usamos el mismo hue base de la rampa para generar el esquema cuadrado
    hues = [h, (h + 0.25) % 1.0, (h + 0.5) % 1.0, (h + 0.75) % 1.0]
    colores_square = [colorsys.hsv_to_rgb(hh, s, v) for hh in hues]

    profile_rgb_pencil = colores_square[0]   # base
    crease_rgb_pencil = colores_square[1]    # +90°

    cmds.setAttr(f"{pencil_toon}.profileColor", *profile_rgb_pencil, type="double3")
    cmds.setAttr(f"{pencil_toon}.creaseColor", *crease_rgb_pencil, type="double3")
    aplicar_material_random()

    print("✅ Toon PencilScribble randomizado (esquema cuadrado):")
    print(f"  profileColor: {profile_rgb_pencil}")
    print(f"  creaseColor: {crease_rgb_pencil}")
    print(f"  Otros colores del esquema: {colores_square[2]}, {colores_square[3]}")

# Ejecutar
randomizar_rampa_y_toon()

def importar_aplicar_randomizar():
    # 1. Si no están importados los toons → importar
    if not cmds.objExists("Pastel:pfxToonShape1") or not cmds.objExists("PencilScribble:pfxToonShape1"):
        ejecutar_pipeline()
        print("📥 Toons importados")

    # 2. Si están importados pero no aplicados → aplicar materiales y outline
    # (puedes verificar si el objeto tiene shading group asignado)
    if not cmds.listConnections("axioma_carro", type="shadingEngine"):
        aplicar_toon()
        print("🎨 Toon aplicado")

    # 3. Si ya están aplicados → randomizar colores
    randomizar_rampa_y_toon()
    print("🎲 Colores randomizados")

