"""
🏙️ Módulo Core - Lógica de generación de ciudad futurista
"""

import maya.cmds as cmds
import random
import math

class CiudadFuturista:
    """Genera una ciudad futurista con formas orgánicas y surrealistas"""
    
    def __init__(self, config=None):
        self.config = config or {
            'num_edificios': 15,
            'radio_ciudad': 100,
            'altura_min': 30,
            'altura_max': 120,
            'intensidad_curvas': 4.0
        }
        self.grupo_ciudad = None
        
    def generar(self):
        """Genera la ciudad completa"""
        try:
            # Limpiar escena anterior
            self._limpiar_escena()
            
            # Crear grupo principal
            self.grupo_ciudad = cmds.group(empty=True, name="ciudad_futurista")
            
            # Generar elementos
            self._generar_carreteras_espirales()
            self._generar_edificios_organicos()
            self._generar_estructuras_surrealistas()
            self._generar_puentes_curvos()
            
            # Organizar y finalizar
            cmds.select(self.grupo_ciudad)
            cmds.viewFit()
            
            print("✅ Ciudad futurista generada exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error generando ciudad: {e}")
            return False
    
    def _limpiar_escena(self):
        """Limpia ciudad anterior"""
        if cmds.objExists("ciudad_futurista"):
            cmds.delete("ciudad_futurista")
    
    def _generar_carreteras_espirales(self):
        """Genera carreteras en espiral y formas infinitas"""
        print("🛣️ Generando carreteras espirales...")
        
        # Espiral principal
        self._crear_espiral_fibonacci(
            radio=60, 
            vueltas=4, 
            nombre="carretera_espiral_principal"
        )
        
        # Forma infinito (lemniscata)
        self._crear_curva_infinito(
            escala=50,
            nombre="carretera_infinito"
        )
        
        # Espirales secundarias
        for i in range(4):
            angulo = random.uniform(0, math.pi * 2)
            distancia = random.uniform(30, 80)
            x = math.cos(angulo) * distancia
            z = math.sin(angulo) * distancia
            
            # Y aleatorio entre -10 y 10 (puedes ajustar el rango)
            y = random.uniform(5, 20)

            self._crear_espiral_arquimedes(
                centro=(x, y, z),
                radio=random.uniform(15, 30),
                vueltas=random.uniform(2, 3),
                nombre=f"espiral_ambiente_{i}"
            )

               
    def _generar_edificios_organicos(self):
        """Genera edificios con formas orgánicas y curvas"""
        print("🏢 Generando edificios orgánicos...")
        
        for i in range(self.config['num_edificios']):
            # Posición en patrones espirales
            angulo = random.uniform(0, math.pi * 2)
            radio = random.uniform(20, self.config['radio_ciudad'] * 0.9)
            x = math.cos(angulo) * radio
            z = math.sin(angulo) * radio
            
            # Tipo de edificio aleatorioB
            tipo_edificio = random.choice([
                self._crear_edificio_espiral,
                self._crear_edificio_onda,
                self._crear_edificio_torsion,
                self._crear_edificio_fractal
            ])
            
            tipo_edificio(x, z, i)
    
    def _generar_estructuras_surrealistas(self):
        """Genera estructuras surrealistas adicionales"""
        print("🌀 Generando estructuras surrealistas...")
        
        # Esfera de Möbius
        self._crear_cinta_mobius(
            radio=25,
            nombre="estructura_mobius"
        )
        
        # Toroide retorcido
        self._crear_toroide_retorcido(
            radio_principal=40,
            radio_secundario=8,
            nombre="toroide_surreal"
        )
    
    def _generar_puentes_curvos(self):
        """Genera puentes curvos entre edificios"""
        print("🌉 Generando puentes curvos...")
        
        for i in range(4):
            self._crear_puente_curvo(
                punto_a=(random.uniform(-15, 15), 8, random.uniform(-15, 15)),
                punto_b=(random.uniform(-15, 15), 12, random.uniform(-15, 15)),
                nombre=f"puente_curvo_{i}"
            )

    # ===== GENERADORES DE CURVAS MATEMÁTICAS =====
    
    def _crear_espiral_fibonacci(self, radio=15, vueltas=3, nombre="espiral"):
        """Crea una espiral de Fibonacci (proporción áurea)"""
        puntos = []
        phi = (1 + math.sqrt(5)) / 2  # Proporción áurea
        
        for i in range(100):
            angulo = 2 * math.pi * phi * i / 100 * vueltas
            r = radio * math.sqrt(i / 100)
            
            x = r * math.cos(angulo)
            z = r * math.sin(angulo)
            y = i * 0.5
            puntos.append((x, y, z))
        
        curva = cmds.curve(p=puntos, degree=3, name=nombre)
        cmds.parent(curva, self.grupo_ciudad)
        return curva
    
    def _crear_espiral_arquimedes(self, centro=(0, 0, 0), radio=5, vueltas=2, nombre="espiral_arquimedes"):
        """Crea espiral de Arquímedes (radio crece linealmente)"""
        puntos = []
        
        for i in range(50):
            t = i / 50.0
            angulo = 2 * math.pi * vueltas * t
            r = radio * t
            
            x = centro[0] + r * math.cos(angulo)
            z = centro[2] + r * math.sin(angulo)
            puntos.append((x, 0.1, z))
        
        curva = cmds.curve(p=puntos, degree=3, name=nombre)
        cmds.parent(curva, self.grupo_ciudad)
        return curva
    
    def _crear_curva_infinito(self, escala=10, nombre="infinito"):
        """Crea curva en forma de infinito (lemniscata)"""
        puntos = []
        
        for i in range(100):
            t = i / 100.0 * 2 * math.pi
            # Ecuación paramétrica de lemniscata
            x = escala * math.cos(t) / (1 + math.sin(t)**2)
            z = escala * math.sin(t) * math.cos(t) / (1 + math.sin(t)**2)
            y = i*0.2
            puntos.append((x, y, z))
        
        curva = cmds.curve(p=puntos, degree=3, name=nombre)
        cmds.parent(curva, self.grupo_ciudad)
        return curva
    
    def _crear_cinta_mobius(self, radio=5, nombre="mobius"):
        """Crea una cinta de Möbius (superficie de una sola cara)"""
        puntos = []
        
        for i in range(100):
            u = i / 100.0 * 2 * math.pi
            for j in range(10):
                v = j / 10.0 * 2 * math.pi
                
                x = (radio + v * math.cos(u/2)) * math.cos(u)
                y = v * math.sin(u/2)
                z = (radio + v * math.cos(u/2)) * math.sin(u)
                
                puntos.append((x, y, z))
        
        # Crear como superficie NURBS
        try:
            superficie = cmds.surface(p=puntos, degree=3, n=nombre)
            cmds.parent(superficie, self.grupo_ciudad)
            return superficie
        except:
            return None
    
    def _crear_toroide_retorcido(self, radio_principal=10, radio_secundario=2, nombre="toroide"):
        """Crea un toroide retorcido"""
        puntos = []
        
        for i in range(50):
            u = i / 50.0 * 2 * math.pi
            for j in range(20):
                v = j / 20.0 * 2 * math.pi
                
                # Toroide retorcido
                x = (radio_principal + radio_secundario * math.cos(v + u)) * math.cos(u)
                y = (radio_principal + radio_secundario * math.cos(v + u)) * math.sin(u)
                z = radio_secundario * math.sin(v + u)
                
                puntos.append((x, y, z))
        
        try:
            superficie = cmds.surface(p=puntos, degree=3, n=nombre)
            cmds.parent(superficie, self.grupo_ciudad)
            return superficie
        except:
            return None

    # ===== GENERADORES DE EDIFICIOS =====
    
    def _crear_edificio_espiral(self, x, z, index):
        """Crea edificio con forma de espiral"""
        altura = random.uniform(self.config['altura_min'], self.config['altura_max'])
        radio_base = random.uniform(4, 10)
        
        # Crear base
        edificio = cmds.polyCylinder(
            radius=radio_base,
            height=altura,
            sx=2, sy=6, sz=2,
            name=f"edificio_espiral_{index}"
        )[0]
        
        cmds.move(x, altura/2, z, edificio)
        cmds.parent(edificio, self.grupo_ciudad)
        #self._aplicar_material_futurista(edificio)
        self._aplicar_deformaciones(edificio, altura)
        
        return edificio
    
    def _crear_edificio_onda(self, x, z, index):
        """Crea edificio con forma de onda sinusoidal"""
        altura = random.uniform(self.config['altura_min'], self.config['altura_max'])
        
        # Crear base rectangular
        edificio = cmds.polyCube(
            width=random.uniform(8, 20),
            height=altura,
            depth=random.uniform(8, 20),
            name=f"edificio_onda_{index}"
        )[0]
        
        cmds.move(x, altura/2, z, edificio)
        
        # Aplicar deformación de onda
        deformador = cmds.nonLinear(edificio, type='sine', name=f"sine_{index}")
        cmds.setAttr(deformador[0] + ".wavelength", random.uniform(2, 5))
        cmds.setAttr(deformador[0] + ".amplitude", random.uniform(0.5, 1.5))
        cmds.setAttr(deformador[0] + ".offset", random.uniform(0, 10))
        
        cmds.delete(edificio, constructionHistory=True)
        cmds.parent(edificio, self.grupo_ciudad)
        
        #self._aplicar_material_futurista(edificio)
        self._aplicar_deformaciones(edificio, altura)
        return edificio
    
    def _crear_edificio_torsion(self, x, z, index):
        """Crea edificio con torsión extrema"""
        altura = random.uniform(self.config['altura_min'], self.config['altura_max'])
        
        edificio = cmds.polyCube(
            width=random.uniform(8, 20),
            height=altura,
            depth=random.uniform(8, 20),
            sx=2, sy=6, sz=2,
            name=f"edificio_torsion_{index}"
        )[0]
        
        cmds.move(x, altura/2, z, edificio)
        cmds.parent(edificio, self.grupo_ciudad)

        
        #self._aplicar_material_futurista(edificio)
        self._aplicar_deformaciones(edificio, altura)
        return edificio
    
    def _crear_edificio_fractal(self, x, z, index):
        """Crea edificio con estructura fractal simple"""
        altura = random.uniform(20, 100)
        
        # Base principal
        base = cmds.polyCube(
            width=10, height=altura, depth=10,
            name=f"edificio_fractal_{index}_base"
        )[0]
        
        cmds.move(x, altura/2, z, base)
        
        # Niveles fractales
        for nivel in range(3):
            escala = 2 ** nivel
            sub_altura = altura * 0.3
            
            for i in range(4):
                offset_x = random.uniform(-5, 11) * (nivel + 1)
                offset_z = random.uniform(-11, 5) * (nivel + 1)
                
                sub_edificio = cmds.polyCube(
                    width=nivel * escala,
                    height=sub_altura,
                    depth=nivel * escala,
                    name=f"edificio_fractal_{index}_n{nivel}_{i}"
                )[0]
                
                cmds.move(
                    x + offset_x, 
                    altura + (nivel * sub_altura), 
                    z + offset_z, 
                    sub_edificio
                )
                cmds.parent(sub_edificio, base)
        
        cmds.parent(base, self.grupo_ciudad)
        #self._aplicar_material_futurista(base)
        
        return base

    def _aplicar_deformaciones(self, objeto, altura):
        """Aplica twist y bend controlado eliminando historial"""
        
        # ---------------------
        # 1. TWIST CONTROLADO
        # ---------------------
        twist, twist_handle = cmds.nonLinear(objeto, type='twist', name=f"{objeto}_twist")
        
        low = random.uniform(-5, 0)
        high = random.uniform(5, 10)
        angle = random.uniform(-300, 300)

        cmds.setAttr(twist + ".lowBound", low)
        cmds.setAttr(twist + ".highBound", high)
        cmds.setAttr(twist + ".startAngle", angle)

        # Opción: inclinar el handle random
        cmds.rotate(0, random.uniform(0, 360), 0, twist_handle)

        # Congelar twist y borrar historia
        cmds.delete(objeto, constructionHistory=True)


        # ---------------------
        # 2. BEND CONTROLADO
        # ---------------------
        bend, bend_handle = cmds.nonLinear(objeto, type='bend', name=f"{objeto}_bend")

        cmds.setAttr(bend + ".curvature", random.uniform(-50, 50))
        cmds.setAttr(bend + ".lowBound", 0)
        cmds.setAttr(bend + ".highBound", altura * 0.5)

        cmds.rotate(0, random.uniform(0, 90), 0, bend_handle)

        # Congelar bend y borrar historia
        cmds.delete(objeto, constructionHistory=True)

        return True
