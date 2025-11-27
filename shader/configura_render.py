import maya.cmds as cmds
import random
import os

def crear_camera(carro="axioma_carro", cam_name="camera_render"):

    # Crear cámara si no existe
    if cmds.objExists(cam_name):
        cam = cam_name
        cam_shape = cmds.listRelatives(cam, shapes=True)[0]
    else:
        # Crear transform + shape
        cam, shape = cmds.camera()

        # Renombrar transform
        cam = cmds.rename(cam, cam_name)

        # Volver a obtener el shape REAL y renombrarlo
        cam_shape = cmds.listRelatives(cam, shapes=True)[0]
        cam_shape = cmds.rename(cam_shape, cam_name + "Shape")

        # Mover y freeze antes del aim
        cmds.xform(cam, ws=True, t=(0, 0, 10))
        cmds.makeIdentity(cam, apply=True, translate=True, rotate=True, scale=True)

    # Validar target
    if not cmds.objExists(carro):
        cmds.warning(f"No existe el objeto/grupo '{carro}'")
        return

    # Crear aimConstraint si no existe
    aim_name = cam_name + "_aimConstraint1"
    if not cmds.objExists(aim_name):
        cons = cmds.aimConstraint(
            carro, cam,
            mo=True,
            weight=1,
            aimVector=(1, 0, 0),
            upVector=(0, 1, 0),
            worldUpType="vector",
            worldUpVector=(0, 1, 0)
        )[0]
        cmds.rename(cons, aim_name)

    # Movimiento aleatorio
    def rand_x_outside(min_abs=2.5, low=-5.0, high=5.0):
        return random.uniform(low, -min_abs) if random.random() < 0.5 else random.uniform(min_abs, high)

    rand_x = rand_x_outside()
    rand_y = random.uniform(1, 7)
    rand_z = random.uniform(-5, 5)

    cmds.setAttr(cam + ".translateX", rand_x)
    cmds.setAttr(cam + ".translateY", rand_y)
    cmds.setAttr(cam + ".translateZ", rand_z)

    # Focal aleatoria
    cmds.setAttr(cam_shape + ".focalLength", random.uniform(5, 10))

    print("📸 Cámara:", cam)
    print("🎯 AimConstraint:", aim_name)

def cambiar_motor_render():
    # Cambiar motor de render a Maya Software
    cmds.setAttr("defaultRenderGlobals.currentRenderer", "mayaSoftware", type="string")

    # Configurar resolución de imagen a 1K (1024x1024)
    cmds.setAttr("defaultResolution.width", 1024)
    cmds.setAttr("defaultResolution.height", 1024)

    # Cambiar formato de salida a JPG
    cmds.setAttr("defaultRenderGlobals.imageFormat", 8)

    print("Render configurado a Maya Software con resolución 1K (1024x1024) en formato JPG.")

def renderizar_escena(cam_name="camera_render"):
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    output_path = os.path.join(escritorio, "render_output.png")

    # Validar cámara
    if not cmds.objExists(cam_name):
        cmds.warning(f"La cámara '{cam_name}' no existe.")
        return

    # Obtener panel de modelado
    panel = cmds.getPanel(withFocus=True)
    if not cmds.getPanel(typeOf=panel) == "modelPanel":
        model_panels = cmds.getPanel(type="modelPanel")
        if model_panels:
            panel = model_panels[0]
        else:
            cmds.error("No hay ningún modelPanel disponible.")
            return

    # Cambiar vista a la cámara
    try:
        cmds.lookThru(panel, cam_name)
        cmds.modelEditor(panel, e=True, camera=cam_name)
        print(f"📷 Vista del panel '{panel}' cambiada a la cámara '{cam_name}'")
    except Exception as e:
        cmds.warning(f"No se pudo aplicar lookThru: {e}")

    # 🚀 ***Abrir Render View ANTES del render***
    try:
        cmds.RenderViewWindow()
    except:
        cmds.showWindow("renderViewWindow")

    # Render normal en la Render View
    cmds.render(cam_name)

    print("Render ejecutado en Render View.")



def guardar_render(nombre="render_output"):
    # Ruta al escritorio del usuario
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    ruta_salida = os.path.join(escritorio, f"{nombre}.png")

    # Renderizar el frame actual en el Render View
    cmds.render()

    # Guardar la imagen desde el Render View
    # "renderView" es el editor por defecto
    cmds.renderWindowEditor("renderView",
                            e=True,
                            writeImage=ruta_salida)

    print(f"Render guardado en: {ruta_salida}")
    return ruta_salida

def crear_spot_lights():
    # Borra si ya existen para evitar duplicados
    for luz in ["spotLight1", "spotLight2"]:
        if cmds.objExists(luz):
            cmds.delete(luz)

    # Primer Spot Light
    luz1 = cmds.spotLight(name="spotLight1", rgb=(1,1,1), coneAngle=40, penumbra=0)
    luz1_transform = cmds.listRelatives(luz1, parent=True)[0]
    cmds.setAttr(luz1_transform + ".translateX", 10)
    cmds.setAttr(luz1_transform + ".translateY", 9)
    cmds.setAttr(luz1_transform + ".translateZ", 12)
    cmds.setAttr(luz1_transform + ".rotateX", -33)
    cmds.setAttr(luz1_transform + ".rotateY", 42)
    # Ajustes extra
    cmds.setAttr(luz1 + ".intensity", 10)
    cmds.setAttr(luz1 + ".decayRate", 1)
    cmds.setAttr(luz1 + ".dropoff", 0)

    # Segundo Spot Light
    luz2 = cmds.spotLight(name="spotLight2", rgb=(1,1,1), coneAngle=47.145585, penumbra=-10)
    luz2_transform = cmds.listRelatives(luz2, parent=True)[0]
    cmds.setAttr(luz2_transform + ".translateX", -9)
    cmds.setAttr(luz2_transform + ".translateY", 5)
    cmds.setAttr(luz2_transform + ".translateZ", -5)
    cmds.setAttr(luz2_transform + ".rotateX", -32)
    cmds.setAttr(luz2_transform + ".rotateY", -115)
    # Ajustes extra
    cmds.setAttr(luz2 + ".intensity", 50)
    cmds.setAttr(luz2 + ".decayRate", 1)
    cmds.setAttr(luz2 + ".dropoff", 0)

    print("✅ Spot lights creados correctamente.")




def ejecutar_render():
    cambiar_motor_render()
    renderizar_escena()
    crear_spot_lights()

# Llamada principal
ejecutar_render()