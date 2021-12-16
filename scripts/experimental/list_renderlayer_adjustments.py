#!/usr/bin/env python
"""
Prints all the render layer overrides
"""
import maya.cmds as cmds


def main(layer_name):
    layer_adjustments = cmds.editRenderLayerAdjustment(
        layer_name, query=True, layer=True)
    for adj in layer_adjustments:
        val = cmds.getAttr(adj)
        print adj + " = " + val


if __name__ == '__main__':
    render_layer = 'layerName'
    main(render_layer)
