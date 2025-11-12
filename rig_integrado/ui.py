import maya.cmds as cmds
import traceback

# Variables globales para trackear el estado de cada rig
rig_states = {
    "leg": False,
    "spine": False, 
    "tail": False
}

# Colores para los diferentes estados
COLOR_GRAY = [0.3, 0.3, 0.3]  # Gris (inactivo)
COLOR_COMPLETE = [0.2, 0.6, 0.4]  # Verde (completado)
def update_button_colors():
    """Actualiza los colores de los botones basado en el estado actual"""
    try:
        # Actualizar botón de pierna
        if cmds.button("btn_leg", exists=True):
            color = COLOR_COMPLETE if rig_states["leg"] else COLOR_GRAY
            cmds.button("btn_leg", edit=True, backgroundColor=color)
        
        # Actualizar botón de columna
        if cmds.button("btn_spine", exists=True):
            color = COLOR_COMPLETE if rig_states["spine"] else COLOR_GRAY
            cmds.button("btn_spine", edit=True, backgroundColor=color)
        
        # Actualizar botón de cola
        if cmds.button("btn_tail", exists=True):
            color = COLOR_COMPLETE if rig_states["tail"] else COLOR_GRAY
            cmds.button("btn_tail", edit=True, backgroundColor=color)
            
    except Exception as e:
        print(f"⚠️ Error actualizando colores: {e}")

def execute_all_steps_IK():
    try:
        from rigIK_02 import execute_all_steps_IK as leg_func
        print("🦵 Ejecutando Rig de Pierna...")
        result = leg_func()
        if result:
            rig_states["leg"] = True
            update_button_colors()
            cmds.inViewMessage(amg='<span style="color:#7FFF7F;">✅ Rig de Pierna completado</span>', pos='topCenter', fade=True, fst=1500, ft=200)
        return result
    except Exception as e:
        cmds.warning(f"❌ Error en rig de pierna: {str(e)}")
        return False

def execute_all_steps():
    try:
        from rig_Columna_02 import execute_all_steps as spine_func
        print("📏 Ejecutando Rig de Columna...")
        result = spine_func()
        if result:
            rig_states["spine"] = True
            update_button_colors()
            cmds.inViewMessage(amg='<span style="color:#7FFF7F;">✅ Rig de Columna completado</span>', pos='topCenter', fade=True, fst=1500, ft=200)
        return result
    except Exception as e:
        cmds.warning(f"❌ Error en rig de columna: {str(e)}")
        return False

def execute_all_steps_Tail():
    try:
        from rig_Cola import execute_all_steps_Tail as tail_func
        print("🦎 Ejecutando Rig de Cola...")
        result = tail_func()
        if result:
            rig_states["tail"] = True
            update_button_colors()
            cmds.inViewMessage(amg='<span style="color:#7FFF7F;">✅ Rig de Cola completado</span>', pos='topCenter', fade=True, fst=1500, ft=200)
        return result
    except Exception as e:
        cmds.warning(f"❌ Error en rig de cola: {str(e)}")
        return False

def cleanup_all_rigs_OPTIMIZED():
    """🚀 VERSIÓN OPTIMIZADA - Limpieza rápida de todos los rigs"""
    try:
        print("🧹 INICIANDO LIMPIEZA COMPLETA OPTIMIZADA...")
        
        # 🔥 ESTRATEGIA: Agrupar por TIPO en lugar de por patrón
        # Esto reduce drásticamente el número de operaciones
        
        # 1. Primero recolectar TODOS los objetos a eliminar
        all_objects_to_delete = []
        
        # Patrones principales (una sola búsqueda por patrón)
        patterns_to_delete = [
            # Rig de Pierna
            "*_practice_L_*",  # 🔥 UN solo patrón para todo el rig de pierna
            "Leg_practice_L_attributes_*",
            "FKIK_reverse",
            
            # Rig de Columna  
            "spine*",  # 🔥 UN solo patrón para spine
            "pointOnCurveInfo_*",
            "splineCurve_*",
            "*_dm",
            
            # Rig de Cola
            "joint_IK_*",
            "dynamic_*",  # 🔥 UN solo patrón para dynamic
            "poly*",      # 🔥 UN solo patrón para poly
            "driverPlane_*",
            
            # Sistemas
            "hairSystem*",
            "follicle*", 
            "nucleus*",
            "nRigid*",
            "nCloth*",
            "IK_Spine_Handle"
        ]
        
        # Recolectar objetos por patrones (OPERACIÓN ÚNICA)
        for pattern in patterns_to_delete:
            all_objects_to_delete.extend(cmds.ls(pattern) or [])
        
        # 2. Recolectar por TIPO (más eficiente que por nombre)
        object_types_to_delete = [
            'parentConstraint', 'pointConstraint', 'orientConstraint', 
            'aimConstraint', 'poleVectorConstraint', 'scaleConstraint',
            'skinCluster', 'ikHandle', 'ikEffector'
        ]
        
        for obj_type in object_types_to_delete:
            all_objects_to_delete.extend(cmds.ls(type=obj_type) or [])
        
        # 3. 🔥 ELIMINAR EN LOTES - Agrupar por tipo para eliminación masiva
        if all_objects_to_delete:
            # Eliminar duplicados
            all_objects_to_delete = list(set(all_objects_to_delete))
            
            print(f"🎯 Eliminando {len(all_objects_to_delete)} objetos...")
            
            # Intentar eliminar todo de una vez
            try:
                cmds.delete(all_objects_to_delete)
                print(f"✅ Eliminación masiva completada: {len(all_objects_to_delete)} objetos")
            except:
                # Si falla la eliminación masiva, hacer por lotes más pequeños
                print("⚠️ Eliminación masiva falló, usando eliminación por lotes...")
                batch_size = 50
                for i in range(0, len(all_objects_to_delete), batch_size):
                    batch = all_objects_to_delete[i:i + batch_size]
                    try:
                        cmds.delete(batch)
                        print(f"📦 Lote {i//batch_size + 1}: {len(batch)} objetos")
                    except Exception as batch_error:
                        print(f"⚠️ Error en lote {i//batch_size + 1}: {batch_error}")
        
        # 4. Limpieza de joints (preservar originales)
        original_joints = cmds.ls("joint_*", type="joint")
        joints_renamed = 0
        
        for joint in original_joints:
            try:
                # Solo renombrar si tiene sufijos numéricos
                if any(suffix in joint for suffix in ["_001", "_002", "_003"]):
                    clean_name = joint.replace("_001", "").replace("_002", "").replace("_003", "")
                    if not cmds.objExists(clean_name):
                        cmds.rename(joint, clean_name)
                        joints_renamed += 1
            except:
                pass
        
        if joints_renamed > 0:
            print(f"🔄 {joints_renamed} joints renombrados")
        
        # 🔥 RESETEAR ESTADOS después de limpiar
        rig_states["leg"] = False
        rig_states["spine"] = False
        rig_states["tail"] = False
        update_button_colors()
        
        # Mensaje final optimizado
        total_deleted = len(all_objects_to_delete)
        cmds.inViewMessage(
            amg=f'<span style="color:#7FFF7F;">🧹 Optimizado: {total_deleted} elementos</span>',
            pos='topCenter', fade=True, fst=1500, ft=150
        )
        
        print(f"✅ LIMPIEZA OPTIMIZADA COMPLETADA")
        print(f"🎯 Total procesado: {total_deleted} elementos")
        
        # 🔥 FORZAR actualización de la vista
        cmds.refresh()
        
        return True
        
    except Exception as e:
        cmds.warning(f"❌ Error en limpieza optimizada: {str(e)}")
        return False

def open_spine_ui_OPTIMIZED():
    """🚀 Interfaz optimizada con botones que cambian de color"""
    try:
        if cmds.window("rigsControl", exists=True):
            cmds.deleteUI("rigsControl")
        
        # 🔥 UI más liviana
        win = cmds.window("rigsControl", title="Control Rigs - CON ESTADO", width=380, height=400)
        main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=6)
        
        # Título simple
        cmds.text(label="SISTEMA DE RIGS", font="boldLabelFont", height=25)
        cmds.separator(height=8, style='in')
        
        # Estado actual
        cmds.text(label="Gris = No ejecutado | Color = Completado", height=20, font="smallPlainLabelFont")
        cmds.separator(height=5, style='none')
        
        # Botones con colores que cambian según el estado
        cmds.button("btn_leg", label=" RIG PIERNA", height=40, 
                   backgroundColor=COLOR_GRAY,
                   command=lambda x: execute_all_steps_IK())
        
        cmds.button("btn_spine", label=" RIG COLUMNA", height=40,
                   backgroundColor=COLOR_GRAY, 
                   command=lambda x: execute_all_steps())
        
        cmds.button("btn_tail", label=" RIG COLA", height=40,
                   backgroundColor=COLOR_GRAY,
                   command=lambda x: execute_all_steps_Tail())
        
        cmds.separator(height=12, style='in')
        
        # 🔥 BOTÓN DE LIMPIEZA (siempre en color rojo)
        cmds.button(label=" LIMPIAR RIG", height=42, 
                   backgroundColor=COLOR_COMPLETE,
                   command=lambda x: cleanup_all_rigs_OPTIMIZED())
        
        cmds.separator(height=8, style='in')
        
        # Información mínima
        cmds.text(label="Ctrl+R: Recargar interfaz", height=18, font="smallPlainLabelFont")
        
        cmds.showWindow(win)
        print("✅ Interfaz con estados cargada")
        
    except Exception as e:
        cmds.warning(f"❌ Error en interfaz: {str(e)}")

# 🔥 MANTENER compatibilidad
def open_spine_ui():
    open_spine_ui_OPTIMIZED()

def cleanup_all_rigs():
    cleanup_all_rigs_OPTIMIZED()