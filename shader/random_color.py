import maya.cmds as cmds
import random
import colorsys

def randomizar_rampa_con_orden():
    ramp = "Pastel:rampShader1"

    if not cmds.objExists(ramp):
        cmds.warning(f"⚠️ No existe el nodo {ramp}")
        return

    # 1. Generar color fuerte aleatorio (HSV)
    h = random.random()
    s = random.uniform(0.8, 1.0)   # saturación alta
    v = random.uniform(0.6, 0.9)   # brillo medio-alto
    fuerte_rgb = colorsys.hsv_to_rgb(h, s, v)

    # 2. Generar color complementario claro
    h_complementario = (h + 0.5) % 1.0
    s_claro = random.uniform(0.2, 0.5)  # saturación baja
    v_claro = random.uniform(0.8, 1.0)  # brillo alto
    claro_rgb = colorsys.hsv_to_rgb(h_complementario, s_claro, v_claro)

    # 3. Colores puente
    puente1_rgb = tuple((f + c) / 2.0 for f, c in zip(fuerte_rgb, claro_rgb))
    puente2_rgb = tuple((f*0.7 + c*0.3) for f, c in zip(fuerte_rgb, claro_rgb))

    # 4. Decidir orden aleatorio
    if random.choice([True, False]):
        # Caso A: fuerte en color[1], claro en color[3]
        cmds.setAttr(f"{ramp}.color[1].color_Color", *fuerte_rgb, type="double3")
        cmds.setAttr(f"{ramp}.color[0].color_Color", *puente1_rgb, type="double3")
        cmds.setAttr(f"{ramp}.color[2].color_Color", *puente2_rgb, type="double3")
        cmds.setAttr(f"{ramp}.color[3].color_Color", *claro_rgb, type="double3")
        print("🎨 Orden: fuerte en [1], claro en [3]")
    else:
        # Caso B: fuerte en color[3], claro en color[1]
        cmds.setAttr(f"{ramp}.color[3].color_Color", *fuerte_rgb, type="double3")
        cmds.setAttr(f"{ramp}.color[0].color_Color", *puente1_rgb, type="double3")
        cmds.setAttr(f"{ramp}.color[2].color_Color", *puente2_rgb, type="double3")
        cmds.setAttr(f"{ramp}.color[1].color_Color", *claro_rgb, type="double3")
        print("🎨 Orden: fuerte en [3], claro en [1]")

    print(f"  Fuerte: {fuerte_rgb}")
    print(f"  Claro:  {claro_rgb}")
    print(f"  Puente1: {puente1_rgb}")
    print(f"  Puente2: {puente2_rgb}")

# Ejecutar
randomizar_rampa_con_orden()


import maya.cmds as cmds
import random
import colorsys

def randomizar_toon():
    toon_shape = "Pastel:pfxToonShape1"

    if not cmds.objExists(toon_shape):
        cmds.warning(f"⚠️ No existe el nodo {toon_shape}")
        return

    # 1. Randomizar grosores
    profile_width = random.uniform(0.8, 3.0)
    crease_width = random.uniform(0.45, 2.0)

    cmds.setAttr(f"{toon_shape}.profileLineWidth", profile_width)
    cmds.setAttr(f"{toon_shape}.creaseLineWidth", crease_width)

    # 2. Generar color base en HSV
    h = random.random()
    s = random.uniform(0.7, 1.0)
    v = random.uniform(0.6, 1.0)
    base_rgb = colorsys.hsv_to_rgb(h, s, v)

    # 3. Decidir si el segundo color será análogo o complementario
    if random.choice([True, False]):
        # Análogo: hue desplazado ligeramente
        h2 = (h + random.uniform(0.05, 0.15)) % 1.0
        mode = "🎨 Análogos"
    else:
        # Complementario: hue opuesto
        h2 = (h + 0.5) % 1.0
        mode = "🎨 Complementarios"

    s2 = random.uniform(0.6, 1.0)
    v2 = random.uniform(0.6, 1.0)
    second_rgb = colorsys.hsv_to_rgb(h2, s2, v2)

    # 4. Asignar colores (asegurando que no sean idénticos)
    if base_rgb == second_rgb:
        second_rgb = tuple(min(1.0, c + 0.1) for c in second_rgb)

    cmds.setAttr(f"{toon_shape}.profileColor", *base_rgb, type="double3")
    cmds.setAttr(f"{toon_shape}.creaseColor", *second_rgb, type="double3")

    print("✅ Toon randomizado:")
    print(f"  profileLineWidth: {profile_width}")
    print(f"  creaseLineWidth: {crease_width}")
    print(f"  profileColor: {base_rgb}")
    print(f"  creaseColor: {second_rgb} ({mode})")

# Ejecutar
randomizar_toon()
