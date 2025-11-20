import maya.cmds as cmds
import maya.api.OpenMaya as om

# DEFINIR NOMBRES ESTÁNDAR
NOMBRES_ESTANDAR = {
    "chasis": "axioma_carro",
    "ruedas": ["rueda_delantera_izquierda", "rueda_delantera_derecha", 
               "rueda_trasera_izquierda", "rueda_trasera_derecha"],
    "grupo_rig": "RIG_CARRO_GRP"
}

def get_face_center(obj, face_index):
    """Devuelve el centro de una cara dada de un objeto."""
    try:
        sel_list = om.MSelectionList()
        sel_list.add(f"{obj}.f[{face_index}]")
        dag_path, comp = sel_list.getComponent(0)
        mfn_mesh = om.MFnMesh(dag_path)
        face_points = mfn_mesh.getPolygonVertices(face_index)
        points = [mfn_mesh.getPoint(vtx, om.MSpace.kWorld) for vtx in face_points]
        avg_point = om.MPoint(
            sum(p.x for p in points) / len(points),
            sum(p.y for p in points) / len(points),
            sum(p.z for p in points) / len(points)
        )
        return [avg_point.x, avg_point.y, avg_point.z]
    except:
        # Fallback: usar bounding box
        bb = cmds.exactWorldBoundingBox(obj)
        return [(bb[0]+bb[3])/2, (bb[1]+bb[4])/2, (bb[2]+bb[5])/2]

def align_joint_to_position(joint, position):
    cmds.xform(joint, ws=True, t=position)

def align_to_object_center(obj):
    """Devuelve el centro de un objeto."""
    bb = cmds.exactWorldBoundingBox(obj)
    return [(bb[0]+bb[3])/2, (bb[1]+bb[4])/2, (bb[2]+bb[5])/2]

def create_control(name, position, radius=1.0, color_index=6):
    """Crea un control circular en la posición dada."""
    ctrl = cmds.circle(name=name, nr=(0,1,0), r=radius)[0]
    grp = cmds.group(ctrl, name=f"{name}_GRP")
    cmds.xform(grp, ws=True, t=position)
    shape = cmds.listRelatives(ctrl, s=True)[0]
    cmds.setAttr(shape + ".overrideEnabled", 1)
    cmds.setAttr(shape + ".overrideColor", color_index)
    return ctrl, grp

def buscar_objetos_escena_filtrado():
    """Busca objetos de carro en la escena"""
    objetos = cmds.ls(transforms=True, long=False)
    
    chasis = None
    ruedas = []
    ejes = []
    
    # Objetos de Maya que debemos ignorar
    objetos_ignorar = ["persp", "front", "side", "top"]
    
    for obj in objetos:
        if obj in objetos_ignorar:
            continue
            
        lower_obj = obj.lower()
        
        # Chasis
        if not chasis and "axioma_carro" in lower_obj:
            chasis = obj
        elif not chasis and any(word in lower_obj for word in ["chasis", "body", "carro", "car"]):
            chasis = obj
        
        # Ruedas
        elif any(word in lower_obj for word in ["rueda", "wheel", "llanta", "tire"]):
            ruedas.append(obj)
        
        # Ejes
        elif any(word in lower_obj for word in ["eje", "axis", "axle"]):
            ejes.append(obj)
    
    print(f"🔍 Objetos encontrados - Chasis: {chasis}, Ruedas: {len(ruedas)}, Ejes: {len(ejes)}")
    return chasis, ruedas, ejes

# Función alias para compatibilidad
def buscar_objetos_escena():
    """Alias para compatibilidad con código existente"""
    return buscar_objetos_escena_filtrado()