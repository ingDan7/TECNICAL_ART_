# ============================================================
# 🏙️ CIUDAD EMERGENTE v11 - MÓDULO DE LÓGICA
# ------------------------------------------------------------
# 🔹 Número aleatorio de edificios (3–15)
# 🔹 Área reducida (ciudad compacta)
# 🔹 Escala aleatoria en X/Z entre (1–4)
# 🔹 Emerge = recrear ciudad limpia (sin acumulaciones)
# ============================================================

import maya.cmds as cmds
import random

# ------------------------------------------------------------
# FUNCIONES BASE
# ------------------------------------------------------------

def _aabb_overlap(center1, ext1, center2, ext2):
    """Verifica si dos cajas AABB se superponen en XZ."""
    dx = abs(center1[0] - center2[0])
    dz = abs(center1[1] - center2[1])
    return (dx <= (ext1[0] + ext2[0])) and (dz <= (ext1[1] + ext2[1]))


def generar_ciudad(min_buildings=3, max_buildings=10):
    """Genera una nueva ciudad procedural limpia."""
    # Si existe una ciudad anterior, eliminarla completamente
    if cmds.objExists("ciudad_procedural_grp"):
        cmds.delete("ciudad_procedural_grp")
    cmds.flushUndo()

    num_buildings = random.randint(min_buildings, max_buildings)

    # 🔹 Área reducida (más compacta)
    area_size = 2.0 + (num_buildings * 0.6)
    print(f"🏗️ Generando {num_buildings} edificios en área {area_size:.1f}...")

    group_name = cmds.group(empty=True, name="ciudad_procedural_grp")
    placed = []

    for i in range(num_buildings):
        placed_ok = False
        attempts = 0

        while not placed_ok and attempts < 100:
            attempts += 1
            # 🔹 Escala aleatoria en X/Z (ancho y profundidad)
            w = random.uniform(2.0, 4.0)
            d = random.uniform(1.5, 4.0)
            # 🔹 Altura independiente
            h = random.uniform(5.0, 14.0)
            # Posición aleatoria en el plano XZ
            x = random.uniform(-area_size, area_size)
            z = random.uniform(-area_size, area_size)

            halfW, halfD = w / 2.0, d / 2.0
            safeW, safeD = halfW * 1.05 + 0.05, halfD * 1.05 + 0.05

            collides = any(_aabb_overlap((x, z), (safeW, safeD), p['center'], p['ext']) for p in placed)
            if collides:
                continue

            placed_ok = True

            # Crear edificio base con subdivisiones en height (2)
            name = cmds.polyCube(w=w, h=h, d=d, sx=1, sy=2, sz=1, name=f"bld_{i:02d}")[0]
            cmds.move(x, h/2.0, z, name, absolute=True)

            # Escalar cara superior o base
            modo = random.choice(["top_scale", "base_scale", "none"])
            if modo == "top_scale":
                cmds.select(f"{name}.f[2]")
                factor = random.uniform(1.1, 1.6)
                cmds.scale(factor, 1, factor, relative=True, pivot=(x, h, z))
            elif modo == "base_scale":
                cmds.select(f"{name}.f[5]")
                factor = random.uniform(0.6, 0.9)
                cmds.scale(factor, 1, factor, relative=True, pivot=(x, 0, z))
            cmds.select(clear=True)

            # Bend controlado
            bend, handle = cmds.nonLinear(name, type='bend', name=f"{name}_bend")
            cmds.setAttr(bend + ".curvature", random.uniform(-50, 50))
            cmds.setAttr(bend + ".lowBound", 0)
            cmds.setAttr(bend + ".highBound", h * 0.5)
            cmds.rotate(0, random.uniform(0, 90), 0, handle)

            # Aplicar deformación y borrar historia
            cmds.delete(name, constructionHistory=True)

            # Guardar datos del edificio
            placed.append({
                'name': name,
                'center': (x, z),
                'ext': (safeW, safeD),
                'dims': (w, h, d)
            })
            cmds.parent(name, group_name)

    cmds.select(clear=True)
    print(f"✅ Ciudad generada con {len(placed)} edificios.")
    return placed


def emerge_ciudad(*_):
    """Borra la ciudad anterior y genera una nueva completamente limpia."""
    print("🌆 Emerge: regenerando ciudad desde cero...")
    generar_ciudad()