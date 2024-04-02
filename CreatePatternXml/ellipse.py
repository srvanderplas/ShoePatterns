import helper
import xml.etree.ElementTree as ET

'''
Attributes
    Transform: 1, matrix(<a> <b> <c> <d> <e> <f>)
                    matrix(-0.34202015,-0.93969262,-0.93969262,0.34202015,0,0) -> (1 b c| d e f| 0 0 1)
                    (xNew yNew 1)' = M(xPrev yPrev 1)'
                    xNew = a*xPrev + c*yPrev + e
                    yNew = b*xPrev + d*yPrev + f
                    1 = 1
                    note: box has four coords, then will compute two sets of matrix operation
               2, translate(<x> [<y>])
                    y not provided, y=x
                    xNew = xPrev + <x>
                    yNew = yPrev + <y>
               3, 
    cx: center coordinate of x
    cy: center coordinate of y
    rx: x-radius of the shape 
    ry: y-radius of the shape
        A Note HERE: rx and ry are equivalent still marked as ellipse. NEED TO DIFFERENTIATE WITH CIRCLE
                     maybe write a function to do that????
    style:
        Fill: None/hexcode Filled in color 
        Stroke: outline color, hexcode
        stroke-width: outline width
        stroke-opcity: outline opacity 0 is transparent, 1 is opaque
        stroke-dasharray: two array numbers, when filled color=stroke color, we will see sketchy outline
        stroke-dashoffset: 0

'''


class Ellipse:
    def __init__(cx, cy, rx, ry) -> None:
        self.cx = cx
        self.cy = cy
        self.rx = rx
        self.ry = ry
        self.style = None

    def svg() -> object:
        return pass
        # return svg

    def coco() -> object:
        return pass
        # return cocoXml
    
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
