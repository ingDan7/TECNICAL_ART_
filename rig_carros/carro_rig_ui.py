# # # import maya.cmds as cmds
# # # from carro_rig_core import crear_rig_carro

# # # def ventana_rig_carro():
# # #     """Interfaz para crear el rig del carro."""
# # #     if cmds.window("winRigCarro", exists=True):
# # #         cmds.deleteUI("winRigCarro")

# # #     win = cmds.window("winRigCarro", title="Rig del Carro", widthHeight=(320, 180))
# # #     cmds.columnLayout(adj=True, rowSpacing=12)
# # #     cmds.text(label="🚗 Creador de Rig para Carro", align="center", height=30)
# # #     cmds.separator(h=10, style="in")

# # #     cmds.text(label="El script buscará automáticamente:\n'chasis_carro' y las ruedas:", align="center")
# # #     cmds.text(label="- rueda_delantera_izq\n- rueda_delantera_der\n- rueda_trasera_izq\n- rueda_trasera_der", align="center")

# # #     cmds.separator(h=10, style="in")
# # #     cmds.button(label="🛠️ Crear Rig del Carro", bgc=(0.3, 0.6, 0.3), height=40, c=crear_rig_carro)
# # #     cmds.separator(h=10, style="none")
# # #     cmds.button(label="Cerrar", c=lambda *_: cmds.deleteUI(win))

# # #     cmds.showWindow(win)

# # # # Ejecutar interfaz
# # # if __name__ == "__main__":
# # #     ventana_rig_carro()


# # import maya.cmds as cmds
# # from carro_rig_core import crear_rig_carro, ajustar_rig_existente, limpiar_rig_existente
# # from carro_rig_utils import buscar_objetos_escena

# # def verificar_objetos_escena():
# #     """Verifica y muestra los objetos encontrados en escena."""
# #     chasis, ruedas = buscar_objetos_escena()
    
# #     mensaje = "🔍 OBJETOS ENCONTRADOS:\n\n"
    
# #     if chasis:
# #         mensaje += f"✅ CHASIS: {chasis}\n"
# #     else:
# #         mensaje += "❌ CHASIS: No encontrado\n"
    
# #     mensaje += f"✅ RUEDAS: {len(ruedas)} encontradas\n"
# #     for rueda in ruedas:
# #         mensaje += f"   - {rueda}\n"
    
# #     if len(ruedas) < 4:
# #         mensaje += f"\n⚠️ Se recomiendan 4 ruedas (encontradas: {len(ruedas)})"
    
# #     cmds.confirmDialog(title="Verificación de Escena", message=mensaje, button=["OK"])

# # def ventana_rig_carro():
# #     """Interfaz completa para controlar el rig del carro."""
# #     if cmds.window("winRigCarro", exists=True):
# #         cmds.deleteUI("winRigCarro")

# #     win = cmds.window("winRigCarro", title="🚗 Control de Rig - Carro", widthHeight=(400, 450))
# #     main_layout = cmds.columnLayout(adj=True, rowSpacing=10)
    
# #     # Título
# #     cmds.text(label="SISTEMA DE RIG PARA CARRO", font="boldLabelFont", height=30)
# #     cmds.separator(h=10, style="in")
    
# #     # Panel de información
# #     cmds.text(label="FUNCIONALIDADES AUTOMÁTICAS:", align="left", height=20)
# #     cmds.text(label="- Busca chasis y ruedas automáticamente", align="left")
# #     cmds.text(label="- Se ajusta a diferentes proporciones", align="left") 
# #     cmds.text(label="- Regenera y actualiza el rig", align="left")
    
# #     cmds.separator(h=15, style="in")
    
# #     # BOTÓN PRINCIPAL - GENERAR/REGENERAR RIG
# #     cmds.button(
# #         label="🛠️ GENERAR / ACTUALIZAR RIG", 
# #         bgc=(0.2, 0.7, 0.3),
# #         height=50,
# #         command=crear_rig_carro,
# #         annotation="Crea nuevo rig o regenera el existente ajustándose al carro actual"
# #     )
    
# #     cmds.separator(h=10)
    
# #     # BOTÓN AJUSTAR RIG EXISTENTE
# #     cmds.button(
# #         label="🎯 AJUSTAR RIG ACTUAL", 
# #         bgc=(0.3, 0.5, 0.8),
# #         height=40,
# #         command=ajustar_rig_existente,
# #         annotation="Ajusta el rig existente a la geometría actual sin recrearlo"
# #     )
    
# #     cmds.separator(h=5)
    
# #     # BOTÓN VERIFICAR OBJETOS
# #     cmds.button(
# #         label="🔍 VERIFICAR OBJETOS EN ESCENA", 
# #         bgc=(0.2, 0.6, 0.8),
# #         height=35,
# #         command=verificar_objetos_escena,
# #         annotation="Muestra qué objetos encuentra automáticamente"
# #     )
    
# #     cmds.separator(h=10, style="in")
    
# #     # BOTÓN LIMPIAR RIG
# #     cmds.button(
# #         label="🧹 LIMPIAR RIG ANTERIOR", 
# #         bgc=(0.8, 0.4, 0.3),
# #         height=35,
# #         command=lambda *_: limpiar_rig_existente(),
# #         annotation="Elimina completamente el rig existente"
# #     )
    
# #     cmds.separator(h=15, style="in")
    
# #     # Información de uso
# #     cmds.text(label="INSTRUCCIONES RÁPIDAS:", align="left", height=20)
# #     cmds.text(label="1. Usa 'GENERAR' para crear rig nuevo", align="left")
# #     cmds.text(label="2. Modifica tu carro (escala, posición)", align="left")
# #     cmds.text(label="3. Usa 'AJUSTAR' para actualizar el rig", align="left")
# #     cmds.text(label="4. Usa 'LIMPIAR' para empezar de nuevo", align="left")
    
# #     cmds.separator(h=10, style="none")
# #     cmds.button(label="CERRAR", bgc=(0.4, 0.4, 0.4), command=lambda *_: cmds.deleteUI(win))

# #     cmds.showWindow(win)

# # # Ejecutar interfaz
# # if __name__ == "__main__":
# #     ventana_rig_carro()

# import maya.cmds as cmds
# from carro_rig_core import crear_rig_carro, ajustar_rig_existente, limpiar_rig_existente
# from carro_rig_utils import buscar_objetos_escena

# def verificar_objetos_escena():
#     """Verifica y muestra los objetos encontrados en escena."""
#     chasis, ruedas = buscar_objetos_escena()
    
#     mensaje = "🔍 OBJETOS ENCONTRADOS:\n\n"
    
#     if chasis:
#         mensaje += f"✅ CHASIS: {chasis}\n"
#     else:
#         mensaje += "❌ CHASIS: No encontrado\n"
    
#     mensaje += f"✅ RUEDAS: {len(ruedas)} encontradas\n"
#     for rueda in ruedas:
#         mensaje += f"   - {rueda}\n"
    
#     if len(ruedas) < 4:
#         mensaje += f"\n⚠️ Se recomiendan 4 ruedas (encontradas: {len(ruedas)})"
    
#     cmds.confirmDialog(title="Verificación de Escena", message=mensaje, button=["OK"])

# def ventana_rig_carro():
#     """Interfaz completa para controlar el rig del carro."""
#     if cmds.window("winRigCarro", exists=True):
#         cmds.deleteUI("winRigCarro")

#     win = cmds.window("winRigCarro", title="🚗 Control de Rig - Carro", widthHeight=(400, 450))
#     main_layout = cmds.columnLayout(adj=True, rowSpacing=10)
    
#     # Título
#     cmds.text(label="SISTEMA DE RIG PARA CARRO", font="boldLabelFont", height=30)
#     cmds.separator(h=10, style="in")
    
#     # Panel de información
#     cmds.text(label="FUNCIONALIDADES AUTOMÁTICAS:", align="left", height=20)
#     cmds.text(label="- Busca chasis y ruedas automáticamente", align="left")
#     cmds.text(label="- Se ajusta a diferentes proporciones", align="left") 
#     cmds.text(label="- Regenera y actualiza el rig", align="left")
    
#     cmds.separator(h=15, style="in")
    
#     # BOTÓN PRINCIPAL - GENERAR/REGENERAR RIG
#     cmds.button(
#         label="🛠️ GENERAR / ACTUALIZAR RIG", 
#         bgc=(0.2, 0.7, 0.3),
#         height=50,
#         command=crear_rig_carro,
#         annotation="Crea nuevo rig o regenera el existente ajustándose al carro actual"
#     )
    
#     cmds.separator(h=10)
    
#     # BOTÓN AJUSTAR RIG EXISTENTE
#     cmds.button(
#         label="🎯 AJUSTAR RIG ACTUAL", 
#         bgc=(0.3, 0.5, 0.8),
#         height=40,
#         command=ajustar_rig_existente,
#         annotation="Ajusta el rig existente a la geometría actual sin recrearlo"
#     )
    
#     cmds.separator(h=5)
    
#     # BOTÓN VERIFICAR OBJETOS
#     cmds.button(
#         label="🔍 VERIFICAR OBJETOS EN ESCENA", 
#         bgc=(0.2, 0.6, 0.8),
#         height=35,
#         command=verificar_objetos_escena,
#         annotation="Muestra qué objetos encuentra automáticamente"
#     )
    
#     cmds.separator(h=10, style="in")
    
#     # BOTÓN LIMPIAR RIG
#     cmds.button(
#         label="🧹 LIMPIAR RIG ANTERIOR", 
#         bgc=(0.8, 0.4, 0.3),
#         height=35,
#         command=lambda *_: limpiar_rig_existente(),
#         annotation="Elimina completamente el rig existente"
#     )
    
#     cmds.separator(h=15, style="in")
    
#     # Información de uso
#     cmds.text(label="INSTRUCCIONES RÁPIDAS:", align="left", height=20)
#     cmds.text(label="1. Usa 'GENERAR' para crear rig nuevo", align="left")
#     cmds.text(label="2. Modifica tu carro (escala, posición)", align="left")
#     cmds.text(label="3. Usa 'AJUSTAR' para actualizar el rig", align="left")
#     cmds.text(label="4. Usa 'LIMPIAR' para empezar de nuevo", align="left")
    
#     cmds.separator(h=10, style="none")
#     cmds.button(label="CERRAR", bgc=(0.4, 0.4, 0.4), command=lambda *_: cmds.deleteUI(win))

#     cmds.showWindow(win)

# # Ejecutar interfaz
# if __name__ == "__main__":
#     ventana_rig_carro()


import maya.cmds as cmds
from carro_rig_core import crear_rig_carro, ajustar_rig_existente, limpiar_rig_existente
from carro_rig_utils import buscar_objetos_escena

def verificar_objetos_escena():
    """Verifica y muestra los objetos encontrados en escena."""
    chasis, ruedas = buscar_objetos_escena()
    
    mensaje = "🔍 OBJETOS ENCONTRADOS:\n\n"
    
    if chasis:
        mensaje += f"✅ CHASIS: {chasis}\n"
    else:
        mensaje += "❌ CHASIS: No encontrado\n"
    
    mensaje += f"✅ RUEDAS: {len(ruedas)} encontradas\n"
    for rueda in ruedas:
        mensaje += f"   - {rueda}\n"
    
    if len(ruedas) < 4:
        mensaje += f"\n⚠️ Se recomiendan 4 ruedas (encontradas: {len(ruedas)})"
    
    cmds.confirmDialog(title="Verificación de Escena", message=mensaje, button=["OK"])

def ventana_rig_carro():
    """Interfaz SIMPLIFICADA con solo los botones esenciales."""
    if cmds.window("winRigCarro", exists=True):
        cmds.deleteUI("winRigCarro")

    win = cmds.window("winRigCarro", title="🚗 Rig de Carro - Simple", widthHeight=(350, 200))
    main_layout = cmds.columnLayout(adj=True, rowSpacing=15)
    
    # Título
    cmds.text(label="CONTROL DE RIG PARA CARRO", font="boldLabelFont", height=30)
    cmds.separator(h=10, style="in")
    
    # Información básica
    cmds.text(label="Sistema automático que busca:", align="center")
    cmds.text(label="- chasis_carro", align="center")
    cmds.text(label="- 4 ruedas", align="center")
    
    cmds.separator(h=15, style="in")
    
    # BOTÓN ESENCIAL 1 - CREAR RIG
    cmds.button(
        label="🛠️ CREAR RIG", 
        bgc=(0.3, 0.7, 0.3),
        height=50,
        command=crear_rig_carro,
        annotation="Crea el rig completo automáticamente"
    )
    
    cmds.separator(h=10)
    
    # BOTÓN ESENCIAL 2 - LIMPIAR RIG
    cmds.button(
        label="🧹 LIMPIAR RIG", 
        bgc=(0.8, 0.3, 0.3),
        height=40,
        command=lambda *_: limpiar_rig_existente(),
        annotation="Elimina todo el rig de la escena"
    )
    
    cmds.separator(h=10, style="in")
    
    # Botones adicionales (opcionales)
    cmds.button(
        label="🔍 VER OBJETOS", 
        bgc=(0.2, 0.5, 0.8),
        height=30,
        command=verificar_objetos_escena
    )
    
    cmds.separator(h=5)
    
    cmds.button(
        label="🎯 AJUSTAR RIG", 
        bgc=(0.8, 0.6, 0.2),
        height=30,
        command=ajustar_rig_existente
    )
    
    cmds.separator(h=10, style="none")
    cmds.button(label="CERRAR", command=lambda *_: cmds.deleteUI(win))

    cmds.showWindow(win)

# Ejecutar interfaz
if __name__ == "__main__":
    ventana_rig_carro()