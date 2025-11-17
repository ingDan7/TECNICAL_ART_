#!/usr/bin/env python
"""
🏙️ CIUDAD EMERGENTE - Punto de entrada principal
"""

import maya.cmds as cmds
from carros_ambiente.ui import ciudad_ui

def main():
    """Función principal que inicia la aplicación."""
    print("🚀 Iniciando Ciudad Emergente...")
    ciudad_ui()

if __name__ == "__main__":
    main()