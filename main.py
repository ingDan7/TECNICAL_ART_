
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

# import sys
# import importlib
# import os
# import gc

# PROJECT_PATH = r"C:\Users\danie\vscode-environment-for-maya\Carros"
# MODULE_NAME = "Carros"

# def reload_carros_modules():
#     """Recarga todos los módulos de Carros de manera más robusta"""
#     print("=" * 60)
#     print("🔄 DEBUG - RECARGANDO MÓDULOS CARROS")
#     print("=" * 60)
    
#     # Verificar y agregar path
#     print(f"📁 PROJECT_PATH: {PROJECT_PATH}")
#     if PROJECT_PATH not in sys.path:
#         sys.path.insert(0, PROJECT_PATH)  # Insertar al inicio para prioridad
#         print("✅ Ruta agregada a sys.path")
    
#     # Encontrar todos los módulos de Carros
#     carros_modules = []
#     for module_name in list(sys.modules.keys()):
#         if module_name and ("Carros" in module_name or module_name.startswith("Carros")):
#             carros_modules.append(module_name)
    
#     print(f"📦 Módulos Carros encontrados: {len(carros_modules)}")
#     for module_name in carros_modules:
#         print(f"   - {module_name}")
    
#     # Recargar módulos en orden inverso (dependencias primero)
#     carros_modules.sort(reverse=True)
    
#     reloaded_modules = []
#     failed_modules = []
    
#     # Primera pasada: intentar recargar
#     for module_name in carros_modules:
#         try:
#             if module_name in sys.modules:
#                 module = sys.modules[module_name]
#                 importlib.reload(module)
#                 reloaded_modules.append(module_name)
#                 print(f"✅ Recargado: {module_name}")
#         except Exception as e:
#             print(f"⚠️  No se pudo recargar {module_name}: {e}")
#             failed_modules.append(module_name)
    
#     # Segunda pasada: para módulos que fallaron, eliminar y reimportar
#     for module_name in failed_modules:
#         try:
#             if module_name in sys.modules:
#                 # Eliminar del sys.modules
#                 del sys.modules[module_name]
#                 print(f"🗑️  Eliminado de cache: {module_name}")
                
#                 # Forzar garbage collection
#                 gc.collect()
                
#                 # Reimportar
#                 new_module = importlib.import_module(module_name)
#                 reloaded_modules.append(module_name)
#                 print(f"✅ Reimportado: {module_name}")
#         except Exception as e:
#             print(f"❌ Error crítico con {module_name}: {e}")
    
#     # Importar módulo principal si no estaba cargado
#     try:
#         if MODULE_NAME not in sys.modules:
#             main_module = importlib.import_module(MODULE_NAME)
#             print(f"✅ Importado nuevo: {MODULE_NAME}")
#         else:
#             main_module = importlib.reload(sys.modules[MODULE_NAME])
#             print(f"✅ Recargado principal: {MODULE_NAME}")
            
#         return main_module
#     except Exception as e:
#         print(f"❌ Error cargando módulo principal: {e}")
#         import traceback
#         traceback.print_exc()
#         return None

# def cleanup_module_references():
#     """Limpia referencias específicas problemáticas"""
#     try:
#         # Limpiar referencias específicas que puedan causar conflictos
#         modules_to_clean = ['ui_builder', 'chasis_controller', 'car_utils']
        
#         for module_name in modules_to_clean:
#             full_name = f"Carros.{module_name}"
#             if full_name in sys.modules:
#                 # Guardar referencia antes de eliminar
#                 old_module = sys.modules[full_name]
                
#                 # Eliminar del sys.modules
#                 del sys.modules[full_name]
                
#                 # Limpiar atributos específicos si existen
#                 if hasattr(old_module, 'chasis_window'):
#                     try:
#                         old_module.chasis_window = None
#                     except:
#                         pass
                
#                 print(f"🧹 Limpiada referencia: {full_name}")
        
#         # Forzar garbage collection
#         gc.collect()
        
#     except Exception as e:
#         print(f"⚠️  Error en cleanup: {e}")

# def open_chasis_ui():
#     """Abre la interfaz de chasis con los módulos recargados"""
#     try:
#         # Limpiar referencias antiguas primero
#         cleanup_module_references()
        
#         # Recargar todos los módulos
#         main_module = reload_carros_modules()
        
#         if main_module is None:
#             print("❌ No se pudo cargar el módulo principal")
#             return
        
#         # Cerrar UI existente si está abierta
#         close_existing_ui()
        
#         # Importar y ejecutar UI después de la recarga
#         from Carros import ui_builder
#         print(f"📍 ui_builder cargado desde: {ui_builder.__file__}")
        
#         print("🎯 Ejecutando open_chasis_ui()...")
#         ui_builder.open_chasis_ui()
        
#         print("✅ Interfaz ejecutada correctamente con módulos actualizados")
        
#     except Exception as e:
#         print(f"❌ Error: {e}")
#         import traceback
#         traceback.print_exc()

# def close_existing_ui():
#     """Cierra cualquier instancia previa de la UI de manera más agresiva"""
#     try:
#         # Buscar en todos los módulos posibles
#         for module_name in list(sys.modules.keys()):
#             if 'ui_builder' in module_name or 'Carros.ui_builder' in module_name:
#                 try:
#                     module = sys.modules[module_name]
#                     if hasattr(module, 'chasis_window') and module.chasis_window:
#                         try:
#                             if hasattr(module.chasis_window, 'close'):
#                                 module.chasis_window.close()
#                             if hasattr(module.chasis_window, 'deleteLater'):
#                                 module.chasis_window.deleteLater()
#                             print("🗑️ Ventana anterior cerrada")
#                         except Exception as e:
#                             print(f"⚠️  Error cerrando ventana: {e}")
#                     # Limpiar la referencia
#                     module.chasis_window = None
#                 except Exception as e:
#                     print(f"⚠️  Error accediendo a módulo {module_name}: {e}")
        
#         # Limpiar garbage collection
#         gc.collect()
                    
#     except Exception as e:
#         print(f"⚠️  Error cerrando UI anterior: {e}")

# def quick_reload():
#     """Función rápida para recargar durante desarrollo"""
#     print("⚡ RECARGA RÁPIDA EJECUTADA")
#     open_chasis_ui()

# # Ejecutar directamente
# if __name__ == "__main__":
#     open_chasis_ui()
#     print("=" * 60)


# import sys
# import importlib
# import os
# import gc

# PROJECT_PATH = r"C:\Users\danie\vscode-environment-for-maya\rig_carros"
# MODULE_NAME = "rig_carros"

# def reload_carro_rig_modules():
#     """Recarga todos los módulos de rig_carros de manera robusta"""
#     print("=" * 60)
#     print("🔄 DEBUG - RECARGANDO MÓDULOS RIG_CARROS")
#     print("=" * 60)
    
#     # Verificar y agregar path
#     print(f"📁 PROJECT_PATH: {PROJECT_PATH}")
#     if PROJECT_PATH not in sys.path:
#         sys.path.insert(0, PROJECT_PATH)
#         print("✅ Ruta agregada a sys.path")
    
#     # Encontrar todos los módulos de rig_carros
#     rig_carros_modules = []
#     for module_name in list(sys.modules.keys()):
#         if module_name and ("rig_carros" in module_name or module_name.startswith("rig_carros")):
#             rig_carros_modules.append(module_name)
    
#     print(f"📦 Módulos rig_carros encontrados: {len(rig_carros_modules)}")
#     for module_name in rig_carros_modules:
#         print(f"   - {module_name}")
    
#     # Recargar módulos en orden inverso (dependencias primero)
#     rig_carros_modules.sort(reverse=True)
    
#     reloaded_modules = []
#     failed_modules = []
    
#     # Primera pasada: intentar recargar
#     for module_name in rig_carros_modules:
#         try:
#             if module_name in sys.modules:
#                 module = sys.modules[module_name]
#                 importlib.reload(module)
#                 reloaded_modules.append(module_name)
#                 print(f"✅ Recargado: {module_name}")
#         except Exception as e:
#             print(f"⚠️  No se pudo recargar {module_name}: {e}")
#             failed_modules.append(module_name)
    
#     # Segunda pasada: para módulos que fallaron, eliminar y reimportar
#     for module_name in failed_modules:
#         try:
#             if module_name in sys.modules:
#                 del sys.modules[module_name]
#                 print(f"🗑️  Eliminado de cache: {module_name}")
                
#                 gc.collect()
                
#                 new_module = importlib.import_module(module_name)
#                 reloaded_modules.append(module_name)
#                 print(f"✅ Reimportado: {module_name}")
#         except Exception as e:
#             print(f"❌ Error crítico con {module_name}: {e}")
    
#     # Importar módulo principal si no estaba cargado
#     try:
#         if MODULE_NAME not in sys.modules:
#             main_module = importlib.import_module(MODULE_NAME)
#             print(f"✅ Importado nuevo: {MODULE_NAME}")
#         else:
#             main_module = importlib.reload(sys.modules[MODULE_NAME])
#             print(f"✅ Recargado principal: {MODULE_NAME}")
            
#         return main_module
#     except Exception as e:
#         print(f"❌ Error cargando módulo principal: {e}")
#         import traceback
#         traceback.print_exc()
#         return None

# def cleanup_module_references():
#     """Limpia referencias específicas problemáticas"""
#     try:
#         # Limpiar referencias específicas que puedan causar conflictos
#         modules_to_clean = ['carro_rig_ui', 'carro_rig_core', 'carro_rig_utils']
        
#         for module_name in modules_to_clean:
#             full_name = f"rig_carros.{module_name}"
#             if full_name in sys.modules:
#                 old_module = sys.modules[full_name]
#                 del sys.modules[full_name]
                
#                 # Limpiar atributos específicos si existen
#                 if hasattr(old_module, 'rig_window'):
#                     try:
#                         old_module.rig_window = None
#                     except:
#                         pass
                
#                 print(f"🧹 Limpiada referencia: {full_name}")
        
#         gc.collect()
        
#     except Exception as e:
#         print(f"⚠️  Error en cleanup: {e}")

# def open_rig_ui():
#     """Abre la interfaz de rig de carro con los módulos recargados"""
#     try:
#         # Limpiar referencias antiguas primero
#         cleanup_module_references()
        
#         # Recargar todos los módulos
#         main_module = reload_carro_rig_modules()
        
#         if main_module is None:
#             print("❌ No se pudo cargar el módulo principal")
#             return
        
#         # Cerrar UI existente si está abierta
#         close_existing_ui()
        
#         # Importar y ejecutar UI después de la recarga
#         from rig_carros import carro_rig_ui
#         print(f"📍 carro_rig_ui cargado desde: {carro_rig_ui.__file__}")
        
#         print("🎯 Ejecutando ventana_rig_carro()...")
#         carro_rig_ui.ventana_rig_carro()
        
#         print("✅ Interfaz ejecutada correctamente con módulos actualizados")
        
#     except Exception as e:
#         print(f"❌ Error: {e}")
#         import traceback
#         traceback.print_exc()

# def close_existing_ui():
#     """Cierra cualquier instancia previa de la UI"""
#     try:
#         import maya.cmds as cmds
#         if cmds.window("winRigCarro", exists=True):
#             cmds.deleteUI("winRigCarro")
#             print("🗑️ Ventana anterior cerrada")
#     except Exception as e:
#         print(f"⚠️  Error cerrando UI anterior: {e}")

# def quick_reload():
#     """Función rápida para recargar durante desarrollo"""
#     print("⚡ RECARGA RÁPIDA EJECUTADA")
#     open_rig_ui()

# # Ejecutar directamente
# if __name__ == "__main__":
#     open_rig_ui()
#     print("=" * 60)
import sys
import importlib
import os
import gc

PROJECT_PATH = r"C:\Users\danie\vscode-environment-for-maya\rig_carros"
MODULE_NAME = "rig_carros"

def reload_carro_rig_modules():
    """Recarga todos los módulos de rig_carros de manera robusta"""
    print("=" * 60)
    print("🔄 DEBUG - RECARGANDO MÓDULOS RIG_CARROS")
    print("=" * 60)
    
    # Verificar y agregar path
    print(f"📁 PROJECT_PATH: {PROJECT_PATH}")
    if PROJECT_PATH not in sys.path:
        sys.path.insert(0, PROJECT_PATH)
        print("✅ Ruta agregada a sys.path")
    
    # Encontrar todos los módulos de rig_carros
    rig_carros_modules = []
    for module_name in list(sys.modules.keys()):
        if module_name and ("rig_carros" in module_name or module_name.startswith("rig_carros")):
            rig_carros_modules.append(module_name)
    
    print(f"📦 Módulos rig_carros encontrados: {len(rig_carros_modules)}")
    for module_name in rig_carros_modules:
        print(f"   - {module_name}")
    
    # Recargar módulos en orden inverso (dependencias primero)
    rig_carros_modules.sort(reverse=True)
    
    reloaded_modules = []
    failed_modules = []
    
    # Primera pasada: intentar recargar
    for module_name in rig_carros_modules:
        try:
            if module_name in sys.modules:
                module = sys.modules[module_name]
                importlib.reload(module)
                reloaded_modules.append(module_name)
                print(f"✅ Recargado: {module_name}")
        except Exception as e:
            print(f"⚠️  No se pudo recargar {module_name}: {e}")
            failed_modules.append(module_name)
    
    # Segunda pasada: para módulos que fallaron, eliminar y reimportar
    for module_name in failed_modules:
        try:
            if module_name in sys.modules:
                del sys.modules[module_name]
                print(f"🗑️  Eliminado de cache: {module_name}")
                
                gc.collect()
                
                new_module = importlib.import_module(module_name)
                reloaded_modules.append(module_name)
                print(f"✅ Reimportado: {module_name}")
        except Exception as e:
            print(f"❌ Error crítico con {module_name}: {e}")
    
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

def cleanup_module_references():
    """Limpia referencias específicas problemáticas"""
    try:
        # Limpiar referencias específicas que puedan causar conflictos
        modules_to_clean = ['carro_rig_ui', 'carro_rig_core', 'carro_rig_utils']
        
        for module_name in modules_to_clean:
            full_name = f"rig_carros.{module_name}"
            if full_name in sys.modules:
                old_module = sys.modules[full_name]
                del sys.modules[full_name]
                
                # Limpiar atributos específicos si existen
                if hasattr(old_module, 'rig_window'):
                    try:
                        old_module.rig_window = None
                    except:
                        pass
                
                print(f"🧹 Limpiada referencia: {full_name}")
        
        gc.collect()
        
    except Exception as e:
        print(f"⚠️  Error en cleanup: {e}")

def open_rig_ui():
    """Abre la interfaz de rig de carro con los módulos recargados"""
    try:
        # Limpiar referencias antiguas primero
        cleanup_module_references()
        
        # Recargar todos los módulos
        main_module = reload_carro_rig_modules()
        
        if main_module is None:
            print("❌ No se pudo cargar el módulo principal")
            return
        
        # Cerrar UI existente si está abierta
        close_existing_ui()
        
        # Importar y ejecutar UI después de la recarga
        from rig_carros import carro_rig_ui
        print(f"📍 carro_rig_ui cargado desde: {carro_rig_ui.__file__}")
        
        print("🎯 Ejecutando ventana_rig_carro()...")
        carro_rig_ui.ventana_rig_carro()
        
        print("✅ Interfaz ejecutada correctamente con módulos actualizados")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def close_existing_ui():
    """Cierra cualquier instancia previa de la UI"""
    try:
        import maya.cmds as cmds
        if cmds.window("winRigCarro", exists=True):
            cmds.deleteUI("winRigCarro")
            print("🗑️ Ventana anterior cerrada")
    except Exception as e:
        print(f"⚠️  Error cerrando UI anterior: {e}")

def verificar_rig_actual():
    """Verifica el estado actual del rig en escena"""
    try:
        import maya.cmds as cmds
        from rig_carros.carro_rig_utils import buscar_objetos_escena
        
        chasis, ruedas = buscar_objetos_escena()
        rig_existe = cmds.objExists("RIG_CARRO_GRP")
        
        print("🔍 ESTADO ACTUAL DEL RIG:")
        print(f"   - Rig en escena: {'✅' if rig_existe else '❌'}")
        print(f"   - Chasis encontrado: {'✅ ' + chasis if chasis else '❌'}")
        print(f"   - Ruedas encontradas: {len(ruedas)}")
        
        if rig_existe:
            print("   - Estado: LISTO para ajustar o limpiar")
        else:
            print("   - Estado: LISTO para generar nuevo rig")
            
    except Exception as e:
        print(f"⚠️  Error en verificación: {e}")

def quick_reload():
    """Función rápida para recargar durante desarrollo"""
    print("⚡ RECARGA RÁPIDA EJECUTADA")
    open_rig_ui()

def crear_rig_directo():
    """Crea el rig directamente sin abrir la UI"""
    try:
        from rig_carros.carro_rig_core import crear_rig_carro
        print("🚗 CREANDO RIG DIRECTAMENTE...")
        crear_rig_carro()
    except Exception as e:
        print(f"❌ Error creando rig: {e}")

def ajustar_rig_directo():
    """Ajusta el rig existente directamente"""
    try:
        from rig_carros.carro_rig_core import ajustar_rig_existente
        print("🎯 AJUSTANDO RIG EXISTENTE...")
        ajustar_rig_existente()
    except Exception as e:
        print(f"❌ Error ajustando rig: {e}")

def limpiar_rig_directo():
    """Limpia el rig existente directamente"""
    try:
        from rig_carros.carro_rig_core import limpiar_rig_existente
        print("🧹 LIMPIANDO RIG EXISTENTE...")
        elementos = limpiar_rig_existente()
        print(f"✅ Elementos eliminados: {elementos}")
    except Exception as e:
        print(f"❌ Error limpiando rig: {e}")

# Comandos rápidos para desarrollo
COMANDOS_RAPIDOS = {
    'ui': open_rig_ui,
    'reload': quick_reload,
    'crear': crear_rig_directo,
    'ajustar': ajustar_rig_directo,
    'limpiar': limpiar_rig_directo,
    'verificar': verificar_rig_actual
}

def ejecutar_comando_rapido(comando):
    """Ejecuta un comando rápido desde la línea de comandos"""
    if comando in COMANDOS_RAPIDOS:
        print(f"⚡ Ejecutando comando: {comando}")
        COMANDOS_RAPIDOS[comando]()
    else:
        print(f"❌ Comando no reconocido: {comando}")
        print("Comandos disponibles: " + ", ".join(COMANDOS_RAPIDOS.keys()))

# Ejecutar directamente
if __name__ == "__main__":
    # Si se pasa un argumento, ejecutar comando rápido
    if len(sys.argv) > 1:
        ejecutar_comando_rapido(sys.argv[1])
    else:
        open_rig_ui()
        print("=" * 60)
        print("💡 Usa: main.py [comando]")
        print("   Comandos: ui, reload, crear, ajustar, limpiar, verificar")
        print("=" * 60)