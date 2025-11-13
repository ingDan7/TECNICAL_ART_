
# # import sys
# # import importlib

# # PROJECT_PATH = r"C:\Users\danie\vscode-environment-for-maya"
# # MODULE_NAME = "Auto_Chain_IKFK_001"

# # if PROJECT_PATH not in sys.path:
# #     sys.path.append(PROJECT_PATH)

# # # Forzar recarga limpia (evita caché)
# # sys.modules.pop("Auto_Chain_IKFK_001", None)
# # sys.modules.pop("Auto_Chain_IKFK_001.ui", None)

# # if MODULE_NAME in sys.modules:
# #     print(f"🔄 Recargando {MODULE_NAME}...")
# #     importlib.reload(sys.modules[MODULE_NAME])
# # else:
# #     print(f"📥 Importando {MODULE_NAME}...")
# #     importlib.import_module(MODULE_NAME)

# # import Auto_Chain_IKFK_001.ui_main as rig
# # rig.open_leg_rig_ui()  # 👈 cambias aquí


# # import sys
# # import importlib

# # # Ruta a tu proyecto
# # PROJECT_PATH = r"C:\Users\danie\vscode-environment-for-maya"
# # MODULE_NAME = "rig_Columna"

# # # Añadir la ruta si no existe
# # if PROJECT_PATH not in sys.path:
# #     sys.path.append(PROJECT_PATH)

# # # Forzar recarga limpia (evita caché)
# # sys.modules.pop("rig_Columna", None)
# # sys.modules.pop("rig_Columna.ui", None)

# # # Recargar o importar el módulo principal
# # if MODULE_NAME in sys.modules:
# #     print(f"🔄 Recargando {MODULE_NAME}...")
# #     importlib.reload(sys.modules[MODULE_NAME])
# # else:
# #     print(f"📥 Importando {MODULE_NAME}...")
# #     importlib.import_module(MODULE_NAME)

# # # 👇 Importamos desde el submódulo ui.py dentro de rig_Columna
# # import rig_Columna.ui as rig

# # # 👇 Abrimos la interfaz de la columna
# # rig.open_spine_ui()




# # import sys
# # import importlib

# # # Ruta a tu proyecto ChailTail
# # PROJECT_PATH = r"C:\Users\danie\vscode-environment-for-maya\ChailTail"
# # MODULE_NAME = "tail_rig_main"

# # # Añadir la ruta si no existe
# # if PROJECT_PATH not in sys.path:
# #     sys.path.append(PROJECT_PATH)
# #     print(f"📁 Ruta añadida: {PROJECT_PATH}")

# # # Forzar recarga limpia (evita caché)
# # modules_to_clean = [
# #     "tail_rig_main", 
# #     "tail_rig_curve", 
# #     "tail_rig_ik", 
# #     "tail_rig_dynamics", 
# #     "tail_rig_controls", 
# #     "tail_rig_geometry"
# # ]

# # for module_name in modules_to_clean:
# #     sys.modules.pop(module_name, None)
# #     print(f"🧹 Limpiando módulo: {module_name}")

# # try:
# #     # Recargar o importar el módulo principal
# #     if MODULE_NAME in sys.modules:
# #         print(f"🔄 Recargando {MODULE_NAME}...")
# #         importlib.reload(sys.modules[MODULE_NAME])
# #     else:
# #         print(f"📥 Importando {MODULE_NAME}...")
# #         importlib.import_module(MODULE_NAME)

# #     import sys
# #     sys.path.append(r"C:\Users\danie\vscode-environment-for-maya")

# #     import ChailTail
# #     ChailTail.open_ui()


# # except Exception as e:
# #     print(f"❌ Error al cargar ChailTail: {e}")
# #     import traceback
# #     traceback.print_exc()



# import sys
# import importlib

# # Ruta al directorio padre de ChailTail
# PROJECT_PATH = r"C:\Users\danie\vscode-environment-for-maya"

# if PROJECT_PATH not in sys.path:
#     sys.path.append(PROJECT_PATH)
#     print(f"📁 Ruta añadida: {PROJECT_PATH}")

# # Forzar recarga limpia de submódulos
# modules_to_clean = [
#     "ChailTail.tail_rig_main", 
#     "ChailTail.tail_rig_curve", 
#     "ChailTail.tail_rig_ik", 
#     "ChailTail.tail_rig_dynamics", 
#     "ChailTail.tail_rig_controls", 
#     "ChailTail.tail_rig_geometry"
# ]

# for module_name in modules_to_clean:
#     sys.modules.pop(module_name, None)
#     print(f"🧹 Limpiando módulo: {module_name}")

# try:
#     import ChailTail
#     importlib.reload(ChailTail)  # recarga el paquete completo

#     print("🚀 Iniciando interfaz de ChailTail...")
#     ChailTail.open_ui()

# except Exception as e:
#     print(f"❌ Error al cargar ChailTail: {e}")
#     import traceback
#     traceback.print_exc()


import sys
import importlib
import os

#PROJECT_PATH = r"C:\Users\danie\vscode-environment-for-maya\Carros"
PROJECT_PATH = r"C:\Users\pc\Documents\Repositorios\TECNICAL_ART_"
MODULE_NAME = "Carros"

def reload_carros_modules():
    """Recarga todos los módulos de Carros manteniendo las referencias"""
    print("=" * 60)
    print("🔄 DEBUG - RECARGANDO MÓDULOS CARROS")
    print("=" * 60)
    
    # Verificar y agregar path
    print(f"📁 PROJECT_PATH: {PROJECT_PATH}")
    if PROJECT_PATH not in sys.path:
        sys.path.append(PROJECT_PATH)
        print("✅ Ruta agregada a sys.path")
    
    # Encontrar todos los módulos de Carros
    carros_modules = []
    for module_name in list(sys.modules.keys()):
        if module_name and ("Carros" in module_name or module_name.startswith("Carros")):
            carros_modules.append(module_name)
    
    print(f"📦 Módulos Carros encontrados: {len(carros_modules)}")
    for module_name in carros_modules:
        print(f"   - {module_name}")
    
    # Recargar módulos en orden inverso (dependencias primero)
    carros_modules.sort(reverse=True)
    
    reloaded_modules = []
    for module_name in carros_modules:
        try:
            module = sys.modules[module_name]
            if hasattr(module, '__file__') and module.__file__:
                importlib.reload(module)
                reloaded_modules.append(module_name)
                print(f"✅ Recargado: {module_name}")
        except Exception as e:
            print(f"⚠️  No se pudo recargar {module_name}: {e}")
    
    # Importar módulo principal si no estaba cargado
    try:
        if MODULE_NAME not in sys.modules:
            main_module = importlib.import_module(MODULE_NAME)
            print(f"✅ Importado nuevo: {MODULE_NAME}")
        else:
            main_module = importlib.reload(sys.modules[MODULE_NAME])
            print(f"✅ Recargado principal: {MODULE_NAME}")
            
        return main_module
    except Exception as e:
        print(f"❌ Error cargando módulo principal: {e}")
        import traceback
        traceback.print_exc()
        return None

def open_chasis_ui():
    """Abre la interfaz de chasis con los módulos recargados"""
    try:
        # Recargar todos los módulos
        main_module = reload_carros_modules()
        
        if main_module is None:
            print("❌ No se pudo cargar el módulo principal")
            return
        
        # Importar y ejecutar UI
        from Carros import ui_builder
        print(f"📍 ui_builder cargado desde: {ui_builder.__file__}")
        
        # Cerrar UI existente si está abierta
        close_existing_ui()
        
        print("🎯 Ejecutando open_chasis_ui()...")
        ui_builder.open_chasis_ui()
        
        print("✅ Interfaz ejecutada correctamente con módulos actualizados")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def close_existing_ui():
    """Cierra cualquier instancia previa de la UI"""
    try:
        # Buscar y cerrar ventanas existentes de chasis
        if 'ui_builder' in sys.modules:
            ui_builder = sys.modules['ui_builder']
            if hasattr(ui_builder, 'chasis_window') and ui_builder.chasis_window:
                try:
                    ui_builder.chasis_window.deleteLater()
                    print("🗑️ Ventana anterior cerrada")
                except:
                    pass
            ui_builder.chasis_window = None
    except Exception as e:
        print(f"⚠️  Error cerrando UI anterior: {e}")

# Ejecutar directamente
if __name__ == "__main__":
    open_chasis_ui()
    print("=" * 60)