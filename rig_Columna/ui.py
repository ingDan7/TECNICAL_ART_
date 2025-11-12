import maya.cmds as cmds
import traceback
from . import joints, locators, controls, targets

def show_message(msg, success=True):
    color = (0.2, 0.8, 0.2) if success else (0.9, 0.4, 0.2)
    cmds.inViewMessage(amg=f"<hl>{msg}</hl>", pos='midCenter', fade=True, fadeStayTime=1500, backColor=color, fadeOutTime=1000)

def reset_spine_rig(*args):
    """
    Elimina TODOS los elementos creados por el sistema de columna modular
    POR TIPOS DE NODO específicos para una limpieza más precisa
    """
    try:
        deleted_count = 0
        
        print("🧹 INICIANDO LIMPIEZA POR TIPOS DE NODO - SISTEMA DE COLUMNA...")
        
        # ESTRATEGIA PRINCIPAL: ELIMINAR POR TIPOS DE NODO
        print("🔍 Eliminando por tipos de nodo...")
        
        # Lista de tipos de nodo a eliminar
        node_types_to_delete = [
            # Sistemas y dinámicas
            "hairSystem", "nucleus", "follicle",
            # IK y handles
            "ikHandle", "ikEffector", "ikSplineSolver",
            # Constraints
            "pointConstraint", "aimConstraint", "parentConstraint", 
            "orientConstraint", "scaleConstraint", "matrixConstraint",
            # Nodos de matriz y matemáticas
            "decomposeMatrix", "multMatrix", "composeMatrix", 
            "multiplyDivide", "plusMinusAverage", "reverse", "condition",
            # Información de curvas y medidas
            "curveInfo", "pointOnCurveInfo", "motionPath", 
            "closestPoint", "distanceDimension",
            # Clusters y deformadores
            "cluster", "skinCluster", "tweak", "blendShape",
            # Locators
            "locator",
            # Curvas
            "nurbsCurve",
            # Scripts y expresiones
            "expression", "script",
            # Grupos y sets
            "objectSet", "groupId"
        ]
        
        for node_type in node_types_to_delete:
            try:
                nodes = cmds.ls(type=node_type)
                for node in nodes:
                    try:
                        # Solo eliminar si existe y no es del sistema por defecto
                        if (cmds.objExists(node) and 
                            not node.startswith('persp') and 
                            not node.startswith('top') and 
                            not node.startswith('front') and 
                            not node.startswith('side') and
                            node != "time1" and
                            node != "sequenceManager1" and
                            not node.startswith('defaultLightSet') and
                            not node.startswith('defaultObjectSet') and
                            not node.startswith('lightLinker')):
                            
                            cmds.delete(node)
                            deleted_count += 1
                            print(f"🗑️ Eliminado por tipo {node_type}: {node}")
                            
                    except Exception as e:
                        print(f"⚠️ No se pudo eliminar {node}: {e}")
            except Exception as e:
                print(f"⚠️ Error con tipo {node_type}: {e}")
        
        # ESTRATEGIA SECUNDARIA: ELIMINAR TRANSFORMS POR PATRONES ESPECÍFICOS
        print("🔍 Eliminando transforms por patrones específicos...")
        
        transform_patterns = [
            # Joints del sistema de columna
            "*_spine_joint*", "*_spine_*_joint*", "*_joint_00*",
            "*_root_joint*", "*_base_joint*", "*_pelvis_joint*",
            "*_chest_joint*", "*_neck_joint*", "*_head_joint*",
            # Locators
            "*_locator*", "*_LOC_*", "*_loc_*", "*_pointLocator*",
            # Controles
            "*_IK_ctrl*", "*_IK_handle*", "*_IK_offset*", "*_IK_auto*",
            "*_ctrl*", "*_control*", "*_CTRL*", "*_driver*", "*_auto*",
            # Targets
            "*_target*", "*_TGT_*", "*_aimTarget*", "*_pointTarget*",
            # Grupos de organización
            "*_SPINE_IK_CTRLS*", "*_SPINE_LOCATORS*", "*_SPINE_TARGETS*",
            "*_SPINE_RIG*", "*_SPINE_GRP*", "*_RIG_GRP*", "*_CONTROLS_GRP*",
            "*_AUTO_GRP*", "*_ZERO_GRP*", "*_OFFSET_GRP*", "*_SETUP_GRP*",
            # Curvas específicas
            "spine_curve*", "spine_base_curve*", "*_spine_crv*",
            "splineCurve*"
        ]
        
        for pattern in transform_patterns:
            try:
                objects = cmds.ls(pattern, type="transform")
                for obj in objects:
                    try:
                        if (cmds.objExists(obj) and 
                            not obj.startswith('persp') and 
                            not obj.startswith('top') and 
                            not obj.startswith('front') and 
                            not obj.startswith('side')):
                            
                            cmds.delete(obj)
                            deleted_count += 1
                            print(f"🗑️ Eliminado transform: {obj}")
                            
                    except Exception as e:
                        print(f"⚠️ No se pudo eliminar {obj}: {e}")
            except Exception as e:
                print(f"⚠️ Error con patrón {pattern}: {e}")
        
        # ESTRATEGIA 3: ELIMINAR SHAPES HUÉRFANOS
        print("🔍 Limpiando shapes huérfanos...")
        try:
            all_shapes = cmds.ls(type=["nurbsCurve", "mesh", "locator"])
            for shape in all_shapes:
                try:
                    # Verificar si el shape está huérfano (no tiene transform padre)
                    parents = cmds.listRelatives(shape, parent=True) or []
                    if not parents:
                        cmds.delete(shape)
                        deleted_count += 1
                        print(f"🗑️ Eliminado shape huérfano: {shape}")
                except Exception as e:
                    print(f"⚠️ No se pudo eliminar shape {shape}: {e}")
        except Exception as e:
            print(f"⚠️ Error limpiando shapes: {e}")
        
        # ESTRATEGIA 4: LIMPIEZA DE GRUPOS VACÍOS
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
                        
                        # Verificar si es un grupo vacío
                        children = cmds.listRelatives(transform, children=True, fullPath=True) or []
                        shapes = cmds.listRelatives(transform, shapes=True, fullPath=True) or []
                        
                        if len(children) == 0 and len(shapes) == 0:
                            # Verificar que no sea un joint
                            if cmds.objectType(transform) != "joint":
                                cmds.delete(transform)
                                deleted_count += 1
                                print(f"🗑️ Eliminado grupo vacío: {transform}")
                                
                except Exception as e:
                    print(f"⚠️ No se pudo limpiar {transform}: {e}")
        except Exception as e:
            print(f"⚠️ Error limpiando grupos vacíos: {e}")
        
        # ESTRATEGIA 5: LIMPIEZA DE CAPAS DE DISPLAY
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
        
        # ESTRATEGIA 7: LIMPIEZA FINAL
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
        show_message(f"✅ Reset por Tipos Completado: {deleted_count} elementos eliminados")
        print(f"🎯 RESET POR TIPOS EXITOSO: {deleted_count} elementos eliminados")
        print("✨ La escena ha quedado completamente limpia (eliminación por tipos)")
        
    except Exception as e:
        show_message(f"⚠️ Error en reset por tipos: {e}", success=False)
        traceback.print_exc()

def ui_create_joints_and_curve(*args):
    try:
        joints.create_spine_joints_and_curve(open_curve=True)
        show_message("✅ Joints y curva creados correctamente")
    except Exception as e:
        show_message(f"⚠️ Error creando joints: {e}", success=False)
        traceback.print_exc()

def ui_create_locators_and_connect(*args):
    try:
        locators.create_and_connect_locators_to_curve()
        show_message("✅ Locators creados y conectados")
    except Exception as e:
        show_message(f"⚠️ Error con locators: {e}", success=False)
        traceback.print_exc()

def ui_decompose_matrix(*args):
    try:
        locators.connect_locators_with_decompose()
        show_message("✅ DecomposeMatrix conectado correctamente")
    except Exception as e:
        show_message(f"⚠️ Error en DecomposeMatrix: {e}", success=False)
        traceback.print_exc()

def ui_organize_controls(*args):
    try:
        controls.organize_spine_ik_controls()
        show_message("✅ Controles IK organizados")
    except Exception as e:
        show_message(f"⚠️ Error organizando controles: {e}", success=False)
        traceback.print_exc()

def ui_create_targets(*args):
    try:
        targets.create_targets_on_curve()
        show_message("✅ Targets creados correctamente")
    except Exception as e:
        show_message(f"⚠️ Error creando targets: {e}", success=False)
        traceback.print_exc()

def ui_aim_constraints(*args):
    try:
        targets.redirect_targets_with_aim()
        show_message("✅ Aim Constraints aplicados")
    except Exception as e:
        show_message(f"⚠️ Error aplicando Aim Constraints: {e}", success=False)
        traceback.print_exc()

def ui_parent_targets_to_joints(*args):
    try:
        targets.parent_constraint_joints_to_targets()
        show_message("✅ Targets conectados a Joints")
    except Exception as e:
        show_message(f"⚠️ Error en parent constraint: {e}", success=False)
        traceback.print_exc()

def build_ui(parent=None):
    """Versión corregida que maneja correctamente el parámetro parent"""
    created_window = False
    
    # Si no hay parent, crear ventana independiente
    if parent is None:
        if cmds.window("spineRigUI", exists=True):
            cmds.deleteUI("spineRigUI")
        win = cmds.window("spineRigUI", title="🦴 Rig Columna Modular", widthHeight=(450, 480), sizeable=True)
        main_layout = cmds.columnLayout(adjustableColumn=True)
        created_window = True
    else:
        # Usar directamente el parent proporcionado sin crear layouts adicionales
        main_layout = parent

    # CONTENIDO DE LA UI - crear elementos directamente en el layout proporcionado
    cmds.text("spine_title", label="🧍‍♂️  Auto Rig Columna Modular", height=35, align="center", bgc=(0.1,0.1,0.1), parent=main_layout)
    cmds.separator("spine_sep1", h=10, style="in", parent=main_layout)

    # BOTONES DE FUNCIONALIDAD
    cmds.button("spine_btn1", label="(1) 🧩 Crear Joints + Curva", c=ui_create_joints_and_curve, bgc=(0.1,0.7,0.9), h=36, parent=main_layout)
    cmds.button("spine_btn2", label="(2) 📍 Locators + Conectar", c=ui_create_locators_and_connect, bgc=(0.4,0.9,0.5), h=36, parent=main_layout)
    cmds.button("spine_btn3", label="(3) 🔄 DecomposeMatrix", c=ui_decompose_matrix, bgc=(0.8,0.6,0.2), h=36, parent=main_layout)
    cmds.separator("spine_sep2", h=8, style="in", parent=main_layout)
    cmds.button("spine_btn4", label="(4) 🎛️ Organizar Controles IK", c=ui_organize_controls, bgc=(0.6,0.4,0.9), h=36, parent=main_layout)
    cmds.separator("spine_sep3", h=8, style="in", parent=main_layout)
    cmds.button("spine_btn5", label="(5) 🎯 Crear Targets", c=ui_create_targets, bgc=(0.9,0.4,0.4), h=36, parent=main_layout)
    cmds.button("spine_btn6", label="(6) 🧭 Aim Constraints", c=ui_aim_constraints, bgc=(0.9,0.7,0.3), h=36, parent=main_layout)
    cmds.button("spine_btn7", label="(7) 🔗 Parent Targets → Joints", c=ui_parent_targets_to_joints, bgc=(0.3,0.8,0.9), h=40, parent=main_layout)

    cmds.separator("spine_sep4", h=10, style="in", parent=main_layout)
    
    # BOTÓN DE RESET COMPLETO - ACTUALIZADO
    cmds.button("spine_reset_btn", label="🗑️ RESET POR TIPOS - Limpiar TODO", c=reset_spine_rig, bgc=(0.9, 0.2, 0.2), h=40, parent=main_layout)
    
    cmds.separator("spine_sep5", h=10, style="in", parent=main_layout)
    
    # TEXTO INFORMATIVO ACTUALIZADO
    cmds.text("spine_reset_info", label="⚠️ ELIMINACIÓN POR TIPOS: Constraints, IK, Locators,\n    Curvas, Deformers, Grupos, etc.", align="center", parent=main_layout)
    cmds.text("spine_reset_warning", label="💡 Limpieza precisa por tipos de nodo Maya", align="center", parent=main_layout)
    cmds.separator("spine_sep6", h=8, style="in", parent=main_layout)
    cmds.text("spine_tip", label="💡 Elimina por tipo específico, no solo por nombre", align="center", parent=main_layout)

    if created_window:
        cmds.showWindow(win)

def open_spine_ui(parent=None):
    build_ui(parent=parent)

if __name__ == "__main__":
    open_spine_ui()