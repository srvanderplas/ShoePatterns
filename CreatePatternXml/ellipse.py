import helper
import xml.etree.ElementTree as ET

'''
Attributes
    Transform: rotate clockwise
    cx: center coordinate of x
    cy: center coordinate of y
    rx:
    ry:
    style:
        Fill: None/hexcode Filled in color 
        Stroke: outline color, hexcode
        stroke-width: outline width
        stroke-opcity: outline opacity 0 is transparent, 1 is opaque
        stroke-dasharray: two array numbers, when filled color=stroke color, we will see sketchy outline
        stroke-dashoffset: 0

'''

# Transform = getTransformAngle
# cx, cy = get central coords
# rx, ry = get x and y axis
# ANY CONFITION TO BE MET?
# style
    # strokeColor = helper.generateColor()
    # fill = get filled or not
        # fillcolorFlag=same with strokeColor or not
            # if fillcolorFlag==same:
                # fillColor = strokeColor
            # fillColor = helper.generateColor()
    # strokeWidth = NEED TO DECIDE THE RANGE
    # strokeOpacity = random number between 0 and 1
    # strokeDasharray = none, CAN DEVELOPE MORE...
    # strokeDasharryOffset = no dasharray, no attribute