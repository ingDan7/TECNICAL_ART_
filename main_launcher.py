import maya.cmds as cmds
import importlib
import traceback

# =========================================================
# FUNCIONES AUXILIARES MEJORADAS
# =========================================================
def safe_reload_module(module_name):
    """Recarga el módulo de forma segura."""
    try:
        mod = importlib.import_module(module_name)
        importlib.reload(mod)
        return mod
    except Exception as e:
        cmds.warning(f"⚠️ No se pudo recargar el módulo '{module_name}': {e}")
        traceback.print_exc()
        return None

def safe_reload_and_embed(module_name, build_func="build_ui", parent_layout=None):
    """
    Recarga un módulo y dibuja su interfaz dentro de un contenedor propio.
    Versión mejorada con manejo robusto de layouts.
    """
    mod = safe_reload_module(module_name)
    if not mod or not hasattr(mod, build_func):
        cmds.warning(f"⚠️ Módulo '{module_name}' sin función '{build_func}'")
        return

    func = getattr(mod, build_func)

    # Crear contenedor con nombre único y seguro
    container_name = f"{module_name.replace('.', '_')}_container"
    
    # Limpiar contenedor previo si existe
    if cmds.columnLayout(container_name, exists=True):
        cmds.deleteUI(container_name)
    
    try:
        # Crear nuevo contenedor
        container = cmds.columnLayout(
            container_name, 
            parent=parent_layout, 
            adjustableColumn=True,
            visible=True
        )
        
        # Ejecutar función de construcción
        func(parent=container)
        print(f"✅ Interfaz cargada correctamente: {module_name}")
        
    except TypeError as e:
        # Si la UI no acepta el argumento "parent"
        if "unexpected keyword argument 'parent'" in str(e):
            cmds.warning(f"⚠️ {module_name} no acepta argumento 'parent'. Se crea sin embebido.")
            # Crear contenedor temporal
            temp_container = cmds.columnLayout(
                f"temp_{container_name}",
                parent=parent_layout,
                adjustableColumn=True
            )
            func()
            print(f"✅ Interfaz cargada (sin parent): {module_name}")
        else:
            cmds.warning(f"⚠️ Error ejecutando {module_name}: {e}")
            traceback.print_exc()
    except Exception as e:
        cmds.warning(f"⚠️ Error cargando interfaz {module_name}: {e}")
        traceback.print_exc()

# =========================================================
# INTERFAZ PRINCIPAL MEJORADA
# =========================================================
def open_main_launcher():
    """Crea la ventana principal con todas las herramientas."""
    # Cerrar ventana existente
    if cmds.window("mainRigLauncherUI", exists=True):
        cmds.deleteUI("mainRigLauncherUI")

    # Crear ventana principal
    win = cmds.window("mainRigLauncherUI", title="🎛️ Auto Rig Tools - Launcher", widthHeight=(600, 550))
    main_form = cmds.formLayout(nd=100)
    
    # Crear tabLayout
    tabs = cmds.tabLayout(
        'mainTabLayout',
        innerMarginWidth=5, 
        innerMarginHeight=5,
        parent=main_form
    )
    
    # Anclar tabLayout al formulario principal
    cmds.formLayout(
        main_form, 
        edit=True, 
        attachForm=[
            (tabs, 'top', 2), 
            (tabs, 'bottom', 2),
            (tabs, 'left', 2), 
            (tabs, 'right', 2)
        ]
    )

    # 🦿 TAB 1 - Pierna FK/IK
    tab1_form = cmds.formLayout('tab1_form', parent=tabs)
    tab1_content = cmds.scrollLayout('tab1_scroll', parent=tab1_form, cr=True)
    cmds.formLayout(tab1_form, edit=True, attachForm=[(tab1_content, 'top', 0), (tab1_content, 'bottom', 0), (tab1_content, 'left', 0), (tab1_content, 'right', 0)])
    
    safe_reload_and_embed("Auto_Chain_IKFK_001.ui_main", "build_ui", tab1_content)
    cmds.setParent('..')  # Volver a tab1_form
    cmds.setParent('..')  # Volver a tabs

    # 🧍 TAB 2 - Columna Modular
    tab2_form = cmds.formLayout('tab2_form', parent=tabs)
    tab2_content = cmds.scrollLayout('tab2_scroll', parent=tab2_form, cr=True)
    cmds.formLayout(tab2_form, edit=True, attachForm=[(tab2_content, 'top', 0), (tab2_content, 'bottom', 0), (tab2_content, 'left', 0), (tab2_content, 'right', 0)])
    
    safe_reload_and_embed("rig_Columna.ui", "build_ui", tab2_content)
    cmds.setParent('..')  # Volver a tab2_form
    cmds.setParent('..')  # Volver a tabs

    # 🐍 TAB 3 - Cola Dinámica
    tab3_form = cmds.formLayout('tab3_form', parent=tabs)
    tab3_content = cmds.scrollLayout('tab3_scroll', parent=tab3_form, cr=True)
    cmds.formLayout(tab3_form, edit=True, attachForm=[(tab3_content, 'top', 0), (tab3_content, 'bottom', 0), (tab3_content, 'left', 0), (tab3_content, 'right', 0)])
    
    safe_reload_and_embed("ChailTail.tail_rig_main", "build_ui", tab3_content)
    cmds.setParent('..')  # Volver a tab3_form
    cmds.setParent('..')  # Volver a tabs

    # 🪡 TAB 4 - ZigZag Joints
    tab4_form = cmds.formLayout('tab4_form', parent=tabs)
    tab4_content = cmds.scrollLayout('tab4_scroll', parent=tab4_form, cr=True)
    cmds.formLayout(tab4_form, edit=True, attachForm=[(tab4_content, 'top', 0), (tab4_content, 'bottom', 0), (tab4_content, 'left', 0), (tab4_content, 'right', 0)])
    
    safe_reload_and_embed("zigzag_creator.ui_zigzag", "build_ui", tab4_content)
    cmds.setParent('..')  # Volver a tab4_form
    cmds.setParent('..')  # Volver a tabs

    # Configurar etiquetas de pestañas
    cmds.tabLayout(tabs, edit=True, tabLabel=[
        (tab1_form, "🦿 Pierna FK/IK"),
        (tab2_form, "🧍 Columna Modular"),
        (tab3_form, "🐍 Cola Dinámica"),
        (tab4_form, "🪡 ZigZag Joints"),
    ])

    # Mostrar ventana
    cmds.showWindow(win)
    print("✅ Auto Rig Launcher abierto correctamente.")

# =========================================================
# AUTOEJECUCIÓN
# =========================================================
if __name__ == "__main__":
    open_main_launcher()

    