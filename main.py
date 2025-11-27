
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
# import maya.cmds as cmds

# # Configuración - Usar variables de entorno
# PROJECT_PATH = os.getenv('RIG_CARROS_PATH', r"C:\Users\danie\vscode-environment-for-maya\rig_carros")


# def reload_rig_carros():
#     """Recarga completa y efectiva de todo el sistema rig_carros"""
#     print("🔄 Recargando sistema rig_carros...")
    
#     # Agregar path si no existe
#     if PROJECT_PATH not in sys.path:
#         sys.path.insert(0, PROJECT_PATH)
#         print(f"📁 Path agregado: {PROJECT_PATH}")
    
#     # Cerrar todas las UIs existentes del sistema
#     ui_windows = ["carro_rig_ui", "carro_rig_coordinator", "winRigCarro"]
#     for window in ui_windows:
#         if cmds.window(window, exists=True):
#             cmds.deleteUI(window)
#             print(f"✅ Ventana {window} cerrada")
    
#     # Eliminar módulos existentes de forma segura
#     modules_to_remove = []
#     for module_name in list(sys.modules.keys()):
#         if module_name and ('rig_carros' in module_name or 'carro_rig' in module_name):
#             modules_to_remove.append(module_name)
    
#     # Eliminar en orden inverso para evitar dependencias
#     modules_to_remove.sort(reverse=True)
#     for module_name in modules_to_remove:
#         try:
#             del sys.modules[module_name]
#             print(f"🗑️ Eliminado: {module_name}")
#         except Exception as e:
#             print(f"⚠️ No se pudo eliminar {module_name}: {e}")
    
#     try:
#         print("📦 Importando módulos frescos...")
        
#         # Importar módulos en orden correcto
#         import rig_carros.carro_rig_utils as utils
#         importlib.reload(utils)
#         print("✅ carro_rig_utils recargado")
        
#         import rig_carros.carro_rig_core as core
#         importlib.reload(core)
#         print("✅ carro_rig_core recargado")
        
#         import rig_carros.carro_rig_ui as ui
#         importlib.reload(ui)
#         print("✅ carro_rig_ui recargado")
        
#         # Crear instancias y CONECTAR CALLBACKS MANUALMENTE
#         core_system = core.CarroRigCore()
#         ui_system = ui.CarroRigUI()
        
#         # CONECTAR CALLBACKS DIRECTAMENTE
#         ui_system.on_crear_rig = lambda: crear_rig_callback(core_system, utils)
#         ui_system.on_ajustar_rig = lambda: ajustar_rig_callback(core_system)
#         ui_system.on_limpiar_rig = lambda: limpiar_rig_callback(core_system)
#         ui_system.on_verificar_escena = lambda: verificar_escena_callback(utils)
        
#         print("🎯 CALLBACKS CONECTADOS MANUALMENTE")
        
#         # Mostrar UI
#         ui_system.mostrar_interfaz_principal()
        
#         print("🎉 Sistema rig_carros recargado exitosamente!")
#         print("✅ Todos los callbacks conectados correctamente")
        
#     except Exception as e:
#         print(f"❌ Error en recarga principal: {e}")
#         # Usar el fallback robusto
#         setup_ui_fallback()

# # CALLBACKS MANUALES - DEFINIDOS GLOBALMENTE
# def crear_rig_callback(core_system, utils):
#     """Callback manual para crear rig"""
#     try:
#         print("🎯 Ejecutando crear rig desde callback...")
#         chasis, ruedas, ejes = utils.buscar_objetos_escena_filtrado()
        
#         if not chasis:
#             cmds.confirmDialog(title="Error", message="❌ No se encontró chasis en la escena", button=["OK"])
#             return False
        
#         resultado = core_system.crear_rig_completo(chasis, ruedas, ejes)
        
#         if resultado:
#             cmds.confirmDialog(title="Éxito", message="✅ Rig creado correctamente", button=["OK"])
#         else:
#             cmds.confirmDialog(title="Error", message="❌ Error creando rig", button=["OK"])
            
#         return resultado
#     except Exception as e:
#         cmds.confirmDialog(title="Error", message=f"❌ Error: {str(e)}", button=["OK"])
#         return False

# def ajustar_rig_callback(core_system):
#     """Callback manual para ajustar rig"""
#     try:
#         print("⚙️ Ejecutando ajustar rig desde callback...")
#         resultado = core_system.ajustar_rig_existente()
#         if resultado:
#             cmds.confirmDialog(title="Éxito", message="✅ Rig ajustado correctamente", button=["OK"])
#         else:
#             cmds.confirmDialog(title="Error", message="❌ No se pudo ajustar el rig", button=["OK"])
#         return resultado
#     except Exception as e:
#         cmds.confirmDialog(title="Error", message=f"❌ Error: {str(e)}", button=["OK"])
#         return False

# def limpiar_rig_callback(core_system):
#     """Callback manual para limpiar rig"""
#     try:
#         print("🗑️ Ejecutando limpiar rig desde callback...")
#         elementos_eliminados = core_system.limpiar_rig_existente()
#         cmds.confirmDialog(
#             title="Limpieza Completa", 
#             message=f"✅ {elementos_eliminados} elementos eliminados", 
#             button=["OK"]
#         )
#         return elementos_eliminados
#     except Exception as e:
#         cmds.confirmDialog(title="Error", message=f"❌ Error: {str(e)}", button=["OK"])
#         return 0

# def verificar_escena_callback(utils):
#     """Callback manual para verificar escena"""
#     try:
#         print("🔍 Ejecutando verificar escena desde callback...")
#         chasis, ruedas, ejes = utils.buscar_objetos_escena_filtrado()
        
#         mensaje = "🔍 DIAGNÓSTICO DE ESCENA:\n\n"
        
#         if chasis:
#             mensaje += f"✅ CHASIS: {chasis}\n"
#         else:
#             mensaje += "❌ CHASIS: No encontrado\n"
        
#         mensaje += f"✅ RUEDAS: {len(ruedas)} encontradas\n"
#         for rueda in ruedas:
#             mensaje += f"   - {rueda}\n"
        
#         mensaje += f"✅ EJES: {len(ejes)} encontrados\n"
#         for eje in ejes:
#             mensaje += f"   - {eje}\n"
        
#         if cmds.objExists("RIG_CARRO_GRP"):
#             mensaje += "\n✅ RIG: Presente en escena\n"
#         else:
#             mensaje += "\n❌ RIG: No existe en escena\n"
        
#         if len(ruedas) < 4:
#             mensaje += f"\n⚠️ Se recomiendan 4 ruedas (encontradas: {len(ruedas)})"
        
#         cmds.confirmDialog(title="Diagnóstico de Escena", message=mensaje, button=["OK"])
        
#     except Exception as e:
#         cmds.confirmDialog(title="Error", message=f"❌ Error verificando escena: {str(e)}", button=["OK"])

# def setup_ui_fallback():
#     """Configuración de emergencia robusta"""
#     print("🆘 Configurando UI de emergencia...")
    
#     try:
#         # Cerrar UI existente
#         if cmds.window("carro_rig_ui", exists=True):
#             cmds.deleteUI("carro_rig_ui")
        
#         # Importar módulos frescos
#         from rig_carros.carro_rig_ui import CarroRigUI
#         from rig_carros.carro_rig_core import CarroRigCore
#         from rig_carros.carro_rig_utils import buscar_objetos_escena_filtrado
        
#         # Crear instancias
#         core_system = CarroRigCore()
#         ui_system = CarroRigUI()
        
#         # Conectar callbacks manualmente usando las funciones globales
#         ui_system.on_crear_rig = lambda: crear_rig_callback(core_system, buscar_objetos_escena_filtrado)
#         ui_system.on_ajustar_rig = lambda: ajustar_rig_callback(core_system)
#         ui_system.on_limpiar_rig = lambda: limpiar_rig_callback(core_system)
#         ui_system.on_verificar_escena = lambda: verificar_escena_callback(buscar_objetos_escena_filtrado)
        
#         ui_system.mostrar_interfaz_principal()
#         print("✅ UI de emergencia con callbacks manuales lista")
        
#     except Exception as e:
#         print(f"❌ Error en UI de emergencia: {e}")
#         # Último recurso: UI básica sin callbacks
#         try:
#             from rig_carros.carro_rig_ui import mostrar_ui_standalone
#             mostrar_ui_standalone()
#             print("✅ UI standalone cargada (sin callbacks)")
#         except:
#             print("❌ Todas las opciones fallaron")

# def quick_reload():
#     """Recarga rápida - alias para hotkeys"""
#     reload_rig_carros()

# def debug_system():
#     """Debug del sistema completo"""
#     print("\n🔍 DEBUG DEL SISTEMA:")
#     print(f"📁 PROJECT_PATH: {PROJECT_PATH}")
#     print(f"📁 En sys.path: {PROJECT_PATH in sys.path}")
    
#     # Verificar módulos
#     modules_to_check = [
#         'carro_rig_utils',
#         'carro_rig_core', 
#         'carro_rig_ui'
#     ]
    
#     for module_name in modules_to_check:
#         full_name = f"rig_carros.{module_name}"
#         if full_name in sys.modules:
#             print(f"✅ {module_name}: CARGADO")
#         else:
#             print(f"❌ {module_name}: NO CARGADO")

# # Comandos rápidos
# def open_ui_simple():
#     """Abre la UI simple sin recargar todo"""
#     try:
#         from rig_carros.carro_rig_ui import mostrar_ui_standalone
#         mostrar_ui_standalone()
#     except Exception as e:
#         print(f"❌ Error abriendo UI simple: {e}")

# # Función directa para crear rig (para testing)
# def crear_rig_directo():
#     """Crea el rig directamente sin UI"""
#     try:
#         from rig_carros.carro_rig_core import CarroRigCore
#         from rig_carros.carro_rig_utils import buscar_objetos_escena_filtrado
        
#         core = CarroRigCore()
#         chasis, ruedas, ejes = buscar_objetos_escena_filtrado()
        
#         if chasis:
#             resultado = core.crear_rig_completo(chasis, ruedas, ejes)
#             if resultado:
#                 cmds.confirmDialog(title="Éxito", message="✅ Rig creado directamente", button=["OK"])
#             else:
#                 cmds.confirmDialog(title="Error", message="❌ Error creando rig", button=["OK"])
#         else:
#             cmds.confirmDialog(title="Error", message="❌ No hay chasis en escena", button=["OK"])
            
#     except Exception as e:
#         cmds.confirmDialog(title="Error", message=f"❌ Error: {str(e)}", button=["OK"])

# # Ejecutar
# if __name__ == "__main__":
#     reload_rig_carros()



import sys
import importlib
import os
import gc

# Usar variable de entorno para Carros
PROJECT_PATH = os.getenv('CARROS_PROJECT_PATH', r"C:\Users\pc\Documents\Repositorios\TECNICAL_ART_\Carros")
MODULE_NAME = "Carros"

def reload_carros_modules():
    """Recarga todos los módulos de Carros de manera más robusta"""
    print("=" * 60)
    print("🔄 DEBUG - RECARGANDO MÓDULOS CARROS")
    print("=" * 60)
    
    # Verificar y agregar path
    print(f"📁 PROJECT_PATH: {PROJECT_PATH}")
    if PROJECT_PATH not in sys.path:
        sys.path.insert(0, PROJECT_PATH)  # Insertar al inicio para prioridad
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
    failed_modules = []
    
    # Primera pasada: intentar recargar
    for module_name in carros_modules:
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
                # Eliminar del sys.modules
                del sys.modules[module_name]
                print(f"🗑️  Eliminado de cache: {module_name}")
                
                # Forzar garbage collection
                gc.collect()
                
                # Reimportar
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
        modules_to_clean = ['ui_builder', 'chasis_controller', 'car_utils']
        
        for module_name in modules_to_clean:
            full_name = f"Carros.{module_name}"
            if full_name in sys.modules:
                # Guardar referencia antes de eliminar
                old_module = sys.modules[full_name]
                
                # Eliminar del sys.modules
                del sys.modules[full_name]
                
                # Limpiar atributos específicos si existen
                if hasattr(old_module, 'chasis_window'):
                    try:
                        old_module.chasis_window = None
                    except:
                        pass
                
                print(f"🧹 Limpiada referencia: {full_name}")
        
        # Forzar garbage collection
        gc.collect()
        
    except Exception as e:
        print(f"⚠️  Error en cleanup: {e}")

def open_chasis_ui():
    """Abre la interfaz de chasis con los módulos recargados"""
    try:
        # Limpiar referencias antiguas primero
        cleanup_module_references()
        
        # Recargar todos los módulos
        main_module = reload_carros_modules()
        
        if main_module is None:
            print("❌ No se pudo cargar el módulo principal")
            return
        
        # Cerrar UI existente si está abierta
        close_existing_ui()
        
        # Importar y ejecutar UI después de la recarga
        from Carros import ui_builder
        print(f"📍 ui_builder cargado desde: {ui_builder.__file__}")
        
        print("🎯 Ejecutando open_chasis_ui()...")
        ui_builder.open_chasis_ui()
        
        print("✅ Interfaz ejecutada correctamente con módulos actualizados")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def close_existing_ui():
    """Cierra cualquier instancia previa de la UI de manera más agresiva"""
    try:
        # Buscar en todos los módulos posibles
        for module_name in list(sys.modules.keys()):
            if 'ui_builder' in module_name or 'Carros.ui_builder' in module_name:
                try:
                    module = sys.modules[module_name]
                    if hasattr(module, 'chasis_window') and module.chasis_window:
                        try:
                            if hasattr(module.chasis_window, 'close'):
                                module.chasis_window.close()
                            if hasattr(module.chasis_window, 'deleteLater'):
                                module.chasis_window.deleteLater()
                            print("🗑️ Ventana anterior cerrada")
                        except Exception as e:
                            print(f"⚠️  Error cerrando ventana: {e}")
                    # Limpiar la referencia
                    module.chasis_window = None
                except Exception as e:
                    print(f"⚠️  Error accediendo a módulo {module_name}: {e}")
        
        # Limpiar garbage collection
        gc.collect()
                    
    except Exception as e:
        print(f"⚠️  Error cerrando UI anterior: {e}")

def quick_reload():
    """Función rápida para recargar durante desarrollo"""
    print("⚡ RECARGA RÁPIDA EJECUTADA")
    open_chasis_ui()

# Ejecutar directamente
if __name__ == "__main__":
    open_chasis_ui()
    print("=" * 60)

