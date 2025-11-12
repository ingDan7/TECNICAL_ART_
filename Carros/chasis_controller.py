import maya.cmds as cmds
import random

class ChasisController:
    def __init__(self):
        self.cubo_actual = None
        self.nombre_base = "axioma_carro"
        self.ultimo_tipo = None
        
        # RANGOS AMPLIADOS PARA CAMBIOS NOTORIOS
        self.rangos_dimensiones = {
            'ancho': {'min': 1.2, 'max': 3.5},
            'alto': {'min': 0.5, 'max': 2.0},
            'largo': {'min': 2.0, 'max': 8.0}
        }
    
    def generar_dimensiones_aleatorias(self):
        """Generar dimensiones aleatorias con variación extrema"""
        def valor_con_variacion(min_val, max_val):
            if random.random() < 0.5:
                return round(random.choice([
                    random.uniform(min_val, min_val + (max_val - min_val) * 0.3),
                    random.uniform(max_val - (max_val - min_val) * 0.3, max_val)
                ]), 2)
            else:
                return round(random.uniform(min_val, max_val), 2)
        
        dimensiones = {
            'ancho': valor_con_variacion(self.rangos_dimensiones['ancho']['min'], 
                                       self.rangos_dimensiones['ancho']['max']),
            'alto': valor_con_variacion(self.rangos_dimensiones['alto']['min'], 
                                      self.rangos_dimensiones['alto']['max']),
            'largo': valor_con_variacion(self.rangos_dimensiones['largo']['min'], 
                                       self.rangos_dimensiones['largo']['max'])
        }
        
        print(f"🎲 DIMENSIONES GENERADAS - Ancho:{dimensiones['ancho']}, Alto:{dimensiones['alto']}, Largo:{dimensiones['largo']}")
        return dimensiones
    
    def crear_cubo_base(self, nombre, ancho, alto, largo):
        """Crear el cubo base del chasis"""
        try:
            cmds.select(clear=True)
            
            cubo = cmds.polyCube(
                width=ancho,
                height=alto,
                depth=largo,
                subdivisionsX=1,
                subdivisionsY=1,
                subdivisionsZ=1,
                axis=(0, 1, 0),
                createUVs=4,
                constructionHistory=1,
                name=nombre
            )
            
            self.cubo_actual = cubo[0]
            cmds.select(self.cubo_actual)
            
            print(f"✅ CHASIS BASE CREADO - Ancho:{ancho}, Alto:{alto}, Largo:{largo}")
            return self.cubo_actual
            
        except Exception as e:
            cmds.warning(f"❌ Error al crear cubo base: {str(e)}")
            return None
    

    def transformar_chasis_existente(self, nuevo_ancho, nuevo_alto, nuevo_largo):
        """SOLUCIÓN DEFINITIVA: Modificar el chasis sin eliminar las extrusiones"""
        if not self.cubo_actual or not cmds.objExists(self.cubo_actual):
            cmds.warning("❌ No hay chasis existente para transformar")
            return False
        
        try:
            print(f"🔄 TRANSFORMANDO CHASIS SIN ELIMINAR: {nuevo_ancho}x{nuevo_alto}x{nuevo_largo}")
            
            # BUSCAR EL NODO polyCube EN EL HISTORIAL PARA MODIFICARLO DIRECTAMENTE
            historial = cmds.listHistory(self.cubo_actual)
            nodo_polyCube = None
            
            for nodo in historial:
                if cmds.nodeType(nodo) == 'polyCube':
                    nodo_polyCube = nodo
                    break
            
            if nodo_polyCube:
                print(f"🔧 ENCONTRADO NODO polyCube: {nodo_polyCube}")
                
                # MODIFICAR LAS DIMENSIONES DIRECTAMENTE EN EL NODO polyCube
                cmds.setAttr(f"{nodo_polyCube}.width", nuevo_ancho)
                cmds.setAttr(f"{nodo_polyCube}.height", nuevo_alto) 
                cmds.setAttr(f"{nodo_polyCube}.depth", nuevo_largo)
                
                # FORZAR ACTUALIZACIÓN
                cmds.refresh()
                
                print(f"✅ CHASIS TRANSFORMADO MANTENIENDO EXTRUSIONES")
                return True
            else:
                print("❌ No se encontró nodo polyCube, usando método alternativo")
                # Método de respaldo: escalar el objeto
                escala_x = nuevo_ancho / self.obtener_dimensiones()['ancho']
                escala_y = nuevo_alto / self.obtener_dimensiones()['alto']
                escala_z = nuevo_largo / self.obtener_dimensiones()['largo']
                
                cmds.scale(escala_x, escala_y, escala_z, self.cubo_actual, relative=False)
                print(f"📏 CHASIS ESCALADO: {escala_x:.2f}, {escala_y:.2f}, {escala_z:.2f}")
                return True
                
        except Exception as e:
            cmds.warning(f"❌ Error en transformación no destructiva: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def obtener_dimensiones(self):
        """Obtener dimensiones actuales del chasis"""
        if not self.cubo_actual:
            return None
            
        try:
            bbox = cmds.xform(self.cubo_actual, query=True, boundingBox=True)
            return {
                'ancho': bbox[3] - bbox[0],
                'alto': bbox[4] - bbox[1], 
                'largo': bbox[5] - bbox[2],
                'posicion': cmds.xform(self.cubo_actual, query=True, translation=True)
            }
        except:
            return None
    
    def limpiar_chasis(self):
        """Eliminar chasis actual"""
        if self.cubo_actual and cmds.objExists(self.cubo_actual):
            cmds.delete(self.cubo_actual)
        self.cubo_actual = None
        self.ultimo_tipo = None



