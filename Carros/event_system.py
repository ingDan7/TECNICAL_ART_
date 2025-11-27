class EventSystem:
    """Sistema de eventos REAL singleton"""
    
    _instance = None
    _listeners = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventSystem, cls).__new__(cls)
            cls._listeners = {}
            print("🎯 EventSystem SINGLETON INICIALIZADO")
        return cls._instance
    
    @classmethod
    def subscribe(cls, event_type, callback):
        """Suscribir un callback a un tipo de evento"""
        if event_type not in cls._listeners:
            cls._listeners[event_type] = []
        
        if callback not in cls._listeners[event_type]:
            cls._listeners[event_type].append(callback)
            print(f"🔔 SUSCRITO: '{event_type}' - Callbacks: {len(cls._listeners[event_type])}")
    
    @classmethod
    def emit(cls, event_type, data=None):
        """Emitir un evento a todos los listeners suscritos"""
        print(f"🎯 EMITIENDO: '{event_type}'")
        
        if event_type in cls._listeners and cls._listeners[event_type]:
            for callback in cls._listeners[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"❌ Error en callback: {e}")
        else:
            print(f"⚠️ NO HAY LISTENERS para: '{event_type}'")
    
    @classmethod
    def unsubscribe(cls, event_type, callback):
        """Desuscribir un callback de un tipo de evento"""
        if event_type in cls._listeners and callback in cls._listeners[event_type]:
            cls._listeners[event_type].remove(callback)

# Definir eventos como constantes
EVENT_EMERGIR_CARRO = "emergir_carro"
EVENT_LIMPIAR_ESCENA = "limpiar_escena" 
EVENT_ACTUALIZAR_VERTICES = "actualizar_vertices"
EVENT_ACTUALIZAR_RUEDAS = "actualizar_ruedas"
EVENT_ACTUALIZAR_EXTRUSION = "actualizar_extrusion"
EVENT_ACTUALIZAR_UI_RUEDAS = "actualizar_ui_ruedas"
EVENT_ACTUALIZAR_UI_EXTRUSION = "actualizar_ui_extrusion"
EVENT_MOVER_VERTICES = "mover_vertices"
EVENT_RESET_VERTICES = "reset_vertices"