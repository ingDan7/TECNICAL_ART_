import maya.cmds as cmds
from .carro_rig_core import crear_rig_carro

def ventana_rig_carro():
    """Interfaz para crear el rig del carro."""
    if cmds.window("winRigCarro", exists=True):
        cmds.deleteUI("winRigCarro")

    win = cmds.window("winRigCarro", title="Rig del Carro", widthHeight=(320, 180))
    cmds.columnLayout(adj=True, rowSpacing=12)
    cmds.text(label="🚗 Creador de Rig para Carro", align="center", height=30)
    cmds.separator(h=10, style="in")

    cmds.text(label="El script buscará automáticamente:\n'chasis_carro' y las ruedas:", align="center")
    cmds.text(label="- rueda_delantera_izq\n- rueda_delantera_der\n- rueda_trasera_izq\n- rueda_trasera_der", align="center")

    cmds.separator(h=10, style="in")
    cmds.button(label="🛠️ Crear Rig del Carro", bgc=(0.3, 0.6, 0.3), height=40, c=crear_rig_carro)
    cmds.separator(h=10, style="none")
    cmds.button(label="Cerrar", c=lambda *_: cmds.deleteUI(win))

    cmds.showWindow(win)

# Ejecutar interfaz
if __name__ == "__main__":
    ventana_rig_carro()