import maya.cmds as cmds
import random

class ExtrusionManager:
    def __init__(self):
        self.extrusion_nodes = {}
        self.configuracion = {
            'capo': {
                'cara_index': 0, 
                'thickness_default': 1.5, 
                'min_thickness': 0.7,
                'max_thickness': 2.5,
                'incremento': 0.1
            },
            'techo': {
                'cara_index': 1, 
                'thickness_default': 0.6, 
                'min_thickness': 0.5,
                'max_thickness': 1.2,
                'incremento': 0.05
            },
            'maletero': {
                'cara_index': 2, 
                'thickness_default': 1.2, 
                'min_thickness': 0.1,
                'max_thickness': 2.0,
                'incremento': 0.1
            }
        }
        
        # Callbacks
        self.on_extrusion_creada = None
    
    def generar_thickness_aleatorio(self, tipo):
        """Generar thickness aleatorio dentro de rangos controlados"""
        config = self.configuracion[tipo]
        return round(random.uniform(config['min_thickness'], config['max_thickness']), 2)

    def crear_extrusion(self, chasis_nombre, tipo, thickness=None):
        """Crear una extrusión para el chasis - MEJORADO"""
        if not chasis_nombre or not cmds.objExists(chasis_nombre):
            cmds.warning(f"❌ No hay chasis válido para crear {tipo}")
            return False
        
        config = self.configuracion[tipo]
        
        # Usar thickness proporcionado o generar uno aleatorio
        if thickness is None:
            thickness = self.generar_thickness_aleatorio(tipo)
        
        cara = f"{chasis_nombre}.f[{config['cara_index']}]"
        
        try:
            # VERIFICAR QUE EL CHASIS Y LA CARA EXISTEN
            if not cmds.objExists(chasis_nombre):
                print(f"❌ El chasis {chasis_nombre} no existe")
                return False
                
            if not cmds.objExists(cara):
                print(f"⚠️ La cara {cara} no existe, intentando recrear geometría...")
                # Forzar la actualización de la geometría
                cmds.select(chasis_nombre)
                cmds.polyNormal(chasis_nombre, normalMode=0, userNormalMode=0, ch=0)
                cmds.select(clear=True)
                
                # Verificar nuevamente
                if not cmds.objExists(cara):
                    print(f"❌ No se pudo acceder a la cara {cara}")
                    return False
            
            # LIMPIAR SELECCIÓN PREVIA
            cmds.select(clear=True)
            cmds.select(cara)
            
            # CREAR EXTRUSIÓN
            extrusion = cmds.polyExtrudeFacet(
                cara,
                constructionHistory=True,
                keepFacesTogether=True,
                thickness=0.1  # Valor mínimo inicial para evitar errores
            )
            
            if extrusion:
                extrude_node = extrusion[0]
                self.extrusion_nodes[tipo] = extrude_node
                
                # AJUSTAR THICKNESS FINAL
                cmds.setAttr(f"{extrude_node}.thickness", thickness)
                
                # LIMPIAR SELECCIÓN
                cmds.select(clear=True)
                
                # Notificar callback
                if self.on_extrusion_creada:
                    self.on_extrusion_creada(tipo, thickness)
                
                print(f"✅ {tipo.upper()} creado con thickness: {thickness}")
                return True
            else:
                print(f"❌ No se pudo crear la extrusión para {tipo}")
                return False
                
        except Exception as e:
            cmds.warning(f"❌ Error al crear {tipo}: {str(e)}")
            cmds.select(clear=True)
            return False
    
    def recrear_extrusiones(self, chasis_nombre):
        """Recrear todas las extrusiones después de transformar el chasis"""
        print("🔄 RECREANDO EXTRUSIONES PARA NUEVO CHASIS...")
        
        # Limpiar extrusiones anteriores
        self.limpiar_extrusiones()
        
        # Crear nuevas extrusiones con valores aleatorios
        for tipo in self.configuracion.keys():
            thickness_aleatorio = self.generar_thickness_aleatorio(tipo)
            print(f"🔄 Recreando {tipo} con thickness: {thickness_aleatorio}")
            resultado = self.crear_extrusion(chasis_nombre, tipo, thickness_aleatorio)
            if resultado and self.on_extrusion_creada:
                self.on_extrusion_creada(tipo, thickness_aleatorio)
        
        print("✅ EXTRUSIONES RECREADAS EXITOSAMENTE")
    
    def ajustar_thickness(self, tipo, thickness):
        """Ajustar thickness de una extrusión"""
        if tipo in self.extrusion_nodes and cmds.objExists(self.extrusion_nodes[tipo]):
            cmds.setAttr(f"{self.extrusion_nodes[tipo]}.thickness", thickness)
            return True
        return False

    def aumentar_thickness(self, tipo):
        """Aumentar thickness de una extrusión existente"""
        if tipo not in self.extrusion_nodes or not cmds.objExists(self.extrusion_nodes[tipo]):
            return None
            
        config = self.configuracion[tipo]
        thickness_actual = self.obtener_thickness_actual(tipo)
        nuevo_thickness = thickness_actual + config['incremento']
        
        # Verificar límite máximo
        if nuevo_thickness > config['max_thickness']:
            nuevo_thickness = config['max_thickness']
            
        self.ajustar_thickness(tipo, nuevo_thickness)
        return nuevo_thickness

    def disminuir_thickness(self, tipo):
        """Disminuir thickness de una extrusión existente"""
        if tipo not in self.extrusion_nodes or not cmds.objExists(self.extrusion_nodes[tipo]):
            return None
            
        config = self.configuracion[tipo]
        thickness_actual = self.obtener_thickness_actual(tipo)
        nuevo_thickness = thickness_actual - config['incremento']
        
        # Verificar límite mínimo
        if nuevo_thickness < config['min_thickness']:
            nuevo_thickness = config['min_thickness']
            
        self.ajustar_thickness(tipo, nuevo_thickness)
        return nuevo_thickness

    def obtener_thickness_actual(self, tipo):
        """Obtener thickness actual con verificación robusta"""
        if tipo in self.extrusion_nodes and cmds.objExists(self.extrusion_nodes[tipo]):
            try:
                return cmds.getAttr(f"{self.extrusion_nodes[tipo]}.thickness")
            except:
                return 0
        return 0
    
    def limpiar_extrusiones(self):
        """Limpiar todas las extrusiones"""
        # No eliminamos los nodos porque se eliminan con el chasis
        self.extrusion_nodes = {}

    def extrusion_existe(self, tipo):
        """Verificar si una extrusión existe"""
        return tipo in self.extrusion_nodes and cmds.objExists(self.extrusion_nodes[tipo])