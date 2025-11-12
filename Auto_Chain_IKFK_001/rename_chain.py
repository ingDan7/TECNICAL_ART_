# File: rename_chain.py
import maya.cmds as cmds

def rename_chain(old_name, new_name):
    """Renombra un objeto si existe y retorna el nuevo nombre."""
    if cmds.objExists(old_name):
        return cmds.rename(old_name, new_name)
    return None







