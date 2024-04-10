import numpy as np
import helper
import xml.etree.ElementTree as ET


# Because of the wierd transformation system in SVG
# The transmations have to follow rules:
#   1, Follow Affine matrix way: Scaling + Rotation + transltion
#   2, Always specifying the center point when rotating
#   3, Each shape has it's own way of transformation

'''
Attributes
    1, translate(<x>, <y>)
                    y not provided, y=x
                    xNew = xPrev + <x>
                    yNew = yPrev + <y> 
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
    def __init__(self, cx, cy, rx, ry, 
                 transform={}, # default to a standardized ellipse, this is for simpleEllipse method only
                 ellipseLimits=None # default to none, this is for simpleEllipse method only
                #, opacity=1, 
                # fill: "#000000",
                # stroke="none",
                # strokeWidth = 0,
                # strokeLinejoin = round,
                # strokeDasharray = none,
                # strokeOpacity = 1 
                ) -> None:
                self.cx = cx
                self.cy = cy
                self.rx = rx
                self.ry = ry
                self.cx1 = self.cx
                self.cy1 = self.cy
                self.rx1 = self.rx
                self.ry1 = self.ry
                if ellipseLimits == None:
                    self.xmin = cx - rx
                    self.ymin = cy - ry
                    self.xmax = cx + rx
                    self.ymax = cy + ry
                else:
                    self.xmin, self.ymin, self.xmax, self.ymax = ellipseLimits
                self.transform = transform # keep track of transformations
                # self.opacity=1, # probably fix the input below, or just open a few
                # self.fill= "#000000"
                # self.stroke="none"
                # self.strokeWidth = 0
                # self.strokeLinejoin = "round"
                # self.strokeDasharray = "none"
                # self.strokeOpacity = 1
    
    def scale(self, sx:float, sy = None) -> list:
        # scale, keeping track of the real parameters and bbox coords
        if sy == None:
            sy = sx
        self.cx1 = sx * self.cx1
        self.cy1 = sy * self.cy1
        self.rx1 = np.abs(sx * self.rx1)
        self.ry1 = np.abs(sy * self.ry1)
        self.transform['scale'] = (sx, sy)
        
        self.xmin = self.cx1 - self.rx1
        self.ymin = self.cy1 - self.ry1
        self.xmax = self.cx1 + self.rx1
        self.ymax = self.cy1 + self.ry1

        return self


    def rotate(self, degree):
        """keep track of true parameters after rotation, only rotate against central point

        Args:
            coord (_type_): initial coords
            origin (_type_): rotate against
            degree (_type_): clockwise degree to accomodate Inkscape
        """
        
        # self.cx1, self.cy1 = helper.rotate([[self.cx1, self.cy1], (-1)*degree) 
        self.transform['rotate'] = degree

        leftPoint = [self.xmin, self.cy1]
        rightPoint = [self.xmax, self.cy1]
        topPoint = [self.cx1, self.ymax]
        bottomPoint = [self.cx1, self.ymin]

        radians = (-1)*np.deg2rad(degree) # -1 to match with clockwise rotation in Inkscape
        cosRad = np.cos(radians)
        sinRad = np.sin(radians)
        
        x1 = np.sqrt((self.rx1**2)*(cosRad**2) + (self.ry1**2)*(sinRad**2))
        x2 = 0-x1
        y1 = np.sqrt((self.rx1**2)*(sinRad**2) + (self.ry1**2)*(cosRad**2))
        y2 = 0-y1

        self.xmin, self.xmax = min(x1, x2)+self.cx1, max(x1, x2)+self.cx1
        self.ymin, self.ymax = min(y1, y2)+self.cy1, max(y1, y2)+self.cy1 

        # centerPoint = [self.cx1, self.cy1]
        # leftPointNew = helper.rotate(leftPoint, centerPoint, (-1)*degree)
        # rightPointNew = helper.rotate(rightPoint, centerPoint, (-1)*degree)
        # topPointNew = helper.rotate(topPoint, centerPoint, (-1)*degree)
        # bottomPointNew = helper.rotate(bottomPoint, centerPoint, (-1)*degree)

        # xs = [leftPointNew[0], rightPointNew[0], topPointNew[0], bottomPointNew[0]]
        # ys = [leftPointNew[1], rightPointNew[1], topPointNew[1], bottomPointNew[1]]
        # self.xmin, self.xmax, self.ymin, self.ymax = min(xs), max(xs), min(ys), max(ys)
        return self
    
    def translate(self, tx, ty=0):
        if "scale" in self.transform.keys():
            xScale, yScale = self.transform['scale']
        else:
            xScale, yScale = 1, 1
        self.cx1, self.cy1 = self.cx1+tx*xScale, self.cy1+ty*yScale
        self.xmin, self.xmax, self.ymin, self.ymax = self.xmin+tx*xScale, self.xmax+tx*yScale, self.ymin+ty*xScale, self.ymax+ty*yScale
        self.transform['translate'] = (tx, ty)

        return self

    def simpleEllipse(self):
        """After three transformations: SRT, we can create a new ellipse object from what has been done
           Only rotate operation needs to be kept, the other two operations can be integrated into parameter change
        """
        clearUpEllipse = Ellipse(self.cx1, self.cy1, self.rx1, self.ry1, 
                                {'rotate': self.transform['rotate']}, 
                                [self.xmin, self.ymin, self.xmax, self.ymax])
        return clearUpEllipse

    def svg() -> object:
        pass
        # return svg

    def coco() -> object:
        pass
        # return cocoXml



if __name__ == '__main__':
    e1 = Ellipse(cx=0, cy=0, rx=10, ry=5)
    e1.scale(2)
    e1.rotate(30)
    e1.translate(1,2)