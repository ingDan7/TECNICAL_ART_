# # # # # # import maya.cmds as cmds
# # # # # # import traceback

# # # # # # from .tail_rig_curve import use_existing_joints, make_curve_dynamic
# # # # # # from .tail_rig_ik import create_ik_spline_handle
# # # # # # from .tail_rig_dynamics import configure_nucleus_and_follicle
# # # # # # from .tail_rig_controls import create_dynamic_control
# # # # # # from .tail_rig_geometry import create_poly_tail, create_body_and_head, create_torus_system


# # # # # # # =========================================================
# # # # # # # (9) FUNCIÓN PARA EJECUTAR TODOS LOS PASOS AUTOMÁTICAMENTE
# # # # # # # =========================================================

# # # # # # def execute_all_steps_Tail():
# # # # # #     """Ejecuta todos los pasos del rig de cola automáticamente."""
# # # # # #     try:
# # # # # #         print("🚀 INICIANDO EJECUCIÓN COMPLETA DEL RIG DE COLA...")
        
# # # # # #         # Paso 1: Crear Curva Base
# # # # # #         print("📝 Paso 1: Creando curva base...")
# # # # # #         result1 = use_existing_joints()
# # # # # #         if result1:
# # # # # #             update_step_status(1, "step1_btn")
        
# # # # # #         # Paso 2: Hacer Curva Dinámica
# # # # # #         print("🌀 Paso 2: Haciendo curva dinámica...")
# # # # # #         result2 = make_curve_dynamic()
# # # # # #         if result2:
# # # # # #             update_step_status(2, "step2_btn")
        
# # # # # #         # Paso 3: Crear IK Spline Handle
# # # # # #         print("🔗 Paso 3: Creando IK Spline Handle...")
# # # # # #         result3 = create_ik_spline_handle()
# # # # # #         if result3:
# # # # # #             update_step_status(3, "step3_btn")
        
# # # # # #         # Paso 4: Configurar Nucleus y Follicle
# # # # # #         print("⚙️ Paso 4: Configurando nucleus y follicle...")
# # # # # #         result4 = configure_nucleus_and_follicle()
# # # # # #         if result4:
# # # # # #             update_step_status(4, "step4_btn")
        
# # # # # #         # Paso 5: Crear Control + Root
# # # # # #         print("🎯 Paso 5: Creando control y root...")
# # # # # #         result5 = create_dynamic_control()
# # # # # #         if result5:
# # # # # #             update_step_status(5, "step5_btn")
        
# # # # # #         # Paso 6: Crear PolyTail + Skin
# # # # # #         print("🧱 Paso 6: Creando polyTail y skin...")
# # # # # #         result6 = create_poly_tail()
# # # # # #         if result6:
# # # # # #             update_step_status(6, "step6_btn")
        
# # # # # #         # Paso 7: Crear Cuerpo + Cabeza + Collider
# # # # # #         print("👤 Paso 7: Creando cuerpo y cabeza...")
# # # # # #         result7 = create_body_and_head()
# # # # # #         if result7:
# # # # # #             update_step_status(7, "step7_btn")
        
# # # # # #         # Paso 8: Crear Toroide + Sistema
# # # # # #         print("🌀 Paso 8: Creando sistema toroide...")
# # # # # #         result8 = create_torus_system()
# # # # # #         if result8:
# # # # # #             update_step_status(8, "step8_btn")
        
# # # # # #         # Mensaje final
# # # # # #         cmds.inViewMessage(
# # # # # #             amg='<span style="color:#7FFF7F;">✅ Rig de cola completado automáticamente</span>',
# # # # # #             pos='topCenter', fade=True, fst=1500, ft=200
# # # # # #         )
# # # # # #         print("🎉 ¡RIG DE COLA COMPLETADO EXITOSAMENTE!")
        
# # # # # #         return True
        
# # # # # #     except Exception as e:
# # # # # #         cmds.warning(f"❌ Error en ejecución automática: {str(e)}")
# # # # # #         traceback.print_exc()
# # # # # #         return False


# # # # # # # =========================================================
# # # # # # # INTERFAZ DE USUARIO (UI) - RIG DE COLA
# # # # # # # =========================================================
# # # # # # step_status = {}

# # # # # # def update_step_status(step_num, button_name):
# # # # # #     """Marca un paso como completado (botón verde + check visual)."""
# # # # # #     step_status[step_num] = True
# # # # # #     if cmds.control(button_name, exists=True):
# # # # # #         cmds.button(button_name, e=True, bgc=(0.2, 0.6, 0.2), label=f"✓ Paso {step_num} completado")

# # # # # # def execute_step(step_num, func, button_name):
# # # # # #     """Ejecuta el paso y actualiza el botón según el resultado."""
# # # # # #     try:
# # # # # #         func()
# # # # # #         update_step_status(step_num, button_name)
# # # # # #     except Exception as e:
# # # # # #         cmds.warning(f"⚠ Error ejecutando paso {step_num}: {e}")
# # # # # #         traceback.print_exc()

# # # # # # def reset_all_steps():
# # # # # #     """Reinicia todos los botones y el estado visual."""
# # # # # #     for step in UI_STEPS:
# # # # # #         btn = step["btn_name"]
# # # # # #         if cmds.control(btn, exists=True):
# # # # # #             cmds.button(btn, e=True, bgc=(0.32, 0.32, 0.32), label=step["label"])
# # # # # #     step_status.clear()
# # # # # #     print("🔁 Progreso reiniciado.")


# # # # # # UI_STEPS = [
# # # # # #     {"num": 1, "btn_name": "step1_btn", "label": "1. Crear Curva Base (8 spans)", "func": use_existing_joints},
# # # # # #     {"num": 2, "btn_name": "step2_btn", "label": "2. Hacer Curva Dinámica (nHair)", "func": make_curve_dynamic},
# # # # # #     {"num": 3, "btn_name": "step3_btn", "label": "3. Crear IK Spline Handle", "func": create_ik_spline_handle},
# # # # # #     {"num": 4, "btn_name": "step4_btn", "label": "4. Configurar Nucleus y Follicle", "func": configure_nucleus_and_follicle},
# # # # # #     {"num": 5, "btn_name": "step5_btn", "label": "5. Crear Control + Root", "func": create_dynamic_control},
# # # # # #     {"num": 6, "btn_name": "step6_btn", "label": "6. Crear PolyTail + Skin", "func": create_poly_tail},
# # # # # #     {"num": 7, "btn_name": "step7_btn", "label": "7. Crear Cuerpo + Cabeza + Collider", "func": create_body_and_head},
# # # # # #     {"num": 8, "btn_name": "step8_btn", "label": "8. Crear Toroide + Plano + Locator + Control", "func": create_torus_system},
# # # # # #     {"num": 9, "btn_name": "step9_btn", "label": "9. Rig Completo", "func": execute_all_steps_Tail},
# # # # # # ]


# # # # # # def open_ui():
# # # # # #     """Abre la interfaz de rig de cola (estilo rig_Columna_02.py)."""
# # # # # #     try:
# # # # # #         if cmds.window("tailRigUI", exists=True):
# # # # # #             cmds.deleteUI("tailRigUI")

# # # # # #         win = cmds.window("tailRigUI", title="Rig de Cola - Builder Modular", w=380, h=360)
# # # # # #         cmds.columnLayout(adjustableColumn=True, rowSpacing=6, columnOffset=["both", 12])

# # # # # #         # Encabezado
# # # # # #         cmds.text(label="RIG DE COLA - SISTEMA MODULAR", align="center", font="boldLabelFont", h=25)
# # # # # #         cmds.separator(h=12, style="in")

# # # # # #         # Crear los botones según los pasos definidos
# # # # # #         for step in UI_STEPS:
# # # # # #             num, btn, label, func = step["num"], step["btn_name"], step["label"], step["func"]
# # # # # #             if callable(func):
# # # # # #                 cmds.button(
# # # # # #                     btn, label=label, h=34,
# # # # # #                     c=(lambda _x, s=num, b=btn, f=func: execute_step(s, f, b)),
# # # # # #                     bgc=[0.32, 0.32, 0.32]
# # # # # #                 )
# # # # # #             else:
# # # # # #                 cmds.button(
# # # # # #                     btn, label=f"{label} (no definida)", h=34,
# # # # # #                     enable=False, bgc=[0.25, 0.25, 0.25]
# # # # # #                 )

# # # # # #         # Separador y botón reiniciar
# # # # # #         cmds.separator(h=18, style="in")
# # # # # #         cmds.button(label="↻ Reiniciar", h=30, c=lambda _x: reset_all_steps(),
# # # # # #                     bgc=[0.35, 0.35, 0.38])

# # # # # #         cmds.showWindow(win)
# # # # # #         print("🟢 Interfaz de rig de cola lista y operativa.")

# # # # # #     except Exception:
# # # # # #         traceback.print_exc()
# # # # # #         cmds.warning("⚠ Error al crear la interfaz de rig de cola.")


# # # # # # # En su lugar:
# # # # # # if __name__ == "__main__":
# # # # # #     open_ui()


# import maya.cmds as cmds
# import traceback
# from .tail_rig_curve import use_existing_joints, make_curve_dynamic
# from .tail_rig_ik import create_ik_spline_handle
# from .tail_rig_dynamics import configure_nucleus_and_follicle
# from .tail_rig_controls import create_dynamic_control
# from .tail_rig_geometry import create_poly_tail, create_body_and_head, create_torus_system

# step_status = {}

# def update_step_status(step_num, button_name):
#     step_status[step_num] = True
#     if cmds.control(button_name, exists=True):
#         cmds.button(button_name, e=True, bgc=(0.2, 0.6, 0.2), label=f"✓ Paso {step_num} completado")

# def execute_step(step_num, func, button_name):
#     try:
#         func()
#         update_step_status(step_num, button_name)
#     except Exception as e:
#         cmds.warning(f"⚠ Error ejecutando paso {step_num}: {e}")
#         traceback.print_exc()

# def reset_tail_rig_system(*args):
#     """
#     Elimina TODOS los elementos creados por el sistema de cola dinámica
#     Versión ultra-agresiva que limpia TODO sin excepciones (excepto joints)
#     """
#     try:
#         deleted_count = 0
        
#         print("🧹 INICIANDO LIMPIEZA ULTRA-COMPLETA DEL SISTEMA DE COLA...")
        
#         # ESTRATEGIA 1: ELIMINAR POR TIPOS DE NODO (EXCLUYENDO JOINTS)
#         print("🔍 Buscando por tipos de nodo...")
#         node_types = [
#             "transform", "mesh", "nurbsCurve", "locator",
#             "hairSystem", "nucleus", "follicle", "ikHandle", "ikEffector", 
#             "ikSplineSolver", "curveInfo", "pointConstraint", "parentConstraint",
#             "aimConstraint", "orientConstraint", "scaleConstraint", "decomposeMatrix",
#             "multMatrix", "composeMatrix", "blendShape", "skinCluster", "cluster",
#             "tweak", "nurbsTessellate", "unitConversion", "condition", "reverse",
#             "multiplyDivide", "plusMinusAverage", "expression", "script", "groupId"
#         ]
        
#         for node_type in node_types:
#             try:
#                 nodes = cmds.ls(type=node_type)
#                 for node in nodes:
#                     try:
#                         # EXCLUSIONES MÍNIMAS - solo lo absolutamente esencial de Maya
#                         if (cmds.objExists(node) and 
#                             not node.startswith('persp') and 
#                             not node.startswith('top') and 
#                             not node.startswith('front') and 
#                             not node.startswith('side') and
#                             node != "time1" and
#                             node != "sequenceManager1" and
#                             not node.startswith('hardware') and
#                             not node.startswith('stroke') and
#                             not node.startswith('default') and
#                             not node.startswith('lightLinker') and
#                             not node.startswith('objectSet') and
#                             not node.startswith('render') and
#                             not node.startswith('dof') and
#                             not node.startswith('hyper') and
#                             not node.startswith('solid') and
#                             not node.startswith('shading') and
#                             not node.startswith('lambert') and
#                             not node.startswith('initial') and
#                             not node.startswith('character') and
#                             'skinCluster' not in node and
#                             'tweak' not in node):
                            
#                             # VERIFICACIÓN CRÍTICA: NO ELIMINAR JOINTS
#                             if cmds.objectType(node) != "joint":
#                                 cmds.delete(node)
#                                 deleted_count += 1
#                                 print(f"🗑️ Eliminado por tipo {node_type}: {node}")
#                             else:
#                                 print(f"🔒 PRESERVADO joint: {node}")
                            
#                     except Exception as e:
#                         print(f"⚠️ No se pudo eliminar {node}: {e}")
#             except Exception as e:
#                 print(f"⚠️ Error con tipo {node_type}: {e}")
        
#         # ESTRATEGIA 2: ELIMINAR POR PATRONES DE NOMBRE (MUY AMPLIA)
#         print("🔍 Buscando por patrones de nombre...")
#         delete_patterns = [
#             # Patrones ultra-amplios
#             "*tail*", "*Tail*", "*TAIL*",
#             "*curve*", "*Curve*", "*CURVE*", "*crv*", "*Crv*", "*CRV*",
#             "*ctrl*", "*Ctrl*", "*CTRL*", "*control*", "*Control*", "*CONTROL*",
#             "*driver*", "*Driver*", "*DRIVER*", "*root*", "*Root*", "*ROOT*",
#             "*auto*", "*Auto*", "*AUTO*", "*master*", "*Master*", "*MASTER*",
#             "*handle*", "*Handle*", "*HANDLE*", "*effector*", "*Effector*", "*EFFECTOR*",
#             "*geo*", "*Geo*", "*GEO*", "*mesh*", "*Mesh*", "*MESH*", "*poly*", "*Poly*", "*POLY*",
#             "*grp*", "*Grp*", "*GRP*", "*group*", "*Group*", "*GROUP*",
#             "*rig*", "*Rig*", "*RIG*", "*setup*", "*Setup*", "*SETUP*",
#             "*dynamic*", "*Dynamic*", "*DYNAMIC*", "*nucleus*", "*Nucleus*", "*NUCLEUS*",
#             "*hair*", "*Hair*", "*HAIR*", "*follicle*", "*Follicle*", "*FOLLICLE*",
#             "*foll*", "*Foll*", "*FOLL*", "*spline*", "*Spline*", "*SPLINE*",
#             "*ik*", "*IK*", "*Ik*", "*skin*", "*Skin*", "*SKIN*", "*cluster*", "*Cluster*", "*CLUSTER*",
#             "*blend*", "*Blend*", "*BLEND*", "*constraint*", "*Constraint*", "*CONSTRAINT*",
#             "*torus*", "*Torus*", "*TORUS*", "*body*", "*Body*", "*BODY*", "*head*", "*Head*", "*HEAD*",
#             "*polyTail*", "*body_geo*", "*head_geo*", "*torus_control*", "*tail_geometry*"
#         ]
        
#         for pattern in delete_patterns:
#             try:
#                 # Buscar de forma MUY amplia
#                 objects = cmds.ls(pattern, transforms=True, shapes=True, dagObjects=True, exactType=False, long=True)
#                 for obj in objects:
#                     try:
#                         # Solo verificar que existe y no es del sistema base
#                         if (cmds.objExists(obj) and 
#                             not any(excluded in obj for excluded in [
#                                 'persp', 'top', 'front', 'side', 'time1', 
#                                 'sequenceManager1', 'default', 'lightLinker'
#                             ])):
                            
#                             # VERIFICACIÓN CRÍTICA: NO ELIMINAR JOINTS
#                             if cmds.objectType(obj) != "joint":
#                                 cmds.delete(obj)
#                                 deleted_count += 1
#                                 print(f"🗑️ Eliminado por patrón '{pattern}': {obj}")
#                             else:
#                                 print(f"🔒 PRESERVADO joint: {obj}")
                            
#                     except Exception as e:
#                         print(f"⚠️ No se pudo eliminar {obj}: {e}")
#             except Exception as e:
#                 print(f"⚠️ Error con patrón {pattern}: {e}")
        
#         # ESTRATEGIA 3: BUSCAR Y ELIMINAR TODO LO QUE CONTENGA PALABRAS CLAVE
#         print("🔍 Buscando por palabras clave...")
#         keywords = [
#             "tail", "curve", "ctrl", "control", "driver", "root", 
#             "auto", "master", "handle", "geo", "mesh", "poly", "grp", "group",
#             "rig", "setup", "dynamic", "nucleus", "hair", "follicle", "foll",
#             "spline", "ik", "skin", "cluster", "blend", "constraint", "torus",
#             "body", "head"
#         ]
        
#         for keyword in keywords:
#             try:
#                 # Buscar en ambos casos (minúsculas y mayúsculas)
#                 objects_lower = cmds.ls(f"*{keyword}*", transforms=True, shapes=True, dagObjects=True)
#                 objects_upper = cmds.ls(f"*{keyword.upper()}*", transforms=True, shapes=True, dagObjects=True)
#                 objects_title = cmds.ls(f"*{keyword.title()}*", transforms=True, shapes=True, dagObjects=True)
                
#                 all_objects = set(objects_lower + objects_upper + objects_title)
                
#                 for obj in all_objects:
#                     try:
#                         if (cmds.objExists(obj) and 
#                             not any(excluded in obj for excluded in [
#                                 'persp', 'top', 'front', 'side', 'time1', 
#                                 'sequenceManager1', 'default', 'lightLinker'
#                             ])):
                            
#                             # VERIFICACIÓN CRÍTICA: NO ELIMINAR JOINTS
#                             if cmds.objectType(obj) != "joint":
#                                 cmds.delete(obj)
#                                 deleted_count += 1
#                                 print(f"🗑️ Eliminado por keyword '{keyword}': {obj}")
#                             else:
#                                 print(f"🔒 PRESERVADO joint: {obj}")
                            
#                     except Exception as e:
#                         print(f"⚠️ No se pudo eliminar {obj}: {e}")
#             except Exception as e:
#                 print(f"⚠️ Error con keyword {keyword}: {e}")
        
#         # ESTRATEGIA 4: ELIMINAR GRUPOS VACÍOS Y ELEMENTOS HUÉRFANOS
#         print("🔍 Limpiando grupos vacíos y elementos huérfanos...")
#         try:
#             # Buscar todos los transforms que no tengan hijos
#             all_transforms = cmds.ls(type="transform", long=True)
#             for transform in all_transforms:
#                 try:
#                     if (cmds.objExists(transform) and 
#                         not any(excluded in transform for excluded in [
#                             'persp', 'top', 'front', 'side', 'time1', 
#                             'sequenceManager1', 'default', 'lightLinker'
#                         ])):
                        
#                         # VERIFICACIÓN CRÍTICA: NO ELIMINAR JOINTS
#                         if cmds.objectType(transform) != "joint":
#                             # Verificar si es un grupo vacío o tiene pocas conexiones
#                             children = cmds.listRelatives(transform, children=True, fullPath=True) or []
#                             shapes = cmds.listRelatives(transform, shapes=True, fullPath=True) or []
                            
#                             if len(children) == 0 and len(shapes) == 0:
#                                 cmds.delete(transform)
#                                 deleted_count += 1
#                                 print(f"🗑️ Eliminado grupo vacío: {transform}")
#                         else:
#                             print(f"🔒 PRESERVADO joint: {transform}")
                            
#                 except Exception as e:
#                     print(f"⚠️ No se pudo limpiar {transform}: {e}")
#         except Exception as e:
#             print(f"⚠️ Error limpiando grupos vacíos: {e}")
        
#         # ESTRATEGIA 5: LIMPIEZA PROFUNDA DE CAPAS Y SETS
#         print("🔍 Limpiando capas y sets...")
        
#         # Limpiar todas las capas de display (excepto defaultLayer)
#         display_layers = cmds.ls(type="displayLayer")
#         for layer in display_layers:
#             if layer != "defaultLayer":
#                 try:
#                     cmds.delete(layer)
#                     deleted_count += 1
#                     print(f"🗑️ Eliminada capa: {layer}")
#                 except Exception as e:
#                     print(f"⚠️ No se pudo eliminar capa {layer}: {e}")
        
#         # Limpiar sets de selección no esenciales
#         selection_sets = cmds.ls(type="objectSet")
#         for obj_set in selection_sets:
#             if obj_set != "defaultObjectSet":
#                 try:
#                     cmds.delete(obj_set)
#                     deleted_count += 1
#                     print(f"🗑️ Eliminado set: {obj_set}")
#                 except Exception as e:
#                     print(f"⚠️ No se pudo eliminar set {obj_set}: {e}")
        
#         # ESTRATEGIA 6: LIMPIAR NAMESPACES
#         print("🔍 Limpiando namespaces...")
#         try:
#             namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
#             for ns in namespaces:
#                 if ns not in ['UI', 'shared'] and not ns.startswith(':'):
#                     try:
#                         cmds.namespace(removeNamespace=ns, mergeNamespaceWithRoot=True)
#                         print(f"🗑️ Limpiado namespace: {ns}")
#                     except Exception as e:
#                         print(f"⚠️ No se pudo limpiar namespace {ns}: {e}")
#         except Exception as e:
#             print(f"⚠️ Error limpiando namespaces: {e}")
        
#         # ESTRATEGIA 7: LIMPIEZA FINAL Y RESET
#         print("🔍 Limpieza final...")
#         try:
#             # Limpiar selección
#             cmds.select(clear=True)
            
#             # Forzar actualización de la escena
#             cmds.refresh()
            
#             # Limpiar canal box
#             cmds.channelBox('mainChannelBox', edit=True, mainObjectList='')
#         except:
#             pass
        
#         # Resetear estado de los botones de la UI
#         reset_all_steps()
        
#         # Mostrar mensaje de confirmación
#         success_msg = f'<hl>✅ RESET COMPLETO: {deleted_count} elementos eliminados</hl>'
#         cmds.inViewMessage(amg=success_msg, pos='midCenter', fade=True)
        
#         print(f"🎯 RESET ULTRA-COMPLETO EXITOSO: {deleted_count} elementos eliminados")
#         print("✨ La escena ha quedado COMPLETAMENTE LIMPIA (joints preservados)")
        
#         # Mensaje final en script editor
#         cmds.warning(f"🎯 Reset ultra-completo: {deleted_count} elementos del sistema de cola eliminados (todos los joints preservados)")
        
#     except Exception as e:
#         cmds.warning(f"⚠️ Error en reset ultra-completo: {e}")
#         traceback.print_exc()

# def reset_all_steps(*args):
#     """Reinicia solo el estado visual de los botones"""
#     for step in UI_STEPS:
#         btn = step["btn_name"]
#         if cmds.control(btn, exists=True):
#             cmds.button(btn, e=True, bgc=(0.32, 0.32, 0.32), label=step["label"])
#     step_status.clear()
#     print("🔄 Estado de botones reiniciado")

# def execute_all_steps_Tail():
#     try:
#         for num, func in enumerate([
#             use_existing_joints, make_curve_dynamic, create_ik_spline_handle,
#             configure_nucleus_and_follicle, create_dynamic_control,
#             create_poly_tail, create_body_and_head, create_torus_system
#         ], start=1):
#             func()
#             update_step_status(num, f"step{num}_btn")
#         cmds.inViewMessage(amg='<hl>✅ Rig de cola completado automáticamente</hl>', pos='topCenter', fade=True)
#     except Exception as e:
#         cmds.warning(f"❌ Error en ejecución automática: {e}")
#         traceback.print_exc()

# UI_STEPS = [
#     {"num": 1, "btn_name": "step1_btn", "label": "1. Crear Curva Base", "func": use_existing_joints},
#     {"num": 2, "btn_name": "step2_btn", "label": "2. Hacer Curva Dinámica", "func": make_curve_dynamic},
#     {"num": 3, "btn_name": "step3_btn", "label": "3. Crear IK Spline Handle", "func": create_ik_spline_handle},
#     {"num": 4, "btn_name": "step4_btn", "label": "4. Configurar Nucleus y Follicle", "func": configure_nucleus_and_follicle},
#     {"num": 5, "btn_name": "step5_btn", "label": "5. Crear Control + Root", "func": create_dynamic_control},
#     {"num": 6, "btn_name": "step6_btn", "label": "6. Crear PolyTail + Skin", "func": create_poly_tail},
#     {"num": 7, "btn_name": "step7_btn", "label": "7. Crear Cuerpo + Cabeza", "func": create_body_and_head},
#     {"num": 8, "btn_name": "step8_btn", "label": "8. Crear Toroide + Control", "func": create_torus_system},
#     {"num": 9, "btn_name": "step9_btn", "label": "9. Rig Completo", "func": execute_all_steps_Tail},
# ]

# def build_ui(parent=None):
#     """Versión corregida que maneja correctamente el parámetro parent"""
#     created_window = False
    
#     # Si no hay parent, crear ventana independiente
#     if parent is None:
#         if cmds.window("tailRigUI", exists=True):
#             cmds.deleteUI("tailRigUI")
#         win = cmds.window("tailRigUI", title="🐍 Rig de Cola Modular", w=400, h=480)
#         main_layout = cmds.columnLayout(adjustableColumn=True)
#         created_window = True
#     else:
#         # Usar directamente el parent proporcionado sin crear layouts adicionales
#         main_layout = parent

#     # CONTENIDO DE LA UI - crear elementos directamente en el layout proporcionado
#     cmds.text("tailRig_title", label="🐍 RIG DE COLA - SISTEMA MODULAR", align="center", font="boldLabelFont", h=25, parent=main_layout)
#     cmds.separator("tailRig_sep1", h=10, style="in", parent=main_layout)

#     # Crear botones directamente en el layout principal
#     for step in UI_STEPS:
#         num, btn_name, label, func = step["num"], step["btn_name"], step["label"], step["func"]
#         cmds.button(btn_name, label=label, h=34, 
#                    c=lambda x, n=num, f=func, b=btn_name: execute_step(n, f, b), 
#                    bgc=(0.32, 0.32, 0.32), parent=main_layout)

#     cmds.separator("tailRig_sep2", h=12, style="in", parent=main_layout)
    
#     # SOLO BOTÓN DE RESET COMPLETO - Eliminado el botón de reiniciar progreso
#     cmds.button("tailRig_reset_full", label="💥 RESET ULTRA-COMPLETO - LIMPIAR TODO (excepto joints)", 
#                 c=reset_tail_rig_system, bgc=(0.9, 0.1, 0.1), h=40, parent=main_layout)
    
#     cmds.separator("tailRig_sep3", h=8, style="in", parent=main_layout)
#     cmds.text("tailRig_reset_info", 
#               label="⚠️ ATENCIÓN EXTREMA: Elimina ABSOLUTAMENTE TODO\n    curvas, controles, geometría, sistemas, grupos", 
#               align="center", parent=main_layout)
#     cmds.text("tailRig_reset_warning", 
#               label="💥 PRESERVA TODOS los joints de la escena", 
#               align="center", parent=main_layout)

#     if created_window:
#         cmds.showWindow(win)

# def open_ui(parent=None):
#     build_ui(parent=parent)

# if __name__ == "__main__":
#     open_ui()



# import maya.cmds as cmds
# import traceback
# from .tail_rig_curve import use_existing_joints, make_curve_dynamic
# from .tail_rig_ik import create_ik_spline_handle
# from .tail_rig_dynamics import configure_nucleus_and_follicle
# from .tail_rig_controls import create_dynamic_control
# from .tail_rig_geometry import create_poly_tail, create_body_and_head, create_torus_system

# step_status = {}

# def update_step_status(step_num, button_name):
#     step_status[step_num] = True
#     if cmds.control(button_name, exists=True):
#         cmds.button(button_name, e=True, bgc=(0.2, 0.8, 0.2), label=f"✅ Paso {step_num} COMPLETADO")

# def execute_step(step_num, func, button_name):
#     try:
#         func()
#         update_step_status(step_num, button_name)
#     except Exception as e:
#         cmds.warning(f"⚠ Error ejecutando paso {step_num}: {e}")
#         traceback.print_exc()

# def reset_tail_rig_system(*args):
#     """
#     Elimina TODOS los elementos creados por el sistema de cola dinámica
#     Versión ultra-agresiva que limpia TODO sin excepciones (excepto joints)
#     """
#     try:
#         deleted_count = 0
        
#         print("🧹 INICIANDO LIMPIEZA ULTRA-COMPLETA DEL SISTEMA DE COLA...")
        
#         # ESTRATEGIA 1: ELIMINAR POR TIPOS DE NODO (EXCLUYENDO JOINTS)
#         print("🔍 Buscando por tipos de nodo...")
#         node_types = [
#             "transform", "mesh", "nurbsCurve", "locator",
#             "hairSystem", "nucleus", "follicle", "ikHandle", "ikEffector", 
#             "ikSplineSolver", "curveInfo", "pointConstraint", "parentConstraint",
#             "aimConstraint", "orientConstraint", "scaleConstraint", "decomposeMatrix",
#             "multMatrix", "composeMatrix", "blendShape", "skinCluster", "cluster",
#             "tweak", "nurbsTessellate", "unitConversion", "condition", "reverse",
#             "multiplyDivide", "plusMinusAverage", "expression", "script", "groupId"
#         ]
        
#         for node_type in node_types:
#             try:
#                 nodes = cmds.ls(type=node_type)
#                 for node in nodes:
#                     try:
#                         # EXCLUSIONES MÍNIMAS - solo lo absolutamente esencial de Maya
#                         if (cmds.objExists(node) and 
#                             not node.startswith('persp') and 
#                             not node.startswith('top') and 
#                             not node.startswith('front') and 
#                             not node.startswith('side') and
#                             node != "time1" and
#                             node != "sequenceManager1" and
#                             not node.startswith('hardware') and
#                             not node.startswith('stroke') and
#                             not node.startswith('default') and
#                             not node.startswith('lightLinker') and
#                             not node.startswith('objectSet') and
#                             not node.startswith('render') and
#                             not node.startswith('dof') and
#                             not node.startswith('hyper') and
#                             not node.startswith('solid') and
#                             not node.startswith('shading') and
#                             not node.startswith('lambert') and
#                             not node.startswith('initial') and
#                             not node.startswith('character') and
#                             'skinCluster' not in node and
#                             'tweak' not in node):
                            
#                             # VERIFICACIÓN CRÍTICA: NO ELIMINAR JOINTS
#                             if cmds.objectType(node) != "joint":
#                                 cmds.delete(node)
#                                 deleted_count += 1
#                                 print(f"🗑️ Eliminado por tipo {node_type}: {node}")
#                             else:
#                                 print(f"🔒 PRESERVADO joint: {node}")
                            
#                     except Exception as e:
#                         print(f"⚠️ No se pudo eliminar {node}: {e}")
#             except Exception as e:
#                 print(f"⚠️ Error con tipo {node_type}: {e}")
        
#         # ESTRATEGIA 2: ELIMINAR POR PATRONES DE NOMBRE (MUY AMPLIA)
#         print("🔍 Buscando por patrones de nombre...")
#         delete_patterns = [
#             # Patrones ultra-amplios
#             "*tail*", "*Tail*", "*TAIL*",
#             "*curve*", "*Curve*", "*CURVE*", "*crv*", "*Crv*", "*CRV*",
#             "*ctrl*", "*Ctrl*", "*CTRL*", "*control*", "*Control*", "*CONTROL*",
#             "*driver*", "*Driver*", "*DRIVER*", "*root*", "*Root*", "*ROOT*",
#             "*auto*", "*Auto*", "*AUTO*", "*master*", "*Master*", "*MASTER*",
#             "*handle*", "*Handle*", "*HANDLE*", "*effector*", "*Effector*", "*EFFECTOR*",
#             "*geo*", "*Geo*", "*GEO*", "*mesh*", "*Mesh*", "*MESH*", "*poly*", "*Poly*", "*POLY*",
#             "*grp*", "*Grp*", "*GRP*", "*group*", "*Group*", "*GROUP*",
#             "*rig*", "*Rig*", "*RIG*", "*setup*", "*Setup*", "*SETUP*",
#             "*dynamic*", "*Dynamic*", "*DYNAMIC*", "*nucleus*", "*Nucleus*", "*NUCLEUS*",
#             "*hair*", "*Hair*", "*HAIR*", "*follicle*", "*Follicle*", "*FOLLICLE*",
#             "*foll*", "*Foll*", "*FOLL*", "*spline*", "*Spline*", "*SPLINE*",
#             "*ik*", "*IK*", "*Ik*", "*skin*", "*Skin*", "*SKIN*", "*cluster*", "*Cluster*", "*CLUSTER*",
#             "*blend*", "*Blend*", "*BLEND*", "*constraint*", "*Constraint*", "*CONSTRAINT*",
#             "*torus*", "*Torus*", "*TORUS*", "*body*", "*Body*", "*BODY*", "*head*", "*Head*", "*HEAD*",
#             "*polyTail*", "*body_geo*", "*head_geo*", "*torus_control*", "*tail_geometry*"
#         ]
        
#         for pattern in delete_patterns:
#             try:
#                 # Buscar de forma MUY amplia
#                 objects = cmds.ls(pattern, transforms=True, shapes=True, dagObjects=True, exactType=False, long=True)
#                 for obj in objects:
#                     try:
#                         # Solo verificar que existe y no es del sistema base
#                         if (cmds.objExists(obj) and 
#                             not any(excluded in obj for excluded in [
#                                 'persp', 'top', 'front', 'side', 'time1', 
#                                 'sequenceManager1', 'default', 'lightLinker'
#                             ])):
                            
#                             # VERIFICACIÓN CRÍTICA: NO ELIMINAR JOINTS
#                             if cmds.objectType(obj) != "joint":
#                                 cmds.delete(obj)
#                                 deleted_count += 1
#                                 print(f"🗑️ Eliminado por patrón '{pattern}': {obj}")
#                             else:
#                                 print(f"🔒 PRESERVADO joint: {obj}")
                            
#                     except Exception as e:
#                         print(f"⚠️ No se pudo eliminar {obj}: {e}")
#             except Exception as e:
#                 print(f"⚠️ Error con patrón {pattern}: {e}")
        
#         # ESTRATEGIA 3: BUSCAR Y ELIMINAR TODO LO QUE CONTENGA PALABRAS CLAVE
#         print("🔍 Buscando por palabras clave...")
#         keywords = [
#             "tail", "curve", "ctrl", "control", "driver", "root", 
#             "auto", "master", "handle", "geo", "mesh", "poly", "grp", "group",
#             "rig", "setup", "dynamic", "nucleus", "hair", "follicle", "foll",
#             "spline", "ik", "skin", "cluster", "blend", "constraint", "torus",
#             "body", "head"
#         ]
        
#         for keyword in keywords:
#             try:
#                 # Buscar en ambos casos (minúsculas y mayúsculas)
#                 objects_lower = cmds.ls(f"*{keyword}*", transforms=True, shapes=True, dagObjects=True)
#                 objects_upper = cmds.ls(f"*{keyword.upper()}*", transforms=True, shapes=True, dagObjects=True)
#                 objects_title = cmds.ls(f"*{keyword.title()}*", transforms=True, shapes=True, dagObjects=True)
                
#                 all_objects = set(objects_lower + objects_upper + objects_title)
                
#                 for obj in all_objects:
#                     try:
#                         if (cmds.objExists(obj) and 
#                             not any(excluded in obj for excluded in [
#                                 'persp', 'top', 'front', 'side', 'time1', 
#                                 'sequenceManager1', 'default', 'lightLinker'
#                             ])):
                            
#                             # VERIFICACIÓN CRÍTICA: NO ELIMINAR JOINTS
#                             if cmds.objectType(obj) != "joint":
#                                 cmds.delete(obj)
#                                 deleted_count += 1
#                                 print(f"🗑️ Eliminado por keyword '{keyword}': {obj}")
#                             else:
#                                 print(f"🔒 PRESERVADO joint: {obj}")
                            
#                     except Exception as e:
#                         print(f"⚠️ No se pudo eliminar {obj}: {e}")
#             except Exception as e:
#                 print(f"⚠️ Error con keyword {keyword}: {e}")
        
#         # ESTRATEGIA 4: ELIMINAR GRUPOS VACÍOS Y ELEMENTOS HUÉRFANOS
#         print("🔍 Limpiando grupos vacíos y elementos huérfanos...")
#         try:
#             # Buscar todos los transforms que no tengan hijos
#             all_transforms = cmds.ls(type="transform", long=True)
#             for transform in all_transforms:
#                 try:
#                     if (cmds.objExists(transform) and 
#                         not any(excluded in transform for excluded in [
#                             'persp', 'top', 'front', 'side', 'time1', 
#                             'sequenceManager1', 'default', 'lightLinker'
#                         ])):
                        
#                         # VERIFICACIÓN CRÍTICA: NO ELIMINAR JOINTS
#                         if cmds.objectType(transform) != "joint":
#                             # Verificar si es un grupo vacío o tiene pocas conexiones
#                             children = cmds.listRelatives(transform, children=True, fullPath=True) or []
#                             shapes = cmds.listRelatives(transform, shapes=True, fullPath=True) or []
                            
#                             if len(children) == 0 and len(shapes) == 0:
#                                 cmds.delete(transform)
#                                 deleted_count += 1
#                                 print(f"🗑️ Eliminado grupo vacío: {transform}")
#                         else:
#                             print(f"🔒 PRESERVADO joint: {transform}")
                            
#                 except Exception as e:
#                     print(f"⚠️ No se pudo limpiar {transform}: {e}")
#         except Exception as e:
#             print(f"⚠️ Error limpiando grupos vacíos: {e}")
        
#         # ESTRATEGIA 5: LIMPIEZA PROFUNDA DE CAPAS Y SETS
#         print("🔍 Limpiando capas y sets...")
        
#         # Limpiar todas las capas de display (excepto defaultLayer)
#         display_layers = cmds.ls(type="displayLayer")
#         for layer in display_layers:
#             if layer != "defaultLayer":
#                 try:
#                     cmds.delete(layer)
#                     deleted_count += 1
#                     print(f"🗑️ Eliminada capa: {layer}")
#                 except Exception as e:
#                     print(f"⚠️ No se pudo eliminar capa {layer}: {e}")
        
#         # Limpiar sets de selección no esenciales
#         selection_sets = cmds.ls(type="objectSet")
#         for obj_set in selection_sets:
#             if obj_set != "defaultObjectSet":
#                 try:
#                     cmds.delete(obj_set)
#                     deleted_count += 1
#                     print(f"🗑️ Eliminado set: {obj_set}")
#                 except Exception as e:
#                     print(f"⚠️ No se pudo eliminar set {obj_set}: {e}")
        
#         # ESTRATEGIA 6: LIMPIAR NAMESPACES
#         print("🔍 Limpiando namespaces...")
#         try:
#             namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
#             for ns in namespaces:
#                 if ns not in ['UI', 'shared'] and not ns.startswith(':'):
#                     try:
#                         cmds.namespace(removeNamespace=ns, mergeNamespaceWithRoot=True)
#                         print(f"🗑️ Limpiado namespace: {ns}")
#                     except Exception as e:
#                         print(f"⚠️ No se pudo limpiar namespace {ns}: {e}")
#         except Exception as e:
#             print(f"⚠️ Error limpiando namespaces: {e}")
        
#         # ESTRATEGIA 7: LIMPIEZA FINAL Y RESET
#         print("🔍 Limpieza final...")
#         try:
#             # Limpiar selección
#             cmds.select(clear=True)
            
#             # Forzar actualización de la escena
#             cmds.refresh()
            
#             # Limpiar canal box
#             cmds.channelBox('mainChannelBox', edit=True, mainObjectList='')
#         except:
#             pass
        
#         # Resetear estado de los botones de la UI
#         reset_all_steps()
        
#         # Mostrar mensaje de confirmación
#         success_msg = f'<hl>🎉 RESET COMPLETO: {deleted_count} elementos eliminados</hl>'
#         cmds.inViewMessage(amg=success_msg, pos='midCenter', fade=True)
        
#         print(f"🎯 RESET ULTRA-COMPLETO EXITOSO: {deleted_count} elementos eliminados")
#         print("✨ La escena ha quedado COMPLETAMENTE LIMPIA (joints preservados)")
        
#         # Mensaje final en script editor
#         cmds.warning(f"🎯 Reset ultra-completo: {deleted_count} elementos del sistema de cola eliminados (todos los joints preservados)")
        
#     except Exception as e:
#         cmds.warning(f"⚠️ Error en reset ultra-completo: {e}")
#         traceback.print_exc()

# def reset_all_steps(*args):
#     """Reinicia solo el estado visual de los botones"""
#     for step in UI_STEPS:
#         btn = step["btn_name"]
#         if cmds.control(btn, exists=True):
#             cmds.button(btn, e=True, bgc=step["color"], label=step["label"])
#     step_status.clear()
#     print("🔄 Estado de botones reiniciado")

# def execute_all_steps_Tail():
#     try:
#         for num, func in enumerate([
#             use_existing_joints, make_curve_dynamic, create_ik_spline_handle,
#             configure_nucleus_and_follicle, create_dynamic_control,
#             create_poly_tail, create_body_and_head, create_torus_system
#         ], start=1):
#             func()
#             update_step_status(num, f"step{num}_btn")
#         cmds.inViewMessage(amg='<hl>🎉 Rig de cola completado automáticamente</hl>', pos='topCenter', fade=True)
#     except Exception as e:
#         cmds.warning(f"❌ Error en ejecución automática: {e}")
#         traceback.print_exc()

# UI_STEPS = [
#     {"num": 1, "btn_name": "step1_btn", "label": "🎯 1. CURVA BASE desde Joints", "func": use_existing_joints, "color": (0.2, 0.5, 0.8)},
#     {"num": 2, "btn_name": "step2_btn", "label": "🌀 2. DINÁMICA de Curva", "func": make_curve_dynamic, "color": (0.3, 0.6, 0.7)},
#     {"num": 3, "btn_name": "step3_btn", "label": "🎚️ 3. IK SPLINE Handle", "func": create_ik_spline_handle, "color": (0.4, 0.5, 0.6)},
#     {"num": 4, "btn_name": "step4_btn", "label": "⚛️ 4. NUCLEUS + Follicle", "func": configure_nucleus_and_follicle, "color": (0.5, 0.4, 0.7)},
#     {"num": 5, "btn_name": "step5_btn", "label": "🎮 5. CONTROL Dinámico + Root", "func": create_dynamic_control, "color": (0.7, 0.4, 0.5)},
#     {"num": 6, "btn_name": "step6_btn", "label": "🐍 6. GEOMETRÍA PolyTail + Skin", "func": create_poly_tail, "color": (0.6, 0.7, 0.3)},
#     {"num": 7, "btn_name": "step7_btn", "label": "👤 7. CUERPO + Cabeza", "func": create_body_and_head, "color": (0.8, 0.6, 0.2)},
#     {"num": 8, "btn_name": "step8_btn", "label": "⭕ 8. TOROIDE + Control Final", "func": create_torus_system, "color": (0.9, 0.5, 0.1)},
#     {"num": 9, "btn_name": "step9_btn", "label": "🚀 9. RIG COMPLETO AUTOMÁTICO", "func": execute_all_steps_Tail, "color": (0.1, 0.8, 0.3)},
# ]

# def build_ui(parent=None):
#     """Versión mejorada con mejor diseño visual"""
#     created_window = False
    
#     # Si no hay parent, crear ventana independiente
#     if parent is None:
#         if cmds.window("tailRigUI", exists=True):
#             cmds.deleteUI("tailRigUI")
#         win = cmds.window("tailRigUI", title="🐍 RIG DE COLA AVANZADO - SISTEMA MODULAR", w=450, h=520)
#         main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
#         created_window = True
#     else:
#         # Usar directamente el parent proporcionado sin crear layouts adicionales
#         main_layout = parent

#     # HEADER CON MEJOR DISEÑO
#     cmds.separator("header_sep_top", h=8, style="none", parent=main_layout)
#     cmds.text("title_banner", 
#               label="🐍 SISTEMA DE RIG DINÁMICO PARA COLA", 
#               align="center", 
#               font="boldLabelFont", 
#               h=30, 
#               backgroundColor=(0.1, 0.3, 0.5),
#               parent=main_layout)
#     cmds.text("subtitle", 
#               label="Sistema Modular Paso a Paso", 
#               align="center", 
#               font="smallBoldLabelFont", 
#               h=20, 
#               parent=main_layout)
#     cmds.separator("header_sep_bottom", h=12, style="in", parent=main_layout)

#     # SECCIÓN DE PASOS PRINCIPALES
#     cmds.text("steps_section_title", 
#               label="📋 PASOS DE CONSTRUCCIÓN", 
#               align="left", 
#               font="boldLabelFont", 
#               h=22,
#               parent=main_layout)
#     cmds.separator("steps_sep", h=5, style="single", parent=main_layout)

#     # Crear botones con colores específicos
#     for step in UI_STEPS:
#         num, btn_name, label, func, color = step["num"], step["btn_name"], step["label"], step["func"], step["color"]
        
#         # Layout para cada paso con mejor espaciado
#         step_frame = cmds.frameLayout(
#             label=f"Paso {num}", 
#             collapsable=False, 
#             marginWidth=5, 
#             marginHeight=5,
#             parent=main_layout
#         )
#         step_column = cmds.columnLayout(adjustableColumn=True, rowSpacing=2, parent=step_frame)
        
#         cmds.button(
#             btn_name, 
#             label=label, 
#             h=36, 
#             c=lambda x, n=num, f=func, b=btn_name: execute_step(n, f, b), 
#             bgc=color,
#             parent=step_column
#         )
        
#         # Tooltip informativo
#         cmds.text(
#             f"step{num}_info",
#             label=get_step_tooltip(num),
#             align="center",
#             font="smallPlainLabelFont",
#             h=16,
#             parent=step_column
#         )
        
#         cmds.setParent(main_layout)

#     cmds.separator("actions_sep", h=15, style="double", parent=main_layout)

#     # SECCIÓN DE ACCIONES AVANZADAS
#     cmds.text("actions_title", 
#               label="⚡ ACCIONES AVANZADAS", 
#               align="left", 
#               font="boldLabelFont", 
#               h=22,
#               parent=main_layout)
    
#     # Botón de RESET con diseño más llamativo
#     reset_frame = cmds.frameLayout(
#         label="🚨 LIMPIEZA TOTAL", 
#         collapsable=True, 
#         collapse=False,
#         marginWidth=8, 
#         marginHeight=8,
#         parent=main_layout
#     )
#     reset_column = cmds.columnLayout(adjustableColumn=True, rowSpacing=5, parent=reset_frame)
    
#     cmds.button(
#         "tailRig_reset_full", 
#         label="💥 RESET ULTRA-COMPLETO - LIMPIAR TODO", 
#         c=reset_tail_rig_system, 
#         bgc=(0.9, 0.2, 0.2), 
#         h=42, 
#         parent=reset_column
#     )
    
#     # Información de reset
#     cmds.text(
#         "reset_warning1", 
#         label="⚠️ ELIMINA: curvas, controles, geometría, sistemas, grupos", 
#         align="center", 
#         font="smallBoldLabelFont",
#         parent=reset_column
#     )
#     cmds.text(
#         "reset_warning2", 
#         label="🛡️ PRESERVA: Todos los joints de la escena", 
#         align="center", 
#         font="smallBoldLabelFont",
#         parent=reset_column
#     )

#     # FOOTER
#     cmds.separator("footer_sep", h=10, style="none", parent=main_layout)
#     cmds.text(
#         "footer", 
#         label="🎯 Sistema Desarrollado para Rig Avanzado", 
#         align="center", 
#         font="smallPlainLabelFont", 
#         h=18,
#         backgroundColor=(0.2, 0.2, 0.2),
#         parent=main_layout
#     )

#     if created_window:
#         cmds.showWindow(win)

# def get_step_tooltip(step_num):
#     """Retorna descripciones tooltip para cada paso"""
#     tooltips = {
#         1: "Crea curva base a partir de joints existentes en la escena",
#         2: "Convierte la curva en sistema dinámico con pelo",
#         3: "Genera handle IK Spline para animación",
#         4: "Configura sistema nucleus y follicles dinámicos",
#         5: "Crea control principal y root para todo el sistema",
#         6: "Genera geometría de cola y aplica skinning",
#         7: "Crea cuerpo y cabeza básicos para referencia",
#         8: "Sistema de control toroidal para ajustes finos",
#         9: "Ejecuta todos los pasos automáticamente"
#     }
#     return tooltips.get(step_num, "")

# def open_ui(parent=None):
#     build_ui(parent=parent)

# if __name__ == "__main__":
#     open_ui()





import maya.cmds as cmds
import traceback
from .tail_rig_curve import use_existing_joints, make_curve_dynamic
from .tail_rig_ik import create_ik_spline_handle
from .tail_rig_dynamics import configure_nucleus_and_follicle
from .tail_rig_controls import create_dynamic_control
from .tail_rig_geometry import create_poly_tail, create_body_and_head, create_torus_system

step_status = {}

def execute_step(step_num, func, button_name):
    try:
        func()
        # Solo mostrar mensaje en pantalla sin cambiar el botón
        success_msg = f'<hl>✅ Paso {step_num} completado exitosamente</hl>'
        cmds.inViewMessage(amg=success_msg, pos='midCenter', fade=True)
    except Exception as e:
        cmds.warning(f"⚠ Error ejecutando paso {step_num}: {e}")
        traceback.print_exc()

def reset_tail_rig_system(*args):
    """
    Elimina TODOS los elementos creados por el sistema de cola dinámica
    Versión ultra-agresiva que limpia TODO sin excepciones (excepto joints)
    """
    try:
        deleted_count = 0
        
        print("🧹 INICIANDO LIMPIEZA ULTRA-COMPLETA DEL SISTEMA DE COLA...")
        
        # ESTRATEGIA 1: ELIMINAR POR TIPOS DE NODO (EXCLUYENDO JOINTS)
        print("🔍 Buscando por tipos de nodo...")
        node_types = [
            "transform", "mesh", "nurbsCurve", "locator",
            "hairSystem", "nucleus", "follicle", "ikHandle", "ikEffector", 
            "ikSplineSolver", "curveInfo", "pointConstraint", "parentConstraint",
            "aimConstraint", "orientConstraint", "scaleConstraint", "decomposeMatrix",
            "multMatrix", "composeMatrix", "blendShape", "skinCluster", "cluster",
            "tweak", "nurbsTessellate", "unitConversion", "condition", "reverse",
            "multiplyDivide", "plusMinusAverage", "expression", "script", "groupId"
        ]
        
        for node_type in node_types:
            try:
                nodes = cmds.ls(type=node_type)
                for node in nodes:
                    try:
                        # EXCLUSIONES MÍNIMAS - solo lo absolutamente esencial de Maya
                        if (cmds.objExists(node) and 
                            not node.startswith('persp') and 
                            not node.startswith('top') and 
                            not node.startswith('front') and 
                            not node.startswith('side') and
                            node != "time1" and
                            node != "sequenceManager1" and
                            not node.startswith('hardware') and
                            not node.startswith('stroke') and
                            not node.startswith('default') and
                            not node.startswith('lightLinker') and
                            not node.startswith('objectSet') and
                            not node.startswith('render') and
                            not node.startswith('dof') and
                            not node.startswith('hyper') and
                            not node.startswith('solid') and
                            not node.startswith('shading') and
                            not node.startswith('lambert') and
                            not node.startswith('initial') and
                            not node.startswith('character') and
                            'skinCluster' not in node and
                            'tweak' not in node):
                            
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
        
        # ESTRATEGIA 2: ELIMINAR POR PATRONES DE NOMBRE (MUY AMPLIA)
        print("🔍 Buscando por patrones de nombre...")
        delete_patterns = [
            # Patrones ultra-amplios
            "*tail*", "*Tail*", "*TAIL*",
            "*curve*", "*Curve*", "*CURVE*", "*crv*", "*Crv*", "*CRV*",
            "*ctrl*", "*Ctrl*", "*CTRL*", "*control*", "*Control*", "*CONTROL*",
            "*driver*", "*Driver*", "*DRIVER*", "*root*", "*Root*", "*ROOT*",
            "*auto*", "*Auto*", "*AUTO*", "*master*", "*Master*", "*MASTER*",
            "*handle*", "*Handle*", "*HANDLE*", "*effector*", "*Effector*", "*EFFECTOR*",
            "*geo*", "*Geo*", "*GEO*", "*mesh*", "*Mesh*", "*MESH*", "*poly*", "*Poly*", "*POLY*",
            "*grp*", "*Grp*", "*GRP*", "*group*", "*Group*", "*GROUP*",
            "*rig*", "*Rig*", "*RIG*", "*setup*", "*Setup*", "*SETUP*",
            "*dynamic*", "*Dynamic*", "*DYNAMIC*", "*nucleus*", "*Nucleus*", "*NUCLEUS*",
            "*hair*", "*Hair*", "*HAIR*", "*follicle*", "*Follicle*", "*FOLLICLE*",
            "*foll*", "*Foll*", "*FOLL*", "*spline*", "*Spline*", "*SPLINE*",
            "*ik*", "*IK*", "*Ik*", "*skin*", "*Skin*", "*SKIN*", "*cluster*", "*Cluster*", "*CLUSTER*",
            "*blend*", "*Blend*", "*BLEND*", "*constraint*", "*Constraint*", "*CONSTRAINT*",
            "*torus*", "*Torus*", "*TORUS*", "*body*", "*Body*", "*BODY*", "*head*", "*Head*", "*HEAD*",
            "*polyTail*", "*body_geo*", "*head_geo*", "*torus_control*", "*tail_geometry*"
        ]
        
        for pattern in delete_patterns:
            try:
                # Buscar de forma MUY amplia
                objects = cmds.ls(pattern, transforms=True, shapes=True, dagObjects=True, exactType=False, long=True)
                for obj in objects:
                    try:
                        # Solo verificar que existe y no es del sistema base
                        if (cmds.objExists(obj) and 
                            not any(excluded in obj for excluded in [
                                'persp', 'top', 'front', 'side', 'time1', 
                                'sequenceManager1', 'default', 'lightLinker'
                            ])):
                            
                            # VERIFICACIÓN CRÍTICA: NO ELIMINAR JOINTS
                            if cmds.objectType(obj) != "joint":
                                cmds.delete(obj)
                                deleted_count += 1
                                print(f"🗑️ Eliminado por patrón '{pattern}': {obj}")
                            else:
                                print(f"🔒 PRESERVADO joint: {obj}")
                            
                    except Exception as e:
                        print(f"⚠️ No se pudo eliminar {obj}: {e}")
            except Exception as e:
                print(f"⚠️ Error con patrón {pattern}: {e}")
        
        # ESTRATEGIA 3: BUSCAR Y ELIMINAR TODO LO QUE CONTENGA PALABRAS CLAVE
        print("🔍 Buscando por palabras clave...")
        keywords = [
            "tail", "curve", "ctrl", "control", "driver", "root", 
            "auto", "master", "handle", "geo", "mesh", "poly", "grp", "group",
            "rig", "setup", "dynamic", "nucleus", "hair", "follicle", "foll",
            "spline", "ik", "skin", "cluster", "blend", "constraint", "torus",
            "body", "head"
        ]
        
        for keyword in keywords:
            try:
                # Buscar en ambos casos (minúsculas y mayúsculas)
                objects_lower = cmds.ls(f"*{keyword}*", transforms=True, shapes=True, dagObjects=True)
                objects_upper = cmds.ls(f"*{keyword.upper()}*", transforms=True, shapes=True, dagObjects=True)
                objects_title = cmds.ls(f"*{keyword.title()}*", transforms=True, shapes=True, dagObjects=True)
                
                all_objects = set(objects_lower + objects_upper + objects_title)
                
                for obj in all_objects:
                    try:
                        if (cmds.objExists(obj) and 
                            not any(excluded in obj for excluded in [
                                'persp', 'top', 'front', 'side', 'time1', 
                                'sequenceManager1', 'default', 'lightLinker'
                            ])):
                            
                            # VERIFICACIÓN CRÍTICA: NO ELIMINAR JOINTS
                            if cmds.objectType(obj) != "joint":
                                cmds.delete(obj)
                                deleted_count += 1
                                print(f"🗑️ Eliminado por keyword '{keyword}': {obj}")
                            else:
                                print(f"🔒 PRESERVADO joint: {obj}")
                            
                    except Exception as e:
                        print(f"⚠️ No se pudo eliminar {obj}: {e}")
            except Exception as e:
                print(f"⚠️ Error con keyword {keyword}: {e}")
        
        # ESTRATEGIA 4: ELIMINAR GRUPOS VACÍOS Y ELEMENTOS HUÉRFANOS
        print("🔍 Limpiando grupos vacíos y elementos huérfanos...")
        try:
            # Buscar todos los transforms que no tengan hijos
            all_transforms = cmds.ls(type="transform", long=True)
            for transform in all_transforms:
                try:
                    if (cmds.objExists(transform) and 
                        not any(excluded in transform for excluded in [
                            'persp', 'top', 'front', 'side', 'time1', 
                            'sequenceManager1', 'default', 'lightLinker'
                        ])):
                        
                        # VERIFICACIÓN CRÍTICA: NO ELIMINAR JOINTS
                        if cmds.objectType(transform) != "joint":
                            # Verificar si es un grupo vacío o tiene pocas conexiones
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
        
        # ESTRATEGIA 5: LIMPIEZA PROFUNDA DE CAPAS Y SETS
        print("🔍 Limpiando capas y sets...")
        
        # Limpiar todas las capas de display (excepto defaultLayer)
        display_layers = cmds.ls(type="displayLayer")
        for layer in display_layers:
            if layer != "defaultLayer":
                try:
                    cmds.delete(layer)
                    deleted_count += 1
                    print(f"🗑️ Eliminada capa: {layer}")
                except Exception as e:
                    print(f"⚠️ No se pudo eliminar capa {layer}: {e}")
        
        # Limpiar sets de selección no esenciales
        selection_sets = cmds.ls(type="objectSet")
        for obj_set in selection_sets:
            if obj_set != "defaultObjectSet":
                try:
                    cmds.delete(obj_set)
                    deleted_count += 1
                    print(f"🗑️ Eliminado set: {obj_set}")
                except Exception as e:
                    print(f"⚠️ No se pudo eliminar set {obj_set}: {e}")
        
        # ESTRATEGIA 6: LIMPIAR NAMESPACES
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
        
        # ESTRATEGIA 7: LIMPIEZA FINAL Y RESET
        print("🔍 Limpieza final...")
        try:
            # Limpiar selección
            cmds.select(clear=True)
            
            # Forzar actualización de la escena
            cmds.refresh()
            
            # Limpiar canal box
            cmds.channelBox('mainChannelBox', edit=True, mainObjectList='')
        except:
            pass
        
        # Mostrar mensaje de confirmación
        success_msg = f'<hl>🎉 RESET COMPLETO: {deleted_count} elementos eliminados</hl>'
        cmds.inViewMessage(amg=success_msg, pos='midCenter', fade=True)
        
        print(f"🎯 RESET ULTRA-COMPLETO EXITOSO: {deleted_count} elementos eliminados")
        print("✨ La escena ha quedado COMPLETAMENTE LIMPIA (joints preservados)")
        
        # Mensaje final en script editor
        cmds.warning(f"🎯 Reset ultra-completo: {deleted_count} elementos del sistema de cola eliminados (todos los joints preservados)")
        
    except Exception as e:
        cmds.warning(f"⚠️ Error en reset ultra-completo: {e}")
        traceback.print_exc()

def execute_all_steps_Tail():
    try:
        for num, func in enumerate([
            use_existing_joints, make_curve_dynamic, create_ik_spline_handle,
            configure_nucleus_and_follicle, create_dynamic_control,
            create_poly_tail, create_body_and_head, create_torus_system
        ], start=1):
            func()
            # Mostrar mensaje individual para cada paso
            success_msg = f'<hl>✅ Paso {num} completado</hl>'
            cmds.inViewMessage(amg=success_msg, pos='topCenter', fade=True)
        
        # Mensaje final de completado
        cmds.inViewMessage(amg='<hl>🎉 Rig de cola completado automáticamente</hl>', pos='midCenter', fade=True)
    except Exception as e:
        cmds.warning(f"❌ Error en ejecución automática: {e}")
        traceback.print_exc()

UI_STEPS = [
    {"num": 1, "btn_name": "step1_btn", "label": "🎯 1. CURVA BASE desde Joints", "func": use_existing_joints, "color": (0.2, 0.5, 0.8)},
    {"num": 2, "btn_name": "step2_btn", "label": "🌀 2. DINÁMICA de Curva", "func": make_curve_dynamic, "color": (0.3, 0.6, 0.7)},
    {"num": 3, "btn_name": "step3_btn", "label": "🎚️ 3. IK SPLINE Handle", "func": create_ik_spline_handle, "color": (0.4, 0.5, 0.6)},
    {"num": 4, "btn_name": "step4_btn", "label": "⚛️ 4. NUCLEUS + Follicle", "func": configure_nucleus_and_follicle, "color": (0.5, 0.4, 0.7)},
    {"num": 5, "btn_name": "step5_btn", "label": "🎮 5. CONTROL Dinámico + Root", "func": create_dynamic_control, "color": (0.7, 0.4, 0.5)},
    {"num": 6, "btn_name": "step6_btn", "label": "🐍 6. GEOMETRÍA PolyTail + Skin", "func": create_poly_tail, "color": (0.6, 0.7, 0.3)},
    {"num": 7, "btn_name": "step7_btn", "label": "👤 7. CUERPO + Cabeza", "func": create_body_and_head, "color": (0.8, 0.6, 0.2)},
    {"num": 8, "btn_name": "step8_btn", "label": "⭕ 8. TOROIDE + Control Final", "func": create_torus_system, "color": (0.9, 0.5, 0.1)},
    {"num": 9, "btn_name": "step9_btn", "label": "🚀 9. RIG COMPLETO AUTOMÁTICO", "func": execute_all_steps_Tail, "color": (0.1, 0.8, 0.3)},
]

def build_ui(parent=None):
    """Versión mejorada con mejor diseño visual y botones que mantienen su estado"""
    created_window = False
    
    # Si no hay parent, crear ventana independiente
    if parent is None:
        if cmds.window("tailRigUI", exists=True):
            cmds.deleteUI("tailRigUI")
        win = cmds.window("tailRigUI", title="🐍 RIG DE COLA AVANZADO - SISTEMA MODULAR", w=450, h=520)
        main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
        created_window = True
    else:
        # Usar directamente el parent proporcionado sin crear layouts adicionales
        main_layout = parent

    # HEADER CON MEJOR DISEÑO
    cmds.separator("header_sep_top", h=8, style="none", parent=main_layout)
    cmds.text("title_banner", 
              label="🐍 SISTEMA DE RIG DINÁMICO PARA COLA", 
              align="center", 
              font="boldLabelFont", 
              h=30, 
              backgroundColor=(0.1, 0.3, 0.5),
              parent=main_layout)
    cmds.text("subtitle", 
              label="Sistema Modular Paso a Paso", 
              align="center", 
              font="smallBoldLabelFont", 
              h=20, 
              parent=main_layout)
    cmds.separator("header_sep_bottom", h=12, style="in", parent=main_layout)

    # SECCIÓN DE PASOS PRINCIPALES
    cmds.text("steps_section_title", 
              label="📋 PASOS DE CONSTRUCCIÓN", 
              align="left", 
              font="boldLabelFont", 
              h=22,
              parent=main_layout)
    cmds.separator("steps_sep", h=5, style="single", parent=main_layout)

    # Crear botones con colores específicos - siempre mantienen su estado inicial
    for step in UI_STEPS:
        num, btn_name, label, func, color = step["num"], step["btn_name"], step["label"], step["func"], step["color"]
        
        # Layout para cada paso con mejor espaciado
        step_frame = cmds.frameLayout(
            label=f"Paso {num}", 
            collapsable=False, 
            marginWidth=5, 
            marginHeight=5,
            parent=main_layout
        )
        step_column = cmds.columnLayout(adjustableColumn=True, rowSpacing=2, parent=step_frame)
        
        cmds.button(
            btn_name, 
            label=label, 
            h=36, 
            c=lambda x, n=num, f=func, b=btn_name: execute_step(n, f, b), 
            bgc=color,
            parent=step_column
        )
        
        # Tooltip informativo
        cmds.text(
            f"step{num}_info",
            label=get_step_tooltip(num),
            align="center",
            font="smallPlainLabelFont",
            h=16,
            parent=step_column
        )
        
        cmds.setParent(main_layout)

    cmds.separator("actions_sep", h=15, style="double", parent=main_layout)

    # SECCIÓN DE ACCIONES AVANZADAS
    cmds.text("actions_title", 
              label="⚡ ACCIONES AVANZADAS", 
              align="left", 
              font="boldLabelFont", 
              h=22,
              parent=main_layout)
    
    # Botón de RESET con diseño más llamativo
    reset_frame = cmds.frameLayout(
        label="🚨 LIMPIEZA TOTAL", 
        collapsable=True, 
        collapse=False,
        marginWidth=8, 
        marginHeight=8,
        parent=main_layout
    )
    reset_column = cmds.columnLayout(adjustableColumn=True, rowSpacing=5, parent=reset_frame)
    
    cmds.button(
        "tailRig_reset_full", 
        label="💥 RESET ULTRA-COMPLETO - LIMPIAR TODO", 
        c=reset_tail_rig_system, 
        bgc=(0.9, 0.2, 0.2), 
        h=42, 
        parent=reset_column
    )
    
    # Información de reset
    cmds.text(
        "reset_warning1", 
        label="⚠️ ELIMINA: curvas, controles, geometría, sistemas, grupos", 
        align="center", 
        font="smallBoldLabelFont",
        parent=reset_column
    )
    cmds.text(
        "reset_warning2", 
        label="🛡️ PRESERVA: Todos los joints de la escena", 
        align="center", 
        font="smallBoldLabelFont",
        parent=reset_column
    )

    # FOOTER
    cmds.separator("footer_sep", h=10, style="none", parent=main_layout)
    cmds.text(
        "footer", 
        label="🎯 Sistema Desarrollado para Rig Avanzado", 
        align="center", 
        font="smallPlainLabelFont", 
        h=18,
        backgroundColor=(0.2, 0.2, 0.2),
        parent=main_layout
    )

    if created_window:
        cmds.showWindow(win)

def get_step_tooltip(step_num):
    """Retorna descripciones tooltip para cada paso"""
    tooltips = {
        1: "Crea curva base a partir de joints existentes en la escena",
        2: "Convierte la curva en sistema dinámico con pelo",
        3: "Genera handle IK Spline para animación",
        4: "Configura sistema nucleus y follicles dinámicos",
        5: "Crea control principal y root para todo el sistema",
        6: "Genera geometría de cola y aplica skinning",
        7: "Crea cuerpo y cabeza básicos para referencia",
        8: "Sistema de control toroidal para ajustes finos",
        9: "Ejecuta todos los pasos automáticamente"
    }
    return tooltips.get(step_num, "")

def open_ui(parent=None):
    build_ui(parent=parent)

if __name__ == "__main__":
    open_ui()