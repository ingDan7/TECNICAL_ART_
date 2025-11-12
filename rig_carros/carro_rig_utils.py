import maya.cmds as cmds
import maya.api.OpenMaya as om

def get_face_center(obj, face_index):
    """Devuelve el centro de una cara dada de un objeto."""
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