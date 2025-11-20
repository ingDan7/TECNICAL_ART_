# ui.py
import maya.cmds as cmds
from shader.shader import ejecutar_pipeline 
from shader.aplicar_shader import aplicar_toon

class ToonUI:
    def __init__(self):
        self.window_name = "toonUI"

    def show(self):
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)

        cmds.window(self.window_name, title="Toon Pastel y PencilScribble", sizeable=False)
        cmds.columnLayout(adj=True, rowSpacing=10, columnAlign="center")

        cmds.text(label="Herramientas Toon", height=25)

        # Botón para importar y limpiar los Toons
        cmds.button(
            label="Importar Toons",
            height=35,
            command=lambda *args: ejecutar_pipeline()
        )

        # Botón para aplicar materiales y outline Toon
        cmds.button(
            label="Aplicar Toon",
            height=35,
            command=lambda *args: aplicar_toon()
        )

        cmds.separator(height=10, style="in")

        cmds.button(
            label="Cerrar",
            height=25,
            command=lambda *args: cmds.deleteUI(self.window_name)
        )

        cmds.setParent("..")
        cmds.showWindow(self.window_name)
