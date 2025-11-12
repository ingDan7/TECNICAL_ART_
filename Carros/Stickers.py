# SnapPlaneToFace.py
# Uso: pegar un plano a una cara seleccionada (centro + orientación)
import maya.cmds as cmds
import maya.api.OpenMaya as om
import math
import re

WINDOW_NAME = "snapPlaneToFaceWindow"

# ---- utilidades ----
def _get_first_selected():
    sel = cmds.ls(sl=True, fl=True)
    return sel[0] if sel else None

def _parse_face_index(face_str):
    """Devuelve (meshName, faceIndex) si face_str es tipo 'mesh.f[12]'"""
    m = re.match(r"^([^\s]+?)\.f\[(\d+)(?:[:\]]).*", face_str)
    if m:
        return m.group(1), int(m.group(2))
    # fallback simple
    if ".f[" in face_str:
        mesh = face_str.split(".f[")[0]
        idx_part = face_str.split(".f[")[1].split("]")[0]
        idx = int(idx_part.split(":")[0])
        return mesh, idx
    raise RuntimeError("No es una cara válida: {}".format(face_str))

def _get_face_center_and_normal(face_str):
    """
    Retorna (centerPoint (MPoint), normal (MVector)) en espacio mundial.
    face_str ejemplo: "pCube1.f[3]"
    """
    mesh, fidx = _parse_face_index(face_str)
    sel = om.MSelectionList()
    sel.add(mesh)
    dag = sel.getDagPath(0)
    fnMesh = om.MFnMesh(dag)

    vert_ids = fnMesh.getPolygonVertices(fidx)
    pts = [fnMesh.getPoint(vid, om.MSpace.kWorld) for vid in vert_ids]
    center = om.MPoint(0.0, 0.0, 0.0)
    for p in pts:
        center += p
    center /= len(pts)

    normal = fnMesh.getPolygonNormal(fidx, om.MSpace.kWorld)
    normal = normal.normalize()
    return center, normal

def _vector_to_euler_deg(from_vec, to_vec):
    """
    Calcula rotación (Euler XYZ, en grados) que rota from_vec hacia to_vec.
    from_vec y to_vec son MVector (deben estar normalizados o se normalizan aquí).
    """
    a = om.MVector(from_vec).normalize()
    b = om.MVector(to_vec).normalize()
    dot = max(-1.0, min(1.0, a * b))
    if dot > 0.999999:
        # ya alineado
        return (0.0, 0.0, 0.0)
    if dot < -0.999999:
        # opuesto: rotación 180 alrededor de cualquier eje perpendicular
        # elegimos X axis perpendicular
        axis = a ^ om.MVector(1, 0, 0)
        if axis.length() < 1e-6:
            axis = a ^ om.MVector(0, 1, 0)
        axis = axis.normalize()
        q = om.MQuaternion(math.pi, axis)
    else:
        axis = a ^ b
        axis = axis.normalize()
        angle = math.acos(dot)
        q = om.MQuaternion(angle, axis)
    euler = q.asEulerRotation()  # radianes
    return (math.degrees(euler.x), math.degrees(euler.y), math.degrees(euler.z))

# ---- lógica principal ----
class SnapToolState:
    plane = None   # string (transform or shape)
    face = None    # string "mesh.f[idx]"
    offset = 0.0

_state = SnapToolState()

def pick_plane_from_selection(*args):
    sel = cmds.ls(sl=True, l=True)
    if not sel:
        cmds.warning("Selecciona primero el plano (transform) en el viewport.")
        return
    # preferir transform (no componente)
    obj = sel[0]
    # si es componente, tomar su transform padre
    if "|" in obj and ".f[" in obj:
        obj = obj.split(".f[")[0]
    # si es shape, obtener transform
    if cmds.objectType(obj, isType='shape'):
        obj = cmds.listRelatives(obj, p=True, f=True)[0]
    _state.plane = obj
    cmds.textField('planeField', e=True, text=_state.plane)

def pick_face_from_selection(*args):
    sel = cmds.ls(sl=True, fl=True)
    if not sel:
        cmds.warning("Selecciona la cara (component mode) en el viewport.")
        return
    # tomar primer seleccionado que parezca .f[]
    face = None
    for s in sel:
        if ".f[" in s:
            face = s
            break
    if not face:
        cmds.warning("Selecciona una cara (component face) de la malla.")
        return
    _state.face = face
    cmds.textField('faceField', e=True, text=_state.face)

def snap_plane_to_face(*args):
    if not _state.plane or not _state.face:
        # también intentar inferir de selection (plane primero, face luego)
        sel = cmds.ls(sl=True, fl=True)
        if sel and len(sel) >= 2:
            # intentar inferir: primer object sin componente = plane, último con '.f[' = face
            plane_candidate = None
            face_candidate = None
            for s in sel:
                if ".f[" in s:
                    face_candidate = s
                else:
                    plane_candidate = s
            if plane_candidate and face_candidate:
                _state.plane = plane_candidate if not _state.plane else _state.plane
                _state.face = face_candidate if not _state.face else _state.face
            else:
                cmds.warning("No pude inferir plane y face de la selección. Usa los botones Pick.")
                return
        else:
            cmds.warning("Debes seleccionar un plano y una cara antes de hacer snap.")
            return

    # obtener centro y normal de la cara
    try:
        center, normal = _get_face_center_and_normal(_state.face)
    except Exception as e:
        cmds.error("Error al obtener la cara: {}".format(e))
        return

    # asumimos que el 'up' local del plano es Y (0,1,0). Si tu plano tiene otra orientación,
    # puedes cambiar from_vec.
    from_vec = om.MVector(0, 1, 0)
    to_vec = om.MVector(normal).normalize()

    # calcular rotación
    rot_deg = _vector_to_euler_deg(from_vec, to_vec)

    # aplicar traducción y rotación en world space
    pos = (center.x + _state.offset * to_vec.x,
           center.y + _state.offset * to_vec.y,
           center.z + _state.offset * to_vec.z)
    try:
        cmds.xform(_state.plane, ws=True, t=pos)
        cmds.xform(_state.plane, ws=True, rotation=rot_deg)
        cmds.select(_state.plane, r=True)
        cmds.inViewMessage(amg='Plane <hl>{}</hl> pegado a cara <hl>{}</hl>'.format(_state.plane, _state.face), pos='midCenter', fade=True)
    except Exception as e:
        cmds.error("Error aplicando transform: {}".format(e))

def set_offset_from_ui(*args):
    val = cmds.floatField('offsetField', q=True, v=True)
    _state.offset = val

def clear_selection(*args):
    _state.plane = None
    _state.face = None
    cmds.textField('planeField', e=True, text="")
    cmds.textField('faceField', e=True, text="")
    cmds.floatField('offsetField', e=True, v=0.0)
    _state.offset = 0.0
def build_ui():
    # elimina ventana previa si existe
    if cmds.window(WINDOW_NAME, exists=True):
        cmds.deleteUI(WINDOW_NAME)

    cmds.window(WINDOW_NAME, title="Snap Plane to Face", widthHeight=(420,160))
    # layout principal vertical
    cmds.columnLayout(adjustableColumn=True, columnAlign='center', rowSpacing=6, parent=WINDOW_NAME)

    # Campos de texto (no editables)
    cmds.textField('planeField', editable=False, placeholderText="Plane (pick or select then click Pick Plane)")
    cmds.textField('faceField',  editable=False, placeholderText="Face (select face component then click Pick Face)")

    # fila con los botones Pick
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(200,200), adjustableColumn=2)
    cmds.button(label="Pick Plane from Selection", command=pick_plane_from_selection, height=30)
    cmds.button(label="Pick Face from Selection",  command=pick_face_from_selection,  height=30)
    cmds.setParent('..')  # salir del rowLayout

    # fila offset: label + floatField
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(80,200,40), adjustableColumn=2)
    cmds.text(label="Offset (m):", align='left')
    cmds.floatField('offsetField', value=_state.offset, step=0.1, changeCommand=set_offset_from_ui)
    # espacio pequeño
    cmds.text(label="") 
    cmds.setParent('..')

    # fila de acción: Snap y Clear
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(200,200), adjustableColumn=2)
    cmds.button(label="Snap Plane to Face", command=snap_plane_to_face, height=36, bgc=(0.2, 0.6, 0.2))
    cmds.button(label="Clear", command=clear_selection, height=36)
    cmds.setParent('..')

    # mensaje/espacio final (opcional)
    cmds.separator(height=6, style='in')

    cmds.showWindow(WINDOW_NAME)

# lanzar UI
build_ui()
