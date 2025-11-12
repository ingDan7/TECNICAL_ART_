import sys
import os
import maya.cmds as cmds

def safe_main():
    try:
        print("🚀 INICIANDO SISTEMA DE RIGS...")
        
        rig_path = r"C:\Users\danie\vscode-environment-for-maya\rig_integrado"
        if rig_path not in sys.path:
            sys.path.insert(0, rig_path)
        
        if cmds.about(batch=True):
            print("❌ No se puede abrir UI en modo batch")
            return
        
        # ✅ IMPORT CORRECTO
        import ui
        ui.open_spine_ui()
        
        print("✅ Sistema iniciado correctamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        try:
            cmds.confirmDialog(title="Error", message=str(e), button=["OK"])
        except:
            pass

if __name__ == "__main__":
    safe_main()