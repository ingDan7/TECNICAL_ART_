import maya.cmds as cmds

def crear_curva_basica():
    """Crea una curva básica usando Curve Tool estándar"""
    
    # Puntos para una curva simple en forma de S
    puntos = [
        (-10, 0, 0),
        (-5, 3, 0),
        (0, 0, 0),
        (5, -3, 0),
        (10, 0, 0)
    ]
    
    # Crear curva
    curva = cmds.curve(p=puntos, d=3, name="curvaBasica")
    
    print(f"✅ Curva básica creada: {curva}")
    return curva

# Ejecutar
crear_curva_basica()