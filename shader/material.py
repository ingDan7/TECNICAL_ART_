import maya.cmds as cmds
import random

def _aplicar_material_futurista(self, objeto):
        """Aplica material con estilo futurista"""
        colores_futuristas = [
            (0.1, 0.5, 0.8),   # Azul eléctrico
            (0.8, 0.2, 0.6),   # Rosa neón
            (0.2, 0.8, 0.4),   # Verde cibernético
            (0.9, 0.7, 0.1),   # Amarillo energía
            (0.6, 0.3, 0.8),   # Púrpura digital
        ]
        
        color = random.choice(colores_futuristas)
        material = cmds.shadingNode('blinn', asShader=True, name=f"mat_futurista_{random.randint(1000,9999)}")
        
        cmds.setAttr(material + ".color", color[0], color[1], color[2], type="double3")
        cmds.setAttr(material + ".specularColor", 0.8, 0.8, 0.8, type="double3")
        cmds.setAttr(material + ".eccentricity", 0.1)
        cmds.setAttr(material + ".reflectivity", 0.3)
        
        cmds.select(objeto)
        cmds.hyperShade(assign=material)