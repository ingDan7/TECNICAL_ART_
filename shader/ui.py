# ui.py
import maya.cmds as cmds
from shader.shader import limpiar_toons 
from shader.random_color import randomizar_rampa_y_toon, importar_aplicar_randomizar
from shader.configura_render import crear_camera, ejecutar_render, guardar_render
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
            command=lambda *args: importar_aplicar_randomizar()
        )

        cmds.button(
            label="Randomizar colores",
            height=35,
            command=lambda *args: randomizar_rampa_y_toon()
        )

        cmds.button(
            label="Crear Cámara",
            height=35,
            command=lambda *args: crear_camera("axioma_carro")
        )

        cmds.button(
            label="Renderizar Escena",
            height=35,
            command=lambda *args: ejecutar_render()
        )

        cmds.button(
            label="Guardar Render en Escritorio :D",
            height=35,
            command=lambda *args: guardar_render("render_toon")
        )

        cmds.separator(height=10, style="in")

        cmds.button(
            label="Limpiar Toons",
            height=35,
            command=lambda *args: limpiar_toons()
        )

        cmds.button(
            label="Cerrar",
            height=25,
            command=lambda *args: cmds.deleteUI(self.window_name)
        )

        cmds.setParent("..")
        cmds.showWindow(self.window_name)
