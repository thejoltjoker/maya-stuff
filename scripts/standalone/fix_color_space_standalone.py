#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
incremental_save.py
Description of incremental_save.py.
"""
import shutil
import sys
from pathlib import Path

from maya import cmds, standalone

# !/usr/bin/env python3
"""fix_color_space.py
Description of fix_color_space.py.
"""
import logging
from maya import cmds

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
file_handler = logging.FileHandler(r'C:\temp\color_space.log')
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s: %(message)s')
handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

IGNORE = ['initialShadingGroup', 'initialShadingGroup', 'initialParticleSE', 'lambert1']

COLOR_SPACES = {'diffuse_color': 'sRGB',
                'refl_roughness': 'Raw',
                'refl_aniso_rotation': 'Raw',
                'bump_input': 'Raw',
                'refl_metalness': 'Raw'}

SCENES_TODO = []
SCENES_DONE = []


def get_inputs(node):
    """Get all input connections for a node

    Args:
        node: input node

    Returns:
        dict: input connections and nodes
    """
    inputs = {node: {}}
    if not node in IGNORE:
        # logger.info(f'Connections to {node}')
        conn = cmds.listConnections(node, s=True, d=False, c=True)
        if conn:
            for i in range(len(conn)):
                if i % 2 == 0:
                    conn_in = conn[i].split('.')[-1]
                    conn_out = conn[i + 1]
                    inputs[node]['type'] = cmds.nodeType(node)

                    if not inputs[node].get('connections'):
                        inputs[node]['connections'] = {}
                    if not conn_in.endswith('.message'):
                        # logger.info(f'{conn_in}: {conn_out}')
                        inputs[node]['connections'][conn_in] = get_inputs(conn_out)
                    else:
                        inputs[node]['connections'][conn_in] = conn_out

    return inputs


def change_colorspace(node, color_space):
    """Change the colorspace of a node

    Args:
        node: file node
        color_space: chosen color space

    Returns:

    """
    has_colorspace = cmds.attributeQuery('colorSpace', node=node, ex=True)
    attrib = node + '.colorSpace'

    if has_colorspace:
        cmds.setAttr(attrib, color_space, type='string')

    return cmds.getAttr(attrib)


def process_tree(tree, color_space='Raw'):
    """Process a dict of nodes and connections

    Args:
        tree: dict with nodes and connections. Generated by get_inputs()
        color_space: The chosen color space for the node
    """
    node = list(tree)[0]
    node_type = tree[node].get('type')

    # Check if the key has a node type or it's just a connection
    if node_type:
        if node_type == 'file':
            logger.info(f'Changing {node} input color space to {color_space}')
            change_colorspace(node, color_space)
        for k, v in tree[node].get('connections', {}).items():
            process_tree(v)


def fix_color_spaces():
    """docstring for main"""
    all_materials = cmds.ls(mat=True)

    for material in all_materials:
        logger.info(f'Processing inputs for {material}')
        inputs = get_inputs(material)

        for k, v in inputs[material].get('connections', {}).items():
            # Determine color space
            clr_space = COLOR_SPACES.get(k, 'Raw')
            logger.info(f'Changing all file input color spaces for {k} to {clr_space}')

            # Process connections
            process_tree(v, clr_space)

        print('')


def get_referenced_scenes():
    scenes = []
    reference_nodes = cmds.ls(references=True)
    for node in reference_nodes:
        path = cmds.referenceQuery(node, filename=True)
        scenes.append(path)
    return scenes


def process_scene(maya_file):
    # Make backup
    path = Path(maya_file)
    backup_path = path.parent / f'{path.name}.BAK'
    logger.info(f'Backing up {path} to {backup_path}')
    shutil.copy2(path, backup_path)
    if path not in SCENES_DONE:
        logger.info(f'Trying to open {path}')

        # Open file
        cmds.file(str(path.resolve()), open=True)

        # Fix referenced scenes
        for scene in get_referenced_scenes():
            scene_path = Path(scene)
            if scene_path.is_file():
                SCENES_TODO.append(scene_path)

        # Fix color spaces
        fix_color_spaces()

        # Save file
        cmds.file(save=True)

        # Remove scene from todo and add to done
        logger.info(f'Scenes to process: {SCENES_TODO}')
        logger.info(f'Scenes processed: {SCENES_DONE}')
        SCENES_TODO.pop(SCENES_TODO.index(path))
        SCENES_DONE.append(path)

    logger.info('Scene processed')


def main(maya_file):
    standalone.initialize()
    path = Path(maya_file)
    SCENES_TODO.append(path)
    while len(SCENES_TODO) > 0:
        process_scene(SCENES_TODO[0])
    standalone.uninitialize()
    logger.info(f'Processed the following scenes:')
    for sc in SCENES_DONE:
        logger.info(sc)


if __name__ == '__main__':
    # path = Path(sys.argv[0])
    # logger.info(path.resolve())
    # path = r'C:\Users\JohannesAndersson\OneDrive - Frank Valiant AB\Desktop\temp\scene\test_color_fix_v001.mb'
    main(sys.argv[1])
