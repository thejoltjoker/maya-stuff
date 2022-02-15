#!/usr/bin/env python
"""
change_override_colors.py
Description of change_override_colors.py.
"""

import maya.cmds as cmds


def main():
    """docstring for main"""

    for node in cmds.ls(sl=True):
        if node.endswith('_ctrl'):
            cmds.setAttr(node + ".overrideEnabled", 1)

            # Red color if it's the right side
            if node.startswith('r_'):
                cmds.setAttr(node + ".overrideColor", 13)
                # Other blue color for offset
                if node.endswith('Offset_ctrl'):
                    cmds.setAttr(node + ".overrideColor", 20)

            # Blue color if it's the left side
            elif node.startswith('l_'):
                cmds.setAttr(node + ".overrideColor", 6)
                # Other blue color for offset
                if node.endswith('Offset_ctrl'):
                    cmds.setAttr(node + ".overrideColor", 18)

            else:
                cmds.setAttr(node + ".overrideColor", 17)

                # Other yellow color for offset
                if node.endswith('Offset_ctrl'):
                    cmds.setAttr(node + ".overrideColor", 21)


if __name__ == '__main__':
    main()
