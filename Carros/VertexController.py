import maya.cmds as cmds
import random

class VertexController:
    def __init__(self):
        # Límites para cada grupo - COHERENTES CON LA UI
        self.limites_y_pares = {'min': -0.5, 'max': 0.5}      # Para 12-13 y 14-15
        
        # RANGOS DIFERENTES PARA CADA GRUPO EN X
        self.limites_grupo_9_10_x = {'min': -0.5, 'max': 0.5}    # Más rango para frontal
        self.limites_grupo_17_18_x = {'min': -0.3, 'max': 0.3}    # Menos rango para trasero
        
        self.limites_y_individual = {'min': -0.3, 'max': 0.3} # Para 16-17 y 10-11
        
        # Estado actual de desplazamiento
        self.desplazamiento_actual = {
            'par_12_13_y': 0.0,
            'par_14_15_y': 0.0,
            'grupo_9_10_x': 0.0,
            'grupo_17_18_x': 0.0,
            'par_16_17_y': 0.0,
            'par_10_11_y': 0.0
        }
        
        # POSICIONES Y ORIGINALES para preservar
        self.posiciones_y_originales = {}
    
    # ===== FUNCIÓN CRÍTICA: PRESERVAR POSICIONES Y ORIGINALES =====
    
    def preservar_posiciones_y_originales(self):
        """Guardar las posiciones Y originales de todos los vértices"""
        try:
            print("💾 PRESERVANDO POSICIONES Y ORIGINALES...")
            
            if not cmds.objExists("axioma_carro"):
                return
            
            # Guardar posiciones Y de TODOS los vértices
            for i in range(20):  # Asumiendo máximo 20 vértices
                vertice = f"axioma_carro.vtx[{i}]"
                if cmds.objExists(vertice):
                    pos = cmds.xform(vertice, query=True, translation=True, worldSpace=True)
                    self.posiciones_y_originales[i] = pos[1]
            
            print(f"✅ Posiciones Y originales guardadas para {len(self.posiciones_y_originales)} vértices")
            
        except Exception as e:
            print(f"❌ Error preservando posiciones Y: {str(e)}")
    
    def restaurar_posiciones_y(self, vertices_indices):
        """Restaurar posiciones Y originales para vértices específicos"""
        try:
            for idx in vertices_indices:
                if idx in self.posiciones_y_originales:
                    vertice = f"axioma_carro.vtx[{idx}]"
                    if cmds.objExists(vertice):
                        pos_actual = cmds.xform(vertice, query=True, translation=True, worldSpace=True)
                        # Restaurar solo la posición Y, mantener X y Z
                        cmds.xform(vertice, translation=[pos_actual[0], self.posiciones_y_originales[idx], pos_actual[2]], worldSpace=True)
            
        except Exception as e:
            print(f"❌ Error restaurando posiciones Y: {str(e)}")
    
    # ===== FUNCIONES RANDOM PARA EMERGER - CON RANGOS INDIVIDUALES =====
    
    def aplicar_desplazamientos_aleatorios(self):
        """Aplicar desplazamientos aleatorios manteniendo la coherencia de grupos"""
        try:
            print("🎲 APLICANDO DESPLAZAMIENTOS ALEATORIOS CON RANGOS INDIVIDUALES...")
            
            # Verificar que el objeto existe
            if not cmds.objExists("axioma_carro"):
                print("❌ No existe el objeto 'axioma_carro'")
                return None
            
            # PRESERVAR posiciones Y originales ANTES de cualquier movimiento
            self.preservar_posiciones_y_originales()
            
            # DIAGNÓSTICO ANTES de aplicar desplazamientos
            posiciones_antes = self._obtener_posiciones_vertices([7, 18])
            self.diagnosticar_vertices_problematicos("ANTES de desplazamientos")
            
            # 1. CONTROL DE VÉRTICES EN EJE Y (PARES INDEPENDIENTES)
            # Par 12-13 - movimiento individual en Y
            random_12_13 = random.uniform(self.limites_y_pares['min'], self.limites_y_pares['max'])
            self.mover_par_12_13_y(random_12_13)
            
            # Par 14-15 - movimiento individual en Y (NO en unísono con 12-13)
            random_14_15 = random.uniform(self.limites_y_pares['min'], self.limites_y_pares['max'])
            self.mover_par_14_15_y(random_14_15)
            
            # 2. CONTROL DE REFLEJO EN EJE X - CON RANGOS INDIVIDUALES
            # Grupo 9-10 con reflejo en 8 y 11 - RANGO MÁS AMPLIO
            random_9_10 = random.uniform(self.limites_grupo_9_10_x['min'], self.limites_grupo_9_10_x['max'])
            self.mover_grupo_9_10_x(random_9_10)
            
            # Grupo 17-18 con reflejo en 16 y 19 - RANGO MÁS CONSERVADOR
            random_17_18 = random.uniform(self.limites_grupo_17_18_x['min'], self.limites_grupo_17_18_x['max'])
            self.mover_grupo_17_18_x(random_17_18)
            
            # 3. CONTROL ADICIONAL EN EJE Y (INDIVIDUAL)
            # Par 16-17 - control individual en Y
            random_16_17 = random.uniform(self.limites_y_individual['min'], self.limites_y_individual['max'])
            self.mover_par_16_17_y(random_16_17)
            
            # Par 10-11 - control individual en Y
            random_10_11 = random.uniform(self.limites_y_individual['min'], self.limites_y_individual['max'])
            self.mover_par_10_11_y(random_10_11)
            
            # DIAGNÓSTICO DESPUÉS de aplicar desplazamientos
            posiciones_despues = self._obtener_posiciones_vertices([7, 18])
            self.diagnosticar_vertices_problematicos("DESPUÉS de desplazamientos")
            self.verificar_movimiento_vertices_problematicos(posiciones_antes, posiciones_despues)
            
            # Si los vértices problemáticos se movieron, restaurarlos
            if self._detectar_movimiento_no_deseado(posiciones_antes, posiciones_despues):
                print("🔄 RESTAURANDO VÉRTICES PROBLEMÁTICOS...")
                self.restaurar_posiciones_y([7, 18])
                self.diagnosticar_vertices_problematicos("DESPUÉS de restauración")
            
            # Retornar los valores aplicados para actualizar UI
            desplazamientos = {
                'par_12_13_y': random_12_13,
                'par_14_15_y': random_14_15,
                'grupo_9_10_x': random_9_10,
                'grupo_17_18_x': random_17_18,
                'par_16_17_y': random_16_17,
                'par_10_11_y': random_10_11
            }
            
            print("✅ DESPLAZAMIENTOS ALEATORIOS APLICADOS CON RANGOS INDIVIDUALES")
            print(f"   Grupo 9-10 X: {random_9_10:.3f} (rango: {self.limites_grupo_9_10_x['min']:.1f} a {self.limites_grupo_9_10_x['max']:.1f})")
            print(f"   Grupo 17-18 X: {random_17_18:.3f} (rango: {self.limites_grupo_17_18_x['min']:.1f} a {self.limites_grupo_17_18_x['max']:.1f})")
            return desplazamientos
            
        except Exception as e:
            print(f"❌ ERROR en desplazamientos aleatorios: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def _detectar_movimiento_no_deseado(self, antes, despues):
        """Detectar si los vértices problemáticos se movieron indebidamente"""
        vertices_problematicos = [7, 18]
        
        for vertice_idx in vertices_problematicos:
            vertice_nombre = f"axioma_carro.vtx[{vertice_idx}]"
            
            if vertice_nombre in antes and vertice_nombre in despues:
                pos_antes = antes[vertice_nombre]
                pos_despues = despues[vertice_nombre]
                
                diferencia_y = abs(pos_despues[1] - pos_antes[1])
                if diferencia_y > 0.001:
                    return True
        return False

    # ===== FUNCIONES DE MOVIMIENTO EN X - CON LÍMITES INDIVIDUALES =====
    
    def mover_grupo_9_10_x(self, desplazamiento):
        """Mover vértices [9:10] en eje X con reflejo en [8] y [11] - SOLO EJE X"""
        try:
            # Aplicar límites ESPECÍFICOS para este grupo
            nuevo_desplazamiento = max(self.limites_grupo_9_10_x['min'],
                                     min(self.limites_grupo_9_10_x['max'], desplazamiento))
            
            # Calcular diferencia para movimiento relativo
            diferencia = nuevo_desplazamiento - self.desplazamiento_actual['grupo_9_10_x']
            
            if abs(diferencia) < 0.001:
                return
            
            print(f"🔧 MOVIENDO GRUPO 9-10 X: {nuevo_desplazamiento:.3f} (rango: {self.limites_grupo_9_10_x['min']:.1f} a {self.limites_grupo_9_10_x['max']:.1f})")
            
            # Grupo principal: [9:10] - SOLO estos vértices
            vertices_principales = [f"axioma_carro.vtx[{i}]" for i in [9, 10]]
            
            # Reflejo correspondiente: [8] y [11] - SOLO estos vértices
            vertices_reflejo = [f"axioma_carro.vtx[{i}]" for i in [8, 11]]
            
            # Mover grupo principal - SOLO EJE X, PRESERVAR Y ORIGINAL
            for vertice in vertices_principales:
                if cmds.objExists(vertice):
                    pos_actual = cmds.xform(vertice, query=True, translation=True, worldSpace=True)
                    nueva_pos_x = pos_actual[0] + diferencia
                    # PRESERVAR POSICIÓN Y ORIGINAL - NO MODIFICAR Y
                    cmds.xform(vertice, translation=[nueva_pos_x, pos_actual[1], pos_actual[2]], worldSpace=True)
            
            # Mover grupo reflejo - MOVIMIENTO INVERSO en X, PRESERVAR Y ORIGINAL
            for vertice in vertices_reflejo:
                if cmds.objExists(vertice):
                    pos_actual = cmds.xform(vertice, query=True, translation=True, worldSpace=True)
                    nueva_pos_x = pos_actual[0] - diferencia  # Movimiento inverso
                    # PRESERVAR POSICIÓN Y ORIGINAL - NO MODIFICAR Y
                    cmds.xform(vertice, translation=[nueva_pos_x, pos_actual[1], pos_actual[2]], worldSpace=True)
            
            # Actualizar estado
            self.desplazamiento_actual['grupo_9_10_x'] = nuevo_desplazamiento
            print(f"✅ Grupo 9-10 X (con reflejo 8,11) movido a: {nuevo_desplazamiento:.3f}")
            
        except Exception as e:
            cmds.warning(f"❌ Error moviendo grupo 9-10 X: {str(e)}")

    def mover_grupo_17_18_x(self, desplazamiento):
        """Mover vértices [17:18] en eje X con reflejo en [16] y [19] - SOLO EJE X"""
        try:
            # Aplicar límites ESPECÍFICOS para este grupo
            nuevo_desplazamiento = max(self.limites_grupo_17_18_x['min'],
                                     min(self.limites_grupo_17_18_x['max'], desplazamiento))
            
            # Calcular diferencia para movimiento relativo
            diferencia = nuevo_desplazamiento - self.desplazamiento_actual['grupo_17_18_x']
            
            if abs(diferencia) < 0.001:
                return
            
            print(f"🔧 MOVIENDO GRUPO 17-18 X: {nuevo_desplazamiento:.3f} (rango: {self.limites_grupo_17_18_x['min']:.1f} a {self.limites_grupo_17_18_x['max']:.1f})")
            
            # Grupo principal: [17:18] - SOLO estos vértices
            vertices_principales = [f"axioma_carro.vtx[{i}]" for i in [17, 18]]
            
            # Reflejo correspondiente: [16] y [19] - SOLO estos vértices
            vertices_reflejo = [f"axioma_carro.vtx[{i}]" for i in [16, 19]]
            
            # Mover grupo principal - SOLO EJE X, PRESERVAR Y ORIGINAL
            for vertice in vertices_principales:
                if cmds.objExists(vertice):
                    pos_actual = cmds.xform(vertice, query=True, translation=True, worldSpace=True)
                    nueva_pos_x = pos_actual[0] + diferencia
                    # PRESERVAR POSICIÓN Y ORIGINAL - NO MODIFICAR Y
                    cmds.xform(vertice, translation=[nueva_pos_x, pos_actual[1], pos_actual[2]], worldSpace=True)
            
            # Mover grupo reflejo - MOVIMIENTO INVERSO en X, PRESERVAR Y ORIGINAL
            for vertice in vertices_reflejo:
                if cmds.objExists(vertice):
                    pos_actual = cmds.xform(vertice, query=True, translation=True, worldSpace=True)
                    nueva_pos_x = pos_actual[0] - diferencia  # Movimiento inverso
                    # PRESERVAR POSICIÓN Y ORIGINAL - NO MODIFICAR Y
                    cmds.xform(vertice, translation=[nueva_pos_x, pos_actual[1], pos_actual[2]], worldSpace=True)
            
            # Actualizar estado
            self.desplazamiento_actual['grupo_17_18_x'] = nuevo_desplazamiento
            print(f"✅ Grupo 17-18 X (con reflejo 16,19) movido a: {nuevo_desplazamiento:.3f}")
            
        except Exception as e:
            cmds.warning(f"❌ Error moviendo grupo 17-18 X: {str(e)}")

    # ===== FUNCIONES DE MOVIMIENTO EN Y =====
    
    def mover_par_12_13_y(self, desplazamiento):
        """Mover vértices [12:13] en eje Y - PAR INDEPENDIENTE"""
        try:
            # Aplicar límites específicos para este grupo
            nuevo_desplazamiento = max(self.limites_y_pares['min'], 
                                     min(self.limites_y_pares['max'], desplazamiento))
            
            # Calcular diferencia para movimiento relativo
            diferencia = nuevo_desplazamiento - self.desplazamiento_actual['par_12_13_y']
            
            if abs(diferencia) < 0.001:
                return
            
            # SOLO mover vértices [12:13] - PAR INDEPENDIENTE
            vertices = [f"axioma_carro.vtx[{i}]" for i in [12, 13]]
            
            for vertice in vertices:
                if cmds.objExists(vertice):
                    pos_actual = cmds.xform(vertice, query=True, translation=True, worldSpace=True)
                    nueva_pos_y = pos_actual[1] + diferencia
                    # MANTENER X y Z - SOLO MOVER Y
                    cmds.xform(vertice, translation=[pos_actual[0], nueva_pos_y, pos_actual[2]], worldSpace=True)
            
            # Actualizar estado
            self.desplazamiento_actual['par_12_13_y'] = nuevo_desplazamiento
            print(f"✅ Par 12-13 Y (INDEPENDIENTE) movido a: {nuevo_desplazamiento:.3f}")
            
        except Exception as e:
            cmds.warning(f"❌ Error moviendo par 12-13 Y: {str(e)}")

    def mover_par_14_15_y(self, desplazamiento):
        """Mover vértices [14:15] en eje Y - PAR INDEPENDIENTE (NO en unísono)"""
        try:
            # Aplicar límites específicos para este grupo
            nuevo_desplazamiento = max(self.limites_y_pares['min'], 
                                     min(self.limites_y_pares['max'], desplazamiento))
            
            # Calcular diferencia para movimiento relativo
            diferencia = nuevo_desplazamiento - self.desplazamiento_actual['par_14_15_y']
            
            if abs(diferencia) < 0.001:
                return
            
            # SOLO mover vértices [14:15] - PAR INDEPENDIENTE
            vertices = [f"axioma_carro.vtx[{i}]" for i in [14, 15]]
            
            for vertice in vertices:
                if cmds.objExists(vertice):
                    pos_actual = cmds.xform(vertice, query=True, translation=True, worldSpace=True)
                    nueva_pos_y = pos_actual[1] + diferencia
                    # MANTENER X y Z - SOLO MOVER Y
                    cmds.xform(vertice, translation=[pos_actual[0], nueva_pos_y, pos_actual[2]], worldSpace=True)
            
            # Actualizar estado
            self.desplazamiento_actual['par_14_15_y'] = nuevo_desplazamiento
            print(f"✅ Par 14-15 Y (INDEPENDIENTE) movido a: {nuevo_desplazamiento:.3f}")
            
        except Exception as e:
            cmds.warning(f"❌ Error moviendo par 14-15 Y: {str(e)}")

    def mover_par_16_17_y(self, desplazamiento):
        """Mover vértices [16:17] en eje Y - CONTROL INDIVIDUAL"""
        try:
            # Aplicar límites específicos para este grupo
            nuevo_desplazamiento = max(self.limites_y_individual['min'], 
                                     min(self.limites_y_individual['max'], desplazamiento))
            
            # Calcular diferencia para movimiento relativo
            diferencia = nuevo_desplazamiento - self.desplazamiento_actual['par_16_17_y']
            
            if abs(diferencia) < 0.001:
                return
            
            # SOLO mover vértices [16:17] - CONTROL INDIVIDUAL
            vertices = [f"axioma_carro.vtx[{i}]" for i in [16, 17]]
            
            for vertice in vertices:
                if cmds.objExists(vertice):
                    pos_actual = cmds.xform(vertice, query=True, translation=True, worldSpace=True)
                    nueva_pos_y = pos_actual[1] + diferencia
                    # MANTENER X y Z - SOLO MOVER Y
                    cmds.xform(vertice, translation=[pos_actual[0], nueva_pos_y, pos_actual[2]], worldSpace=True)
            
            # Actualizar estado
            self.desplazamiento_actual['par_16_17_y'] = nuevo_desplazamiento
            print(f"✅ Par 16-17 Y (INDIVIDUAL) movido a: {nuevo_desplazamiento:.3f}")
            
        except Exception as e:
            cmds.warning(f"❌ Error moviendo par 16-17 Y: {str(e)}")

    def mover_par_10_11_y(self, desplazamiento):
        """Mover vértices [10:11] en eje Y - CONTROL INDIVIDUAL"""
        try:
            # Aplicar límites específicos para este grupo
            nuevo_desplazamiento = max(self.limites_y_individual['min'], 
                                     min(self.limites_y_individual['max'], desplazamiento))
            
            # Calcular diferencia para movimiento relativo
            diferencia = nuevo_desplazamiento - self.desplazamiento_actual['par_10_11_y']
            
            if abs(diferencia) < 0.001:
                return
            
            # SOLO mover vértices [10:11] - CONTROL INDIVIDUAL
            vertices = [f"axioma_carro.vtx[{i}]" for i in [10, 11]]
            
            for vertice in vertices:
                if cmds.objExists(vertice):
                    pos_actual = cmds.xform(vertice, query=True, translation=True, worldSpace=True)
                    nueva_pos_y = pos_actual[1] + diferencia
                    # MANTENER X y Z - SOLO MOVER Y
                    cmds.xform(vertice, translation=[pos_actual[0], nueva_pos_y, pos_actual[2]], worldSpace=True)
            
            # Actualizar estado
            self.desplazamiento_actual['par_10_11_y'] = nuevo_desplazamiento
            print(f"✅ Par 10-11 Y (INDIVIDUAL) movido a: {nuevo_desplazamiento:.3f}")
            
        except Exception as e:
            cmds.warning(f"❌ Error moviendo par 10-11 Y: {str(e)}")

    # ===== FUNCIONES DE RESETEO =====
    def resetear_todos_vertices(self):
        """Resetear todos los vértices a posición original"""
        try:
            print("🔄 RESETEANDO TODOS LOS VÉRTICES...")
            
            # Resetear pares en Y (independientes)
            self.mover_par_12_13_y(0.0)
            self.mover_par_14_15_y(0.0)
            
            # Resetear grupos en X con espejo
            self.mover_grupo_9_10_x(0.0)
            self.mover_grupo_17_18_x(0.0)
            
            # Resetear controles individuales en Y
            self.mover_par_16_17_y(0.0)
            self.mover_par_10_11_y(0.0)
            
            print("✅ TODOS LOS VÉRTICES RESETEADOS MANTENIENDO COHERENCIA DE GRUPOS")
            
        except Exception as e:
            cmds.warning(f"❌ Error reseteando vértices: {str(e)}")

    # ===== FUNCIONES DE SELECCIÓN =====
    
    def seleccionar_par_12_13(self):
        """Seleccionar vértices [12:13] - PAR INDEPENDIENTE"""
        cmds.select(clear=True)
        vertices = [f"axioma_carro.vtx[{i}]" for i in [12, 13]]
        cmds.select(vertices)
        print("✅ Par 12-13 seleccionado (INDEPENDIENTE)")

    def seleccionar_par_14_15(self):
        """Seleccionar vértices [14:15] - PAR INDEPENDIENTE"""
        cmds.select(clear=True)
        vertices = [f"axioma_carro.vtx[{i}]" for i in [14, 15]]
        cmds.select(vertices)
        print("✅ Par 14-15 seleccionado (INDEPENDIENTE)")

    def seleccionar_grupo_9_10(self):
        """Seleccionar vértices [9:10] y reflejos [8,11]"""
        cmds.select(clear=True)
        vertices = [f"axioma_carro.vtx[{i}]" for i in [8, 9, 10, 11]]
        cmds.select(vertices)
        print("✅ Grupo 9-10 con reflejos 8,11 seleccionado")

    def seleccionar_grupo_17_18(self):
        """Seleccionar vértices [17:18] y reflejos [16,19]"""
        cmds.select(clear=True)
        vertices = [f"axioma_carro.vtx[{i}]" for i in [16, 17, 18, 19]]
        cmds.select(vertices)
        print("✅ Grupo 17-18 con reflejos 16,19 seleccionado")

    def seleccionar_par_16_17(self):
        """Seleccionar vértices [16:17] - CONTROL INDIVIDUAL"""
        cmds.select(clear=True)
        vertices = [f"axioma_carro.vtx[{i}]" for i in [16, 17]]
        cmds.select(vertices)
        print("✅ Par 16-17 seleccionado (INDIVIDUAL)")

    def seleccionar_par_10_11(self):
        """Seleccionar vértices [10:11] - CONTROL INDIVIDUAL"""
        cmds.select(clear=True)
        vertices = [f"axioma_carro.vtx[{i}]" for i in [10, 11]]
        cmds.select(vertices)
        print("✅ Par 10-11 seleccionado (INDIVIDUAL)")

    # ===== DIAGNÓSTICO DE VÉRTICES PROBLEMÁTICOS =====
    
    def diagnosticar_vertices_problematicos(self, etapa):
        """Diagnóstico detallado de los vértices [7] y [18] en cada etapa"""
        try:
            print(f"🔍 DIAGNÓSTICO VÉRTICES [{etapa}]:")
            
            if not cmds.objExists("axioma_carro"):
                print("❌ No existe 'axioma_carro'")
                return
            
            # Vértices problemáticos y sus vecinos para comparación
            vertices_monitoreo = [6, 7, 8, 9, 10, 11, 16, 17, 18, 19]
            
            for i in vertices_monitoreo:
                vertice = f"axioma_carro.vtx[{i}]"
                if cmds.objExists(vertice):
                    pos = cmds.xform(vertice, query=True, translation=True, worldSpace=True)
                    print(f"   📍 {vertice}: X={pos[0]:.3f}, Y={pos[1]:.3f}, Z={pos[2]:.3f}")
                else:
                    print(f"   ❌ {vertice}: NO EXISTE")
                    
        except Exception as e:
            print(f"❌ Error en diagnóstico: {str(e)}")

    def _obtener_posiciones_vertices(self, indices_vertices):
        """Obtener posiciones de vértices específicos"""
        posiciones = {}
        for idx in indices_vertices:
            vertice = f"axioma_carro.vtx[{idx}]"
            if cmds.objExists(vertice):
                pos = cmds.xform(vertice, query=True, translation=True, worldSpace=True)
                posiciones[vertice] = pos
        return posiciones

    def verificar_movimiento_vertices_problematicos(self, antes, despues):
        """Verificar si los vértices problemáticos se movieron"""
        vertices_problematicos = [7, 18]
        
        for vertice_idx in vertices_problematicos:
            vertice_nombre = f"axioma_carro.vtx[{vertice_idx}]"
            
            if vertice_nombre in antes and vertice_nombre in despues:
                pos_antes = antes[vertice_nombre]
                pos_despues = despues[vertice_nombre]
                
                diferencia_y = abs(pos_despues[1] - pos_antes[1])
                if diferencia_y > 0.001:
                    print(f"⚠️ ALERTA: {vertice_nombre} se movió en Y: {diferencia_y:.3f}")
                    print(f"   Antes: Y={pos_antes[1]:.3f}, Después: Y={pos_despues[1]:.3f}")