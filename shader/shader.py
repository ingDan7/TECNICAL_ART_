import maya.cmds as cmds
import maya.mel as mel
import os

def importar_pencil_scribble():
    """Importa el archivo PencilScribble.ma con namespace PencilScribble"""
    maya_location = os.getenv("MAYA_LOCATION")
    pencil_path = os.path.join(
        maya_location,
        "Examples", "Lighting_And_Rendering", "Toon", "PencilScribble.ma"
    )

    if os.path.exists(pencil_path):
        cmds.file(
            pencil_path,
            i=True,
            type="mayaAscii",
            ignoreVersion=True,
            ra=True,
            namespace="PencilScribble",
            options="v=0;p=17",
            importFrameRate=True,
            importTimeRange="override"
        )
        print(f"✅ Archivo importado: {pencil_path}")
    else:
        cmds.warning(f"No se encontró el archivo Toon PencilScribble en: {pencil_path}")


def importar_y_limpiar_teapot():
    """Importa el archivo Pastel.ma y elimina los primeros CV de la curva teapot"""
    maya_location = os.getenv("MAYA_LOCATION")
    pastel_path = os.path.join(
        maya_location,
        "Examples", "Lighting_And_Rendering", "Toon", "Pastel.ma"
    )

    if os.path.exists(pastel_path):
        cmds.file(
            pastel_path,
            i=True,
            type="mayaAscii",
            ignoreVersion=True,
            ra=True,
            namespace="Pastel",
            importFrameRate=True,
            importTimeRange="override"
        )
        print(f"✅ Archivo importado: {pastel_path}")
    else:
        cmds.warning(f"No se encontró el archivo Toon Pastel en: {pastel_path}")
        return

    node = "Pastel:curveTeapot"
    if cmds.objExists(node):
        cmds.select(node, r=True)
        behaviour = cmds.optionVar(q="toggleVisibilityAndKeepSelectionBehaviour")
        mel.eval(f"toggleVisibilityAndKeepSelection {behaviour};")
        mel.eval(f"hilite {node};")
        cmds.select(f"{node}.cv[0:3]", r=True)
        cmds.delete()
        print(f"✅ CV eliminados de {node}")
    else:
        cmds.warning(f"No se encontró el nodo {node}")


def limpiar_y_agrupar():
    """Elimina nodos innecesarios y agrupa los relevantes en 'Toon'"""
    nodos_eliminar = [
        "Pastel:teapot1MeshGroup",
        "Pastel:pointLight1",
        "Pastel:curveTeapot",
        "PencilScribble:pPlane1",
        "PencilScribble:pCylinder1",
        "PencilScribble:nurbsCylinder2",
        "PencilScribble:nurbsCylinder1",
        "PencilScribble:revolvedSurface2",
        "PencilScribble:revolvedSurface1",
        "PencilScribble:polySurface2",
        "PencilScribble:nurbsToPoly4"
    ]

    nodos_agrupar = [
        "Pastel:place3dTexture2",
        "Pastel:pfxToon1",
        "Pastel:strokeTeapot1",
        "Pastel:_UNKNOWN_REF_NODE_fosterParent1",
        "PencilScribble:pfxToon1",
        "PencilScribble:nurbsPlane1",
        "PencilScribble:directionalLight1"
    ]

    eliminados, agrupados = [], []

    # Eliminar nodos
    for nodo in nodos_eliminar:
        if cmds.objExists(nodo):
            try:
                cmds.delete(nodo)
                eliminados.append(nodo)
                print(f"🔥 Nodo eliminado: {nodo}")
            except Exception as e:
                cmds.warning(f"❌ Error al eliminar {nodo}: {e}")
        else:
            print(f"⚠️ Nodo no encontrado (no se elimina): {nodo}")

    # Crear grupo Toon si no existe
    if not cmds.objExists("Toon"):
        cmds.group(empty=True, name="Toon")
        print("📦 Grupo 'Toon' creado")

    # Agrupar nodos
    for nodo in nodos_agrupar:
        if cmds.objExists(nodo):
            try:
                cmds.parent(nodo, "Toon")
                agrupados.append(nodo)
                print(f"✅ Nodo agrupado en 'Toon': {nodo}")
            except Exception as e:
                cmds.warning(f"❌ No se pudo agrupar {nodo}: {e}")
        else:
            print(f"⚠️ Nodo no encontrado (no se agrupa): {nodo}")

    print("\n🎨 Proceso terminado.")
    print("🔥 Nodos eliminados:", eliminados)
    print("📦 Nodos agrupados en 'Toon':", agrupados)


def ejecutar_pipeline():
    """Pipeline completo: importar PencilScribble, importar/limpiar Pastel, y limpiar/agrupar"""
    importar_pencil_scribble()
    importar_y_limpiar_teapot()
    limpiar_y_agrupar()
