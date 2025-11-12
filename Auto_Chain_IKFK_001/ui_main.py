# # import maya.cmds as cmds
# # from .create_joints import build_chains
# # from .fk_setup import setup_fk_chain
# # from .ik_setup import setup_ik_chain
# # from .orient_constraints import setup_main_chain


# # def cleanup_previous_rig():
# #     objs = [
# #         "upperLeg_practice_L_FK_joint_001","middleLeg_practice_L_FK_joint_001","endLeg_practice_L_FK_joint_001",
# #         "upperLeg_practice_L_IK_joint_002","middleLeg_practice_L_IK_joint_002","endLeg_practice_L_IK_joint_002",
# #         "upperLeg_practice_L_MAIN_joint_003","middleLeg_practice_L_MAIN_joint_003","endLeg_practice_L_MAIN_joint_003",
# #         "middleLeg_practice_L_IKhandle_001","middleLeg_practice_L_effector_001",
# #         "middleLeg_practice_L_IKpoleVector_001","middleLeg_practice_L_IKpoleVectorRoot_001",
# #         "endLeg_practice_L_IKctrl_001","Leg_practice_L_attributes_001","FKIK_reverse"
# #     ]
# #     for o in objs:
# #         if cmds.objExists(o):
# #             cmds.delete(o)


# # _fk_chain = []
# # _ik_chain = []
# # _main_chain = []

# # def show_message(msg, success=True):
# #     """Muestra un mensaje flotante de verificación"""
# #     color = (0.2, 0.8, 0.2) if success else (0.9, 0.5, 0.2)
# #     cmds.inViewMessage(
# #         amg=f"<hl>{msg}</hl>",
# #         pos='midCenter',
# #         fade=True,
# #         fadeStayTime=1500,
# #         backColor=color,
# #         fadeOutTime=1000
# #     )

# # def ui_build_chains(*args):
# #     global _fk_chain, _ik_chain, _main_chain
# #     cleanup_previous_rig()
# #     _fk_chain, _ik_chain, _main_chain = build_chains()
# #     show_message("✅ Cadenas creadas correctamente", success=True)

# # def ui_setup_fk(*args):
# #     if _fk_chain:
# #         setup_fk_chain(_fk_chain)
# #         show_message("✅ FK configurado correctamente", success=True)
# #     else:
# #         show_message("⚠️ Primero crea las cadenas", success=False)

# # def ui_setup_ik(*args):
# #     if _ik_chain:
# #         setup_ik_chain(_ik_chain)
# #         show_message("✅ IK configurado correctamente", success=True)
# #     else:
# #         show_message("⚠️ Primero crea las cadenas", success=False)

# # def ui_setup_main(*args):
# #     if _fk_chain and _ik_chain and _main_chain:
# #         setup_main_chain(_fk_chain, _ik_chain, _main_chain)
# #         show_message("✅ MAIN configurado correctamente", success=True)
# #     else:
# #         show_message("⚠️ Primero crea las cadenas", success=False)

# # def ui_build_all(*args):
# #     cleanup_previous_rig()
# #     fk_chain, ik_chain, main_chain = build_chains()
# #     setup_fk_chain(fk_chain)
# #     setup_ik_chain(ik_chain)
# #     setup_main_chain(fk_chain, ik_chain, main_chain)
# #     show_message("🎉 Rig completo creado con éxito", success=True)


# # def open_leg_rig_ui():
# #     if cmds.window("legRigUI", exists=True):
# #         cmds.deleteUI("legRigUI")

# #     win = cmds.window("legRigUI", title="🦿 Rig Pierna FK/IK - Auto Builder", widthHeight=(400, 350), sizeable=True)
# #     cmds.columnLayout(adjustableColumn=True, rowSpacing=8, columnAlign="center")

# #     cmds.text(label="⚙️  Auto Rig Pierna FK/IK", height=30, align="center", bgc=(0.1, 0.1, 0.1))
# #     cmds.separator(h=8, style="in")

# #     cmds.button(label="🔧 Crear Joints Base", c=ui_build_chains, bgc=(0.1, 0.7, 0.9), height=40)
# #     cmds.button(label="🦴 Configurar Cadena FK", c=ui_setup_fk, bgc=(0.9, 0.4, 0.4), height=40)
# #     cmds.button(label="⚙️ Configurar Cadena IK", c=ui_setup_ik, bgc=(0.4, 0.9, 0.4), height=40)
# #     cmds.button(label="🔗 Configurar Cadena MAIN", c=ui_setup_main, bgc=(0.5, 0.5, 0.9), height=40)

# #     cmds.separator(h=10, style="in")
# #     cmds.button(label="🚀 Crear Todo el Rig (Full Auto)", c=ui_build_all, bgc=(1.0, 0.8, 0.3), height=45)

# #     cmds.separator(h=10, style="in")
# #     cmds.text(label="💡 Tip: Ejecuta paso a paso para depurar errores.", align="center")

# #     cmds.showWindow(win)


# # if __name__ == "__main__":
# #     open_leg_rig_ui()


# import maya.cmds as cmds
# import traceback
# from .create_joints import build_chains
# from .fk_setup import setup_fk_chain
# from .ik_setup import setup_ik_chain
# from .orient_constraints import setup_main_chain

# _fk_chain = []
# _ik_chain = []
# _main_chain = []

# def cleanup_previous_rig():
#     objs = [
#         "upperLeg_practice_L_FK_joint_001","middleLeg_practice_L_FK_joint_001","endLeg_practice_L_FK_joint_001",
#         "upperLeg_practice_L_IK_joint_002","middleLeg_practice_L_IK_joint_002","endLeg_practice_L_IK_joint_002",
#         "upperLeg_practice_L_MAIN_joint_003","middleLeg_practice_L_MAIN_joint_003","endLeg_practice_L_MAIN_joint_003",
#         "middleLeg_practice_L_IKhandle_001","middleLeg_practice_L_effector_001",
#         "middleLeg_practice_L_IKpoleVector_001","middleLeg_practice_L_IKpoleVectorRoot_001",
#         "endLeg_practice_L_IKctrl_001","Leg_practice_L_attributes_001","FKIK_reverse"
#     ]
#     for o in objs:
#         if cmds.objExists(o):
#             cmds.delete(o)

# def show_message(msg, success=True):
#     color = (0.2, 0.8, 0.2) if success else (0.9, 0.5, 0.2)
#     cmds.inViewMessage(amg=f"<hl>{msg}</hl>", pos='midCenter', fade=True, fadeStayTime=1500, backColor=color, fadeOutTime=1000)

# def ui_build_chains(*args):
#     global _fk_chain, _ik_chain, _main_chain
#     cleanup_previous_rig()
#     _fk_chain, _ik_chain, _main_chain = build_chains()
#     show_message("✅ Cadenas creadas correctamente")

# def ui_setup_fk(*args):
#     if _fk_chain:
#         setup_fk_chain(_fk_chain)
#         show_message("✅ FK configurado correctamente")
#     else:
#         show_message("⚠️ Primero crea las cadenas", success=False)

# def ui_setup_ik(*args):
#     if _ik_chain:
#         setup_ik_chain(_ik_chain)
#         show_message("✅ IK configurado correctamente")
#     else:
#         show_message("⚠️ Primero crea las cadenas", success=False)

# def ui_setup_main(*args):
#     if _fk_chain and _ik_chain and _main_chain:
#         setup_main_chain(_fk_chain, _ik_chain, _main_chain)
#         show_message("✅ MAIN configurado correctamente")
#     else:
#         show_message("⚠️ Primero crea las cadenas", success=False)

# def ui_build_all(*args):
#     cleanup_previous_rig()
#     fk_chain, ik_chain, main_chain = build_chains()
#     setup_fk_chain(fk_chain)
#     setup_ik_chain(ik_chain)
#     setup_main_chain(fk_chain, ik_chain, main_chain)
#     show_message("🎉 Rig completo creado con éxito")

# # ---------------------------
# # Embeddable UI
# # ---------------------------
# def build_ui(parent=None):
#     """Versión mejorada que maneja correctamente el parent"""
#     created_window = False
    
#     # Si no hay parent, crear ventana independiente
#     if parent is None:
#         if cmds.window("legRigUI", exists=True):
#             cmds.deleteUI("legRigUI")
#         win = cmds.window("legRigUI", title="🦿 Rig Pierna FK/IK - Auto Builder", w=400, h=350, sizeable=True)
#         main_layout = cmds.columnLayout(adjustableColumn=True)
#         created_window = True
#     else:
#         # Usar el parent proporcionado directamente
#         main_layout = parent

#     # CONTENIDO DE LA UI (sin crear layouts adicionales)
#     cmds.text(label="⚙️  Auto Rig Pierna FK/IK", height=30, align="center", bgc=(0.1, 0.1, 0.1), parent=main_layout)
#     cmds.separator(h=8, style="in", parent=main_layout)

#     cmds.button(label="🔧 Crear Joints Base", c=ui_build_chains, bgc=(0.1, 0.7, 0.9), h=36, parent=main_layout)
#     cmds.button(label="🦴 Configurar Cadena FK", c=ui_setup_fk, bgc=(0.9, 0.4, 0.4), h=36, parent=main_layout)
#     cmds.button(label="⚙️ Configurar Cadena IK", c=ui_setup_ik, bgc=(0.4, 0.9, 0.4), h=36, parent=main_layout)
#     cmds.button(label="🔗 Configurar Cadena MAIN", c=ui_setup_main, bgc=(0.5, 0.5, 0.9), h=36, parent=main_layout)
#     cmds.separator(h=8, style="in", parent=main_layout)
#     cmds.button(label="🚀 Crear Todo el Rig (Full Auto)", c=ui_build_all, bgc=(1.0, 0.8, 0.3), h=40, parent=main_layout)
#     cmds.separator(h=10, style="in", parent=main_layout)
#     cmds.text(label="💡 Tip: Ejecuta paso a paso para depurar errores.", align="center", parent=main_layout)

#     if created_window:
#         cmds.showWindow(win)

# def open_leg_rig_ui():
#     build_ui(parent=None)

# if __name__ == "__main__":
#     open_leg_rig_ui()



# import maya.cmds as cmds
# import traceback
# from .create_joints import build_chains
# from .fk_setup import setup_fk_chain
# from .ik_setup import setup_ik_chain
# from .orient_constraints import setup_main_chain

# _fk_chain = []
# _ik_chain = []
# _main_chain = []

# def cleanup_previous_rig():
#     objs = [
#         "upperLeg_practice_L_FK_joint_001","middleLeg_practice_L_FK_joint_001","endLeg_practice_L_FK_joint_001",
#         "upperLeg_practice_L_IK_joint_002","middleLeg_practice_L_IK_joint_002","endLeg_practice_L_IK_joint_002",
#         "upperLeg_practice_L_MAIN_joint_003","middleLeg_practice_L_MAIN_joint_003","endLeg_practice_L_MAIN_joint_003",
#         "middleLeg_practice_L_IKhandle_001","middleLeg_practice_L_effector_001",
#         "middleLeg_practice_L_IKpoleVector_001","middleLeg_practice_L_IKpoleVectorRoot_001",
#         "endLeg_practice_L_IKctrl_001","Leg_practice_L_attributes_001","FKIK_reverse"
#     ]
#     for o in objs:
#         if cmds.objExists(o):
#             cmds.delete(o)

# def reset_leg_rig_system(*args):
#     """
#     Elimina todos los elementos creados por el sistema de pierna FK/IK
#     pero preserva los joints principales existentes en la escena
#     """
#     try:
#         # Lista de patrones para identificar elementos a eliminar
#         delete_patterns = [
#             # Joints creados por el sistema (con numeración específica)
#             "*_FK_joint_00*",
#             "*_IK_joint_00*", 
#             "*_MAIN_joint_00*",
#             # Controles FK/IK
#             "*_FK_ctrl*",
#             "*_IK_ctrl*",
#             "*_ctrl*",
#             "*_control*",
#             "*_CTRL*",
#             # IK Handles y effeectors
#             "*_IKhandle*",
#             "*_ikHandle*",
#             "*_effector*",
#             # Pole Vectors
#             "*_poleVector*",
#             "*_PV_*",
#             "*_pole_*",
#             # Grupos de organización
#             "*_FK_GRP*",
#             "*_IK_GRP*", 
#             "*_MAIN_GRP*",
#             "*_RIG_GRP*",
#             "*_CONTROLS_GRP*",
#             "*_AUTO_GRP*",
#             "*_ZERO_GRP*",
#             "*_OFFSET_GRP*",
#             # Nodos de utilidad y conexión
#             "*_attributes*",
#             "*_reverse*",
#             "*_condition*",
#             "*_multiplyDivide*",
#             "*_decomposeMatrix*",
#             "*_composeMatrix*",
#             "*_constraint*",
#             "*_pointConstraint*",
#             "*_orientConstraint*",
#             "*_parentConstraint*",
#             "*_aimConstraint*",
#             "*_skinCluster*"
#         ]
        
#         # Elementos específicos por nombre (del cleanup original)
#         specific_elements = [
#             "upperLeg_practice_L_FK_joint_001", "middleLeg_practice_L_FK_joint_001", "endLeg_practice_L_FK_joint_001",
#             "upperLeg_practice_L_IK_joint_002", "middleLeg_practice_L_IK_joint_002", "endLeg_practice_L_IK_joint_002",
#             "upperLeg_practice_L_MAIN_joint_003", "middleLeg_practice_L_MAIN_joint_003", "endLeg_practice_L_MAIN_joint_003",
#             "middleLeg_practice_L_IKhandle_001", "middleLeg_practice_L_effector_001",
#             "middleLeg_practice_L_IKpoleVector_001", "middleLeg_practice_L_IKpoleVectorRoot_001",
#             "endLeg_practice_L_IKctrl_001", "Leg_practice_L_attributes_001", "FKIK_reverse"
#         ]
        
#         deleted_count = 0
        
#         # Eliminar por patrones
#         for pattern in delete_patterns:
#             objects = cmds.ls(pattern, transforms=True, shapes=True, dagObjects=True)
#             for obj in objects:
#                 try:
#                     # Verificar que no sea un joint principal existente
#                     if cmds.objectType(obj, isType="joint"):
#                         # Solo eliminar joints creados por este sistema (con numeración específica)
#                         if any(x in obj for x in ["_FK_joint_", "_IK_joint_", "_MAIN_joint_"]):
#                             cmds.delete(obj)
#                             deleted_count += 1
#                             print(f"🗑️ Eliminado: {obj}")
#                     else:
#                         # Eliminar cualquier otro objeto que no sea joint
#                         cmds.delete(obj)
#                         deleted_count += 1
#                         print(f"🗑️ Eliminado: {obj}")
#                 except Exception as e:
#                     print(f"⚠️ No se pudo eliminar {obj}: {e}")
        
#         # Eliminar elementos específicos
#         for element in specific_elements:
#             if cmds.objExists(element):
#                 try:
#                     cmds.delete(element)
#                     deleted_count += 1
#                     print(f"🗑️ Eliminado: {element}")
#                 except Exception as e:
#                     print(f"⚠️ No se pudo eliminar {element}: {e}")
        
#         # Limpiar referencias en capas de display
#         display_layers = cmds.ls(type="displayLayer")
#         for layer in display_layers:
#             if layer != "defaultLayer":
#                 try:
#                     members = cmds.editDisplayLayerMembers(layer, query=True)
#                     if members:
#                         cmds.editDisplayLayerMembers(layer, remove=True)
#                         print(f"🧹 Limpiada capa: {layer}")
#                 except:
#                     pass
        
#         # Resetear variables globales
#         global _fk_chain, _ik_chain, _main_chain
#         _fk_chain = []
#         _ik_chain = [] 
#         _main_chain = []
        
#         # Mostrar mensaje de confirmación
#         show_message(f"✅ Reset Leg Rig: {deleted_count} elementos eliminados")
#         print(f"🎯 Reset del Leg Rig: {deleted_count} elementos eliminados")
        
#     except Exception as e:
#         show_message(f"⚠️ Error en reset del Leg Rig: {e}", success=False)
#         traceback.print_exc()

# def show_message(msg, success=True):
#     color = (0.2, 0.8, 0.2) if success else (0.9, 0.5, 0.2)
#     cmds.inViewMessage(amg=f"<hl>{msg}</hl>", pos='midCenter', fade=True, fadeStayTime=1500, backColor=color, fadeOutTime=1000)

# def ui_build_chains(*args):
#     global _fk_chain, _ik_chain, _main_chain
#     cleanup_previous_rig()
#     _fk_chain, _ik_chain, _main_chain = build_chains()
#     show_message("✅ Cadenas creadas correctamente")

# def ui_setup_fk(*args):
#     if _fk_chain:
#         setup_fk_chain(_fk_chain)
#         show_message("✅ FK configurado correctamente")
#     else:
#         show_message("⚠️ Primero crea las cadenas", success=False)

# def ui_setup_ik(*args):
#     if _ik_chain:
#         setup_ik_chain(_ik_chain)
#         show_message("✅ IK configurado correctamente")
#     else:
#         show_message("⚠️ Primero crea las cadenas", success=False)

# def ui_setup_main(*args):
#     if _fk_chain and _ik_chain and _main_chain:
#         setup_main_chain(_fk_chain, _ik_chain, _main_chain)
#         show_message("✅ MAIN configurado correctamente")
#     else:
#         show_message("⚠️ Primero crea las cadenas", success=False)

# def ui_build_all(*args):
#     cleanup_previous_rig()
#     fk_chain, ik_chain, main_chain = build_chains()
#     setup_fk_chain(fk_chain)
#     setup_ik_chain(ik_chain)
#     setup_main_chain(fk_chain, ik_chain, main_chain)
#     show_message("🎉 Rig completo creado con éxito")

# # ---------------------------
# # Embeddable UI
# # ---------------------------
# def build_ui(parent=None):
#     """Versión mejorada que maneja correctamente el parent"""
#     created_window = False
    
#     # Si no hay parent, crear ventana independiente
#     if parent is None:
#         if cmds.window("legRigUI", exists=True):
#             cmds.deleteUI("legRigUI")
#         win = cmds.window("legRigUI", title="🦿 Rig Pierna FK/IK - Auto Builder", w=400, h=400, sizeable=True)
#         main_layout = cmds.columnLayout(adjustableColumn=True)
#         created_window = True
#     else:
#         # Usar el parent proporcionado directamente
#         main_layout = parent

#     # CONTENIDO DE LA UI (sin crear layouts adicionales)
#     cmds.text(label="⚙️  Auto Rig Pierna FK/IK", height=30, align="center", bgc=(0.1, 0.1, 0.1), parent=main_layout)
#     cmds.separator(h=8, style="in", parent=main_layout)

#     cmds.button(label="🔧 Crear Joints Base", c=ui_build_chains, bgc=(0.1, 0.7, 0.9), h=36, parent=main_layout)
#     cmds.button(label="🦴 Configurar Cadena FK", c=ui_setup_fk, bgc=(0.9, 0.4, 0.4), h=36, parent=main_layout)
#     cmds.button(label="⚙️ Configurar Cadena IK", c=ui_setup_ik, bgc=(0.4, 0.9, 0.4), h=36, parent=main_layout)
#     cmds.button(label="🔗 Configurar Cadena MAIN", c=ui_setup_main, bgc=(0.5, 0.5, 0.9), h=36, parent=main_layout)
#     cmds.separator(h=8, style="in", parent=main_layout)
#     cmds.button(label="🚀 Crear Todo el Rig (Full Auto)", c=ui_build_all, bgc=(1.0, 0.8, 0.3), h=40, parent=main_layout)
    
#     cmds.separator(h=10, style="in", parent=main_layout)
    
#     # BOTÓN DE RESET COMPLETO
#     cmds.button(label="🔄 RESET COMPLETO - Limpiar Sistema", c=reset_leg_rig_system, 
#                 bgc=(0.9, 0.3, 0.3), h=36, parent=main_layout)
    
#     cmds.separator(h=8, style="in", parent=main_layout)
#     cmds.text(label="⚠️ Reset: Elimina controles, joints del sistema y conexiones\n💡 Preserva joints principales existentes", 
#               align="center", parent=main_layout)
#     cmds.separator(h=10, style="in", parent=main_layout)
#     cmds.text(label="💡 Tip: Ejecuta paso a paso para depurar errores.", align="center", parent=main_layout)

#     if created_window:
#         cmds.showWindow(win)

# def open_leg_rig_ui():
#     build_ui(parent=None)

# if __name__ == "__main__":
#     open_leg_rig_ui()



# import maya.cmds as cmds
# import traceback
# from .create_joints import build_chains
# from .fk_setup import setup_fk_chain
# from .ik_setup import setup_ik_chain
# from .orient_constraints import setup_main_chain

# _fk_chain = []
# _ik_chain = []
# _main_chain = []

# def reset_leg_rig_system(*args):
#     """
#     Elimina TODOS los elementos creados por el sistema de pierna FK/IK
#     Incluyendo joints base, controles, grupos, constraints, etc.
#     Deja la escena completamente limpia
#     """
#     try:
#         # Lista completa de patrones para identificar elementos a eliminar
#         delete_patterns = [
#             # TODOS los joints del sistema (base y derivados)
#             "*_practice_*",
#             "*_FK_joint*",
#             "*_IK_joint*", 
#             "*_MAIN_joint*"
#             # Controles FK/IK
#             "*_FK_ctrl*",
#             "*_IK_ctrl*",
#             "*_ctrl*",
#             "*_control*",
#             "*_CTRL*",
#             "*_auto*",
#             "*_driver*",
#             # IK Handles y effectors
#             "*_IKhandle*",
#             "*_ikHandle*",
#             "*_effector*",
#             "*_ikSpline*",
#             # Pole Vectors
#             "*_poleVector*",
#             "*_PV_*",
#             "*_pole_*",
#             "*_PVctr*",
#             # Grupos de organización
#             "*_FK_GRP*",
#             "*_IK_GRP*", 
#             "*_MAIN_GRP*",
#             "*_RIG_GRP*",
#             "*_CONTROLS_GRP*",
#             "*_AUTO_GRP*",
#             "*_ZERO_GRP*",
#             "*_OFFSET_GRP*",
#             "*_SETUP_GRP*",
#             "*_GEO_GRP*",
#             "*_JOINTS_GRP*",
#             # Nodos de utilidad y conexión
#             "*_attributes*",
#             "*_reverse*",
#             "*_condition*",
#             "*_multiplyDivide*",
#             "*_decomposeMatrix*",
#             "*_composeMatrix*",
#             "*_multMatrix*",
#             "*_plusMinusAverage*",
#             "*_vectorProduct*",
#             # Constraints
#             "*_constraint*",
#             "*_pointConstraint*",
#             "*_orientConstraint*",
#             "*_parentConstraint*",
#             "*_aimConstraint*",
#             "*_scaleConstraint*",
#             "*_geometryConstraint*",
#             # Skin y deformadores
#             "*_skinCluster*",
#             "*_blendShape*",
#             "*_cluster*",
#             "*_nonLinear*",
#             # Curvas y formas
#             "*_curve*",
#             "*_shape*",
#             "*_nurbsCircle*",
#             "*_locator*"
#         ]
        
#         # Elementos específicos por nombre (backup para elementos que no coincidan con patrones)
#         specific_elements = [
#             "upperLeg_practice_L_FK_joint_001", "middleLeg_practice_L_FK_joint_001", "endLeg_practice_L_FK_joint_001",
#             "upperLeg_practice_L_IK_joint_002", "middleLeg_practice_L_IK_joint_002", "endLeg_practice_L_IK_joint_002",
#             "upperLeg_practice_L_MAIN_joint_003", "middleLeg_practice_L_MAIN_joint_003", "endLeg_practice_L_MAIN_joint_003",
#             "middleLeg_practice_L_IKhandle_001", "middleLeg_practice_L_effector_001",
#             "middleLeg_practice_L_IKpoleVector_001", "middleLeg_practice_L_IKpoleVectorRoot_001",
#             "endLeg_practice_L_IKctrl_001", "Leg_practice_L_attributes_001", "FKIK_reverse",
#             # Joints base originales
#             "upperLeg_practice_L_joint", "middleLeg_practice_L_joint", "endLeg_practice_L_joint",
#             "upperLeg_practice_L", "middleLeg_practice_L", "endLeg_practice_L"
#         ]
        
#         deleted_count = 0
        
#         print("🧹 INICIANDO LIMPIEZA COMPLETA DEL SISTEMA...")
        
#         # Estrategia 1: Eliminar por patrones (más agresiva)
#         for pattern in delete_patterns:
#             try:
#                 objects = cmds.ls(pattern, transforms=True, shapes=True, dagObjects=True, exactType=False)
#                 for obj in objects:
#                     try:
#                         # Verificar que el objeto existe y no es parte del sistema por defecto
#                         if cmds.objExists(obj) and not obj.startswith('persp') and not obj.startswith('top') and not obj.startswith('front') and not obj.startswith('side'):
#                             cmds.delete(obj)
#                             deleted_count += 1
#                             print(f"🗑️ Eliminado: {obj}")
#                     except Exception as e:
#                         print(f"⚠️ No se pudo eliminar {obj}: {e}")
#             except Exception as e:
#                 print(f"⚠️ Error con patrón {pattern}: {e}")
        
#         # Estrategia 2: Eliminar elementos específicos
#         for element in specific_elements:
#             if cmds.objExists(element):
#                 try:
#                     cmds.delete(element)
#                     deleted_count += 1
#                     print(f"🗑️ Eliminado específico: {element}")
#                 except Exception as e:
#                     print(f"⚠️ No se pudo eliminar {element}: {e}")
        
#         # Estrategia 3: Buscar y eliminar por nombres que contengan "practice"
#         practice_objects = cmds.ls("*practice*", transforms=True, shapes=True, dagObjects=True)
#         for obj in practice_objects:
#             try:
#                 if cmds.objExists(obj) and not obj.startswith('persp') and not obj.startswith('top') and not obj.startswith('front') and not obj.startswith('side'):
#                     cmds.delete(obj)
#                     deleted_count += 1
#                     print(f"🗑️ Eliminado por 'practice': {obj}")
#             except Exception as e:
#                 print(f"⚠️ No se pudo eliminar {obj}: {e}")
        
#         # Estrategia 4: Limpiar grupos vacíos y capas de display
#         display_layers = cmds.ls(type="displayLayer")
#         for layer in display_layers:
#             if layer != "defaultLayer":
#                 try:
#                     # Verificar si la capa está vacía
#                     members = cmds.editDisplayLayerMembers(layer, query=True)
#                     if not members:
#                         cmds.delete(layer)
#                         print(f"🗑️ Eliminada capa vacía: {layer}")
#                     else:
#                         # Remover miembros y luego eliminar la capa
#                         cmds.editDisplayLayerMembers(layer, remove=True)
#                         cmds.delete(layer)
#                         print(f"🗑️ Eliminada capa: {layer}")
#                 except Exception as e:
#                     print(f"⚠️ No se pudo limpiar capa {layer}: {e}")
        
#         # Estrategia 5: Limpiar sets de selección vacíos
#         selection_sets = cmds.ls(type="objectSet")
#         for obj_set in selection_sets:
#             try:
#                 if obj_set != "defaultObjectSet" and "character" not in obj_set.lower():
#                     members = cmds.sets(obj_set, query=True)
#                     if not members:
#                         cmds.delete(obj_set)
#                         print(f"🗑️ Eliminado set vacío: {obj_set}")
#             except Exception as e:
#                 print(f"⚠️ No se pudo limpiar set {obj_set}: {e}")
        
#         # Resetear variables globales
#         global _fk_chain, _ik_chain, _main_chain
#         _fk_chain = []
#         _ik_chain = [] 
#         _main_chain = []
        
#         # Forzar actualización de la escena
#         cmds.refresh()
        
#         # Mostrar mensaje de confirmación
#         show_message(f"✅ Reset Completo: {deleted_count} elementos eliminados")
#         print(f"🎯 RESET COMPLETO EXITOSO: {deleted_count} elementos eliminados")
#         print("✨ La escena ha quedado completamente limpia")
        
#     except Exception as e:
#         show_message(f"⚠️ Error en reset completo: {e}", success=False)
#         traceback.print_exc()

# def show_message(msg, success=True):
#     color = (0.2, 0.8, 0.2) if success else (0.9, 0.5, 0.2)
#     cmds.inViewMessage(amg=f"<hl>{msg}</hl>", pos='midCenter', fade=True, fadeStayTime=1500, backColor=color, fadeOutTime=1000)

# def ui_build_chains(*args):
#     global _fk_chain, _ik_chain, _main_chain
#     _fk_chain, _ik_chain, _main_chain = build_chains()
#     show_message("✅ Cadenas creadas correctamente")

# def ui_setup_fk(*args):
#     if _fk_chain:
#         setup_fk_chain(_fk_chain)
#         show_message("✅ FK configurado correctamente")
#     else:
#         show_message("⚠️ Primero crea las cadenas", success=False)

# def ui_setup_ik(*args):
#     if _ik_chain:
#         setup_ik_chain(_ik_chain)
#         show_message("✅ IK configurado correctamente")
#     else:
#         show_message("⚠️ Primero crea las cadenas", success=False)

# def ui_setup_main(*args):
#     if _fk_chain and _ik_chain and _main_chain:
#         setup_main_chain(_fk_chain, _ik_chain, _main_chain)
#         show_message("✅ MAIN configurado correctamente")
#     else:
#         show_message("⚠️ Primero crea las cadenas", success=False)

# def ui_build_all(*args):
#     fk_chain, ik_chain, main_chain = build_chains()
#     setup_fk_chain(fk_chain)
#     setup_ik_chain(ik_chain)
#     setup_main_chain(fk_chain, ik_chain, main_chain)
#     show_message("🎉 Rig completo creado con éxito")

# # ---------------------------
# # Embeddable UI
# # ---------------------------
# def build_ui(parent=None):
#     """Versión mejorada que maneja correctamente el parent"""
#     created_window = False
    
#     # Si no hay parent, crear ventana independiente
#     if parent is None:
#         if cmds.window("legRigUI", exists=True):
#             cmds.deleteUI("legRigUI")
#         win = cmds.window("legRigUI", title="🦿 Rig Pierna FK/IK - Auto Builder", w=420, h=420, sizeable=True)
#         main_layout = cmds.columnLayout(adjustableColumn=True)
#         created_window = True
#     else:
#         # Usar el parent proporcionado directamente
#         main_layout = parent

#     # CONTENIDO DE LA UI (sin crear layouts adicionales)
#     cmds.text(label="⚙️  Auto Rig Pierna FK/IK", height=30, align="center", bgc=(0.1, 0.1, 0.1), parent=main_layout)
#     cmds.separator(h=8, style="in", parent=main_layout)

#     cmds.button(label="🔧 Crear Joints Base", c=ui_build_chains, bgc=(0.1, 0.7, 0.9), h=36, parent=main_layout)
#     cmds.button(label="🦴 Configurar Cadena FK", c=ui_setup_fk, bgc=(0.9, 0.4, 0.4), h=36, parent=main_layout)
#     cmds.button(label="⚙️ Configurar Cadena IK", c=ui_setup_ik, bgc=(0.4, 0.9, 0.4), h=36, parent=main_layout)
#     cmds.button(label="🔗 Configurar Cadena MAIN", c=ui_setup_main, bgc=(0.5, 0.5, 0.9), h=36, parent=main_layout)
#     cmds.separator(h=8, style="in", parent=main_layout)
#     cmds.button(label="🚀 Crear Todo el Rig (Full Auto)", c=ui_build_all, bgc=(1.0, 0.8, 0.3), h=40, parent=main_layout)
    
#     cmds.separator(h=10, style="in", parent=main_layout)
    
#     # BOTÓN DE RESET COMPLETO - MÁS DESTACADO
#     cmds.button(label="🗑️ RESET COMPLETO - Limpiar TODO", c=reset_leg_rig_system, 
#                 bgc=(0.9, 0.2, 0.2), h=40, parent=main_layout)
    
#     cmds.separator(h=8, style="in", parent=main_layout)
#     cmds.text(label="⚠️ ATENCIÓN: Elimina TODOS los joints, controles,\n    grupos, constraints y sistemas creados", 
#               align="center", parent=main_layout)
#     cmds.text(label="💡 La escena quedará completamente limpia", 
#               align="center", parent=main_layout)
#     cmds.separator(h=10, style="in", parent=main_layout)
#     cmds.text(label="💡 Tip: Ejecuta paso a paso para depurar errores.", align="center", parent=main_layout)

#     if created_window:
#         cmds.showWindow(win)

# def open_leg_rig_ui():
#     build_ui(parent=None)

# if __name__ == "__main__":
#     open_leg_rig_ui()



import maya.cmds as cmds
import traceback
from .create_joints import build_chains
from .fk_setup import setup_fk_chain
from .ik_setup import setup_ik_chain
from .orient_constraints import setup_main_chain

_fk_chain = []
_ik_chain = []
_main_chain = []

def reset_leg_rig_system(*args):
    """
    Elimina TODOS los elementos creados por el sistema de pierna FK/IK
    EXCEPTO los joints - preserva toda la jerarquía de joints
    """
    try:
        # Lista completa de patrones para identificar elementos a eliminar (EXCLUYENDO JOINTS)
        delete_patterns = [
            # Controles FK/IK
            "*_FK_ctrl*",
            "*_IK_ctrl*",
            "*_ctrl*",
            "*_control*",
            "*_CTRL*",
            "*_auto*",
            "*_driver*",
            # IK Handles y effectors
            "*_IKhandle*",
            "*_ikHandle*",
            "*_effector*",
            "*_ikSpline*",
            # Pole Vectors
            "*_poleVector*",
            "*_PV_*",
            "*_pole_*",
            "*_PVctr*",
            # Grupos de organización
            "*_FK_GRP*",
            "*_IK_GRP*", 
            "*_MAIN_GRP*",
            "*_RIG_GRP*",
            "*_CONTROLS_GRP*",
            "*_AUTO_GRP*",
            "*_ZERO_GRP*",
            "*_OFFSET_GRP*",
            "*_SETUP_GRP*",
            "*_GEO_GRP*",
            "*_JOINTS_GRP*",
            # Nodos de utilidad y conexión
            "*_attributes*",
            "*_reverse*",
            "*_condition*",
            "*_multiplyDivide*",
            "*_decomposeMatrix*",
            "*_composeMatrix*",
            "*_multMatrix*",
            "*_plusMinusAverage*",
            "*_vectorProduct*",
            # Constraints
            "*_constraint*",
            "*_pointConstraint*",
            "*_orientConstraint*",
            "*_parentConstraint*",
            "*_aimConstraint*",
            "*_scaleConstraint*",
            "*_geometryConstraint*",
            # Skin y deformadores
            "*_skinCluster*",
            "*_blendShape*",
            "*_cluster*",
            "*_nonLinear*",
            # Curvas y formas
            "*_curve*",
            "*_shape*",
            "*_nurbsCircle*",
            "*_locator*"
        ]
        
        # Elementos específicos por nombre (EXCLUYENDO JOINTS)
        specific_elements = [
            "middleLeg_practice_L_IKhandle_001", "middleLeg_practice_L_effector_001",
            "middleLeg_practice_L_IKpoleVector_001", "middleLeg_practice_L_IKpoleVectorRoot_001",
            "endLeg_practice_L_IKctrl_001", "Leg_practice_L_attributes_001", "FKIK_reverse"
        ]
        
        deleted_count = 0
        
        print("🧹 INICIANDO LIMPIEZA COMPLETA DEL SISTEMA (JOINTS PRESERVADOS)...")
        
        # ESTRATEGIA 1: ELIMINAR POR TIPOS DE NODO (EXCLUYENDO JOINTS)
        print("🔍 Eliminando por tipos de nodo...")
        node_types_to_delete = [
            "transform", "mesh", "nurbsCurve", "locator",
            "ikHandle", "ikEffector", "pointConstraint", "orientConstraint",
            "parentConstraint", "aimConstraint", "scaleConstraint",
            "decomposeMatrix", "multMatrix", "composeMatrix", "multiplyDivide",
            "plusMinusAverage", "reverse", "condition", "vectorProduct",
            "curveInfo", "motionPath", "cluster", "skinCluster", "blendShape",
            "expression", "script", "objectSet", "groupId"
        ]
        
        for node_type in node_types_to_delete:
            try:
                nodes = cmds.ls(type=node_type)
                for node in nodes:
                    try:
                        # Verificar que existe y no es del sistema por defecto
                        if (cmds.objExists(node) and 
                            not node.startswith('persp') and 
                            not node.startswith('top') and 
                            not node.startswith('front') and 
                            not node.startswith('side') and
                            node != "time1" and
                            node != "sequenceManager1" and
                            not node.startswith('defaultLightSet') and
                            not node.startswith('defaultObjectSet')):
                            
                            # VERIFICACIÓN CRÍTICA: NO ELIMINAR JOINTS
                            if cmds.objectType(node) != "joint":
                                cmds.delete(node)
                                deleted_count += 1
                                print(f"🗑️ Eliminado por tipo {node_type}: {node}")
                            else:
                                print(f"🔒 PRESERVADO joint: {node}")
                            
                    except Exception as e:
                        print(f"⚠️ No se pudo eliminar {node}: {e}")
            except Exception as e:
                print(f"⚠️ Error con tipo {node_type}: {e}")
        
        # ESTRATEGIA 2: ELIMINAR POR PATRONES DE NOMBRE (EXCLUYENDO JOINTS)
        print("🔍 Eliminando por patrones de nombre...")
        for pattern in delete_patterns:
            try:
                objects = cmds.ls(pattern, transforms=True, shapes=True, dagObjects=True, exactType=False)
                for obj in objects:
                    try:
                        # Verificar que existe y no es del sistema por defecto
                        if (cmds.objExists(obj) and 
                            not obj.startswith('persp') and 
                            not obj.startswith('top') and 
                            not obj.startswith('front') and 
                            not obj.startswith('side')):
                            
                            # VERIFICACIÓN CRÍTICA: NO ELIMINAR JOINTS
                            if cmds.objectType(obj) != "joint":
                                cmds.delete(obj)
                                deleted_count += 1
                                print(f"🗑️ Eliminado por patrón: {obj}")
                            else:
                                print(f"🔒 PRESERVADO joint: {obj}")
                                
                    except Exception as e:
                        print(f"⚠️ No se pudo eliminar {obj}: {e}")
            except Exception as e:
                print(f"⚠️ Error con patrón {pattern}: {e}")
        
        # ESTRATEGIA 3: ELIMINAR ELEMENTOS ESPECÍFICOS
        print("🔍 Eliminando elementos específicos...")
        for element in specific_elements:
            if cmds.objExists(element):
                try:
                    # VERIFICACIÓN CRÍTICA: NO ELIMINAR JOINTS
                    if cmds.objectType(element) != "joint":
                        cmds.delete(element)
                        deleted_count += 1
                        print(f"🗑️ Eliminado específico: {element}")
                    else:
                        print(f"🔒 PRESERVADO joint: {element}")
                except Exception as e:
                    print(f"⚠️ No se pudo eliminar {element}: {e}")
        
        # ESTRATEGIA 4: BUSCAR Y ELIMINAR POR "practice" (EXCLUYENDO JOINTS)
        print("🔍 Buscando elementos con 'practice'...")
        practice_objects = cmds.ls("*practice*", transforms=True, shapes=True, dagObjects=True)
        for obj in practice_objects:
            try:
                if (cmds.objExists(obj) and 
                    not obj.startswith('persp') and 
                    not obj.startswith('top') and 
                    not obj.startswith('front') and 
                    not obj.startswith('side')):
                    
                    # VERIFICACIÓN CRÍTICA: NO ELIMINAR JOINTS
                    if cmds.objectType(obj) != "joint":
                        cmds.delete(obj)
                        deleted_count += 1
                        print(f"🗑️ Eliminado por 'practice': {obj}")
                    else:
                        print(f"🔒 PRESERVADO joint: {obj}")
                        
            except Exception as e:
                print(f"⚠️ No se pudo eliminar {obj}: {e}")
        
        # ESTRATEGIA 5: LIMPIEZA DE GRUPOS VACÍOS (EXCLUYENDO JOINTS)
        print("🔍 Limpiando grupos vacíos...")
        try:
            all_transforms = cmds.ls(type="transform")
            for transform in all_transforms:
                try:
                    if (cmds.objExists(transform) and 
                        not transform.startswith('persp') and 
                        not transform.startswith('top') and 
                        not transform.startswith('front') and 
                        not transform.startswith('side')):
                        
                        # VERIFICACIÓN CRÍTICA: NO ELIMINAR JOINTS
                        if cmds.objectType(transform) != "joint":
                            # Verificar si es un grupo vacío
                            children = cmds.listRelatives(transform, children=True, fullPath=True) or []
                            shapes = cmds.listRelatives(transform, shapes=True, fullPath=True) or []
                            
                            if len(children) == 0 and len(shapes) == 0:
                                cmds.delete(transform)
                                deleted_count += 1
                                print(f"🗑️ Eliminado grupo vacío: {transform}")
                        else:
                            print(f"🔒 PRESERVADO joint: {transform}")
                            
                except Exception as e:
                    print(f"⚠️ No se pudo limpiar {transform}: {e}")
        except Exception as e:
            print(f"⚠️ Error limpiando grupos vacíos: {e}")
        
        # ESTRATEGIA 6: LIMPIEZA DE CAPAS DE DISPLAY
        print("🔍 Limpiando capas de display...")
        display_layers = cmds.ls(type="displayLayer")
        for layer in display_layers:
            if layer != "defaultLayer":
                try:
                    cmds.delete(layer)
                    deleted_count += 1
                    print(f"🗑️ Eliminada capa: {layer}")
                except Exception as e:
                    print(f"⚠️ No se pudo eliminar capa {layer}: {e}")
        
        # ESTRATEGIA 7: LIMPIAR NAMESPACES
        print("🔍 Limpiando namespaces...")
        try:
            namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
            for ns in namespaces:
                if ns not in ['UI', 'shared'] and not ns.startswith(':'):
                    try:
                        cmds.namespace(removeNamespace=ns, mergeNamespaceWithRoot=True)
                        print(f"🗑️ Limpiado namespace: {ns}")
                    except Exception as e:
                        print(f"⚠️ No se pudo limpiar namespace {ns}: {e}")
        except Exception as e:
            print(f"⚠️ Error limpiando namespaces: {e}")
        
        # Resetear variables globales
        global _fk_chain, _ik_chain, _main_chain
        _fk_chain = []
        _ik_chain = [] 
        _main_chain = []
        
        # Forzar actualización de la escena
        cmds.refresh()
        
        # Mostrar mensaje de confirmación
        show_message(f"✅ Reset Completo: {deleted_count} elementos eliminados (joints preservados)")
        print(f"🎯 RESET COMPLETO EXITOSO: {deleted_count} elementos eliminados")
        print("✨ La escena ha quedado completamente limpia (todos los joints preservados)")
        
    except Exception as e:
        show_message(f"⚠️ Error en reset completo: {e}", success=False)
        traceback.print_exc()

def show_message(msg, success=True):
    color = (0.2, 0.8, 0.2) if success else (0.9, 0.5, 0.2)
    cmds.inViewMessage(amg=f"<hl>{msg}</hl>", pos='midCenter', fade=True, fadeStayTime=1500, backColor=color, fadeOutTime=1000)

def ui_build_chains(*args):
    global _fk_chain, _ik_chain, _main_chain
    _fk_chain, _ik_chain, _main_chain = build_chains()
    show_message("✅ Cadenas creadas correctamente")

def ui_setup_fk(*args):
    if _fk_chain:
        setup_fk_chain(_fk_chain)
        show_message("✅ FK configurado correctamente")
    else:
        show_message("⚠️ Primero crea las cadenas", success=False)

def ui_setup_ik(*args):
    if _ik_chain:
        setup_ik_chain(_ik_chain)
        show_message("✅ IK configurado correctamente")
    else:
        show_message("⚠️ Primero crea las cadenas", success=False)

def ui_setup_main(*args):
    if _fk_chain and _ik_chain and _main_chain:
        setup_main_chain(_fk_chain, _ik_chain, _main_chain)
        show_message("✅ MAIN configurado correctamente")
    else:
        show_message("⚠️ Primero crea las cadenas", success=False)

def ui_build_all(*args):
    fk_chain, ik_chain, main_chain = build_chains()
    setup_fk_chain(fk_chain)
    setup_ik_chain(ik_chain)
    setup_main_chain(fk_chain, ik_chain, main_chain)
    show_message("🎉 Rig completo creado con éxito")

# ---------------------------
# Embeddable UI
# ---------------------------
def build_ui(parent=None):
    """Versión mejorada que maneja correctamente el parent"""
    created_window = False
    
    # Si no hay parent, crear ventana independiente
    if parent is None:
        if cmds.window("legRigUI", exists=True):
            cmds.deleteUI("legRigUI")
        win = cmds.window("legRigUI", title="🦿 Rig Pierna FK/IK - Auto Builder", w=420, h=420, sizeable=True)
        main_layout = cmds.columnLayout(adjustableColumn=True)
        created_window = True
    else:
        # Usar el parent proporcionado directamente
        main_layout = parent

    # CONTENIDO DE LA UI (sin crear layouts adicionales)
    cmds.text(label="⚙️  Auto Rig Pierna FK/IK", height=30, align="center", bgc=(0.1, 0.1, 0.1), parent=main_layout)
    cmds.separator(h=8, style="in", parent=main_layout)

    cmds.button(label="🔧 Crear Joints Base", c=ui_build_chains, bgc=(0.1, 0.7, 0.9), h=36, parent=main_layout)
    cmds.button(label="🦴 Configurar Cadena FK", c=ui_setup_fk, bgc=(0.9, 0.4, 0.4), h=36, parent=main_layout)
    cmds.button(label="⚙️ Configurar Cadena IK", c=ui_setup_ik, bgc=(0.4, 0.9, 0.4), h=36, parent=main_layout)
    cmds.button(label="🔗 Configurar Cadena MAIN", c=ui_setup_main, bgc=(0.5, 0.5, 0.9), h=36, parent=main_layout)
    cmds.separator(h=8, style="in", parent=main_layout)
    cmds.button(label="🚀 Crear Todo el Rig (Full Auto)", c=ui_build_all, bgc=(1.0, 0.8, 0.3), h=40, parent=main_layout)
    
    cmds.separator(h=10, style="in", parent=main_layout)
    
    # BOTÓN DE RESET COMPLETO - ACTUALIZADO
    cmds.button(label="🗑️ RESET COMPLETO (Preserva Joints)", c=reset_leg_rig_system, 
                bgc=(0.9, 0.2, 0.2), h=40, parent=main_layout)
    
    cmds.separator(h=8, style="in", parent=main_layout)
    cmds.text(label="⚠️ ATENCIÓN: Elimina controles, IK, constraints,\n    grupos y sistemas PERO PRESERVA JOINTS", 
              align="center", parent=main_layout)
    cmds.text(label="💡 Todos los joints de la escena se mantienen", 
              align="center", parent=main_layout)
    cmds.separator(h=10, style="in", parent=main_layout)
    cmds.text(label="💡 Tip: Los joints base se preservan para reutilizar", align="center", parent=main_layout)

    if created_window:
        cmds.showWindow(win)

def open_leg_rig_ui():
    build_ui(parent=None)

if __name__ == "__main__":
    open_leg_rig_ui()