
import maya.cmds as cmds

class ExtrusionController:
    def __init__(self):
        self.history_nodes = []
    
    def _limpiar_extrusiones_anteriores(self):
        """Limpiar TODAS las extrusiones anteriores antes de aplicar nuevas"""
        print("🧹 LIMPIANDO EXTRUSIONES ANTERIORES...")
        nodos_eliminados = 0
        
        for nodo in self.history_nodes:
            if cmds.objExists(nodo):
                try:
                    cmds.delete(nodo)
                    print(f"  ✅ Eliminado nodo de extrusión: {nodo}")
                    nodos_eliminados += 1
                except Exception as e:
                    print(f"  ⚠️ No se pudo eliminar {nodo}: {e}")
        
        self.history_nodes = []
        print(f"✅ Limpieza completada - {nodos_eliminados} nodos eliminados")
    
    def _obtener_caras_correctas_rueda(self, nombre_rueda):
        """Obtener las caras CORRECTAS para cada rueda - CARAS OPUESTAS PARA IZQUIERDAS"""
        try:
            # Para ruedas DERECHAS (delantera_der, trasera_der): caras 32-47
            if "der" in nombre_rueda.lower():
                caras = list(range(32, 48))
                print(f"  🎯 Rueda DERECHA {nombre_rueda}: usando caras 32-47")
                return caras
            
            # Para ruedas IZQUIERDAS (delantera_izq, trasera_izq): caras OPUESTAS
            elif "izq" in nombre_rueda.lower():
                # CARAS OPUESTAS para llantas izquierdas - AJUSTAR SEGÚN TU MODELO
                caras = list(range(16, 32))  # Caras 16-31 como ejemplo
                print(f"  🎯 Rueda IZQUIERDA {nombre_rueda}: usando caras OPUESTAS 16-31")
                return caras
            
            else:
                # Por defecto usar caras 32-47
                caras = list(range(32, 48))
                print(f"  ⚠️ Rueda {nombre_rueda}: usando caras por defecto 32-47")
                return caras
                
        except Exception as e:
            print(f"❌ Error obteniendo caras para {nombre_rueda}: {e}")
            # Fallback a caras por defecto
            return list(range(32, 48))
    
    def extrudir_caras_rueda(self, nombre_rueda):
        """Aplicar extrusiones consecutivas a las caras CORRECTAS de una rueda"""
        try:
            # Verificar que la rueda existe
            if not cmds.objExists(nombre_rueda):
                print(f"❌ Rueda {nombre_rueda} no existe, no se puede extrudir")
                return False
            
            # OBTENER CARAS CORRECTAS para esta rueda específica
            caras = self._obtener_caras_correctas_rueda(nombre_rueda)
            
            # Convertir números de cara a formato Maya
            caras_maya = [f"{nombre_rueda}.f[{i}]" for i in caras]
            
            print(f"🔧 Aplicando extrusiones a {len(caras_maya)} caras de {nombre_rueda}")
            
            # PRIMERA EXTRUSIÓN: Escala reducida
            extrusion1 = cmds.polyExtrudeFacet(
                caras_maya,
                constructionHistory=True,
                keepFacesTogether=True,
                divisions=1,
                twist=0,
                taper=1,
                off=0,
                thickness=0,
                smoothingAngle=30
            )
            
            if not extrusion1:
                print(f"❌ Falló primera extrusión para {nombre_rueda}")
                return False
            
            # Aplicar escala 58.3%
            cmds.setAttr(f"{extrusion1[0]}.localScale", 0.583333, 0.583333, 0.583333)
            self.history_nodes.append(extrusion1[0])
            print("  ✅ Primera extrusión (escala 58.3%) aplicada")
            
            # SEGUNDA EXTRUSIÓN: Traslación hacia adentro
            extrusion2 = cmds.polyExtrudeFacet(
                caras_maya,
                constructionHistory=True,
                keepFacesTogether=True,
                divisions=1,
                twist=0,
                taper=1,
                off=0,
                thickness=0,
                smoothingAngle=30
            )
            
            if not extrusion2:
                print(f"❌ Falló segunda extrusión para {nombre_rueda}")
                return False
            
            # Aplicar traslación en Z
            cmds.setAttr(f"{extrusion2[0]}.localTranslate", 0, 0, -0.274187)
            self.history_nodes.append(extrusion2[0])
            print("  ✅ Segunda extrusión (traslación -0.274) aplicada")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en extrusión de rueda {nombre_rueda}: {e}")
            return False
    
    def extrudir_caras_chasis(self, nombre_chasis="axioma_carro"):
        """Aplicar extrusiones consecutivas a las caras del chasis"""
        try:
            # Verificar que el chasis existe
            if not cmds.objExists(nombre_chasis):
                print(f"❌ Chasis {nombre_chasis} no existe, no se puede extrudir")
                return False
            
            caras = list(range(10, 14))  # Caras 10-13 del chasis
            
            # Convertir números de cara a formato Maya
            caras_maya = [f"{nombre_chasis}.f[{i}]" for i in caras]
            
            print(f"🔧 Aplicando extrusiones a {len(caras_maya)} caras del chasis")
            
            # PRIMERA EXTRUSIÓN DEL CHASIS
            extrusion1 = cmds.polyExtrudeFacet(
                caras_maya,
                constructionHistory=True,
                keepFacesTogether=True,
                divisions=1,
                twist=0,
                taper=1,
                off=0,
                thickness=0,
                smoothingAngle=30
            )
            
            if not extrusion1:
                print("❌ Falló primera extrusión del chasis")
                return False
            
            # Aplicar escala específica Y reducida
            cmds.setAttr(f"{extrusion1[0]}.localScale", 1, 0.890945, 1)
            self.history_nodes.append(extrusion1[0])
            print("  ✅ Primera extrusión chasis (escala Y 89%) aplicada")
            
            # SEGUNDA EXTRUSIÓN DEL CHASIS
            extrusion2 = cmds.polyExtrudeFacet(
                caras_maya,
                constructionHistory=True,
                keepFacesTogether=True,
                divisions=1,
                twist=0,
                taper=1,
                off=0,
                thickness=0,
                smoothingAngle=30
            )
            
            if not extrusion2:
                print("❌ Falló segunda extrusión del chasis")
                return False
            
            # Aplicar escala uniforme 85%
            cmds.setAttr(f"{extrusion2[0]}.localScale", 0.85, 0.85, 0.85)
            self.history_nodes.append(extrusion2[0])
            print("  ✅ Segunda extrusión chasis (escala 85%) aplicada")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en extrusión de chasis: {e}")
            return False
    
    def aplicar_extrusion_automatica(self, ruedas_controller=None):
        """Aplicar TODAS las extrusiones automáticamente - VERSIÓN MEJORADA"""
        try:
            print("🎯 INICIANDO EXTRUSIÓN AUTOMÁTICA DESDE CERO...")
            
            # ✅ SIEMPRE LIMPIAR EXTRUSIONES ANTERIORES ANTES DE APLICAR NUEVAS
            self._limpiar_extrusiones_anteriores()
            
            # 1. Extruir caras del chasis (si existe)
            chasis_exitoso = False
            if cmds.objExists("axioma_carro"):
                resultado_chasis = self.extrudir_caras_chasis("axioma_carro")
                if resultado_chasis:
                    chasis_exitoso = True
                    print("✅ Chasis extrudido exitosamente")
                else:
                    print("⚠️ No se pudo extrudir el chasis")
            else:
                print("ℹ️ Chasis 'axioma_carro' no encontrado")
            
            # 2. ✅ EXTRUIR LAS 4 LLANTAS CON CARAS CORRECTAS
            todas_las_ruedas = []
            
            # Buscar ruedas desde el controlador
            if ruedas_controller and hasattr(ruedas_controller, 'ruedas'):
                for posicion, nombre_rueda in ruedas_controller.ruedas.items():
                    if cmds.objExists(nombre_rueda):
                        todas_las_ruedas.append(nombre_rueda)
                        print(f"🔍 Rueda encontrada: {nombre_rueda}")
            
            # Si no se encontraron, buscar manualmente
            if not todas_las_ruedas:
                print("ℹ️ Buscando ruedas manualmente...")
                ruedas_manual = ["rueda_delantera_izq", "rueda_delantera_der", 
                               "rueda_trasera_izq", "rueda_trasera_der"]
                for rueda in ruedas_manual:
                    if cmds.objExists(rueda):
                        todas_las_ruedas.append(rueda)
                        print(f"🔍 Rueda manual encontrada: {rueda}")
            
            # Aplicar extrusiones a TODAS las ruedas encontradas
            ruedas_procesadas = 0
            for rueda in todas_las_ruedas:
                if cmds.objExists(rueda):
                    resultado = self.extrudir_caras_rueda(rueda)
                    if resultado:
                        print(f"  ✅ Rueda {rueda} procesada exitosamente")
                        ruedas_procesadas += 1
                    else:
                        print(f"  ⚠️ Rueda {rueda} falló al procesar")
                else:
                    print(f"  ⚠️ Rueda {rueda} no existe en la escena")
            
            print(f"🎉 EXTRUSIÓN AUTOMÁTICA COMPLETADA - {ruedas_procesadas}/4 ruedas procesadas + chasis: {chasis_exitoso}")
            return ruedas_procesadas > 0 or chasis_exitoso
            
        except Exception as e:
            print(f"❌ Error en extrusión automática: {e}")
            return False
    
    def limpiar_historial(self):
        """Limpiar nodos de historial de extrusión"""
        self._limpiar_extrusiones_anteriores()

# USO RÁPIDO - EJEMPLO DE IMPLEMENTACIÓN
def ejecutar_extrusion_automatica():
    """Función para ejecutar rápidamente todas las extrusiones"""
    extrusion_controller = ExtrusionController()
    
    # Aplicar todas las extrusiones automáticamente
    resultado = extrusion_controller.aplicar_extrusion_automatica()
    
    if resultado:
        print("✨ Todas las extrusiones aplicadas exitosamente")
    else:
        print("⚠️ Algunas extrusiones fallaron")
    
    return extrusion_controller

# También puedes usar los métodos individualmente:
def extrudir_solo_chasis():
    """Extruir solo las caras del chasis"""
    controller = ExtrusionController()
    controller.extrudir_caras_chasis()
    return controller

def extrudir_solo_ruedas():
    """Extruir solo las caras de las ruedas"""
    controller = ExtrusionController()
    controller.aplicar_extrusion_automatica(aplicar_chasis=False)
    return controller