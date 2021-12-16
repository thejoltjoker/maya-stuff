#!/usr/bin/env python
"""
add_sel_to_disp_layer.py
Add selected objects to a specified display layer.
"""

import maya.cmds as cmds


def main():
    """docstring for main"""

    my_sel = cmds.ls(sl=True)
    layer_sel = cmds.ls(type='displayLayer')
    for i in layer_sel:
        print(i)
    cmds.editDisplayLayerMembers('displayLayer1', my_sel)


if __name__ == '__main__':
    main()
