import numpy as np
import helper
import xml.etree.ElementTree as ET

# Because of the wierd transformation system in SVG
# The transmations have to follow rules:
#   1, Follow Affine matrix way: Scaling + Rotation + transltion
#   2, Always do inplace rotation, so only one parameter, theta, is allowed
#   3, Input has to be only (x,y,w,h)
#      Rotated rec NOT ALLOWED. MAYBE IMPLEMENT LATER
#   4, If there are follow up transformations, ONLY ONE scale parameter is allowed, otherwise we will get a parrallelogram.


class Triangle:
    def __init__(self, ax, ay, bx, by, cx, cy, 
                 transform={}, # default to a standardized ellipse, this is for simpleEllipse method only
                 limits=None # default to none, this is for simplify method only
                #, opacity=1, 
                # fill: "#000000",
                # stroke="none",
                # strokeWidth = 0,
                # strokeLinejoin = round,
                # strokeDasharray = none,
                # strokeOpacity = 1 
                ) -> None:
                self.ax = ax 
                self.ay = ay
                self.bx = bx
                self.by = by
                self.cx = cx
                self.cy = cy

                self.ax1 = ax
                self.ay1 = ay
                self.bx1 = bx
                self.by1 = by
                self.cx1 = cx
                self.cy1 = cy

                if limits == None:
                    self.xmin, self.xmax = min(ax, bx, cx), max(ax, bx, cx)
                    self.ymin, self.ymax = min(ay, by, cy), max(ay, by, cy)
                else:
                    self.xmin, self.ymin, self.xmax, self.ymax = limits
                self.transform = transform # keep track of transformations
                self.transform1 = {}
                # self.opacity=1, # probably fix the input below, or just open a few
                # self.fill= "#000000"
                # self.stroke="none"
                # self.strokeWidth = 0
                # self.strokeLinejoin = "round"
                # self.strokeDasharray = "none"
                # self.strokeOpacity = 1
    
    def scale(self, s) -> list:
        """No sy allowed if there are more transformations, otherwise we will end up with an parallelogram.
           
        Args:
            sx (int): _description_
            sy (int, optional): _description_. Defaults to None.
        """
        # scale, keeping track of the real parameters and bbox coords
        self.ax1 = s * self.ax
        self.ay1 = s * self.ay
        self.bx1 = s * self.bx
        self.by1 = s * self.by
        self.cx1 = s * self.cx
        self.cy1 = s * self.cy
        self.transform['scale'] = [s]
        
        self.xmin = self.xmin * s
        self.ymin = self.ymin * s
        self.xmax = self.xmax * s
        self.ymax = self.ymax * s

        return self
    
    def rotate(self, degree):
        """keep track of true parameters after rotation, only rotate against central point of rectangle
           Always starts with a no rotation rectangle, this limitation due to the params don't contain rotation information
           Default to inplace rotation.

        Args:
            coord (_type_): initial coords
            origin (_type_): rotate against
            degree (_type_): clockwise degree to accomodate Inkscape
                             degree input is clockwise rotating the object, but need -degree in helper.rotate
        """
        # Get the center and radius of the circumcircle
        centerx, centery, r = helper.circumcircle(self.ax, self.ay, self.bx, self.by, self.cx, self.cy)
        if "scale" in self.transform.keys():
            self.transform1['rotate'] = degree, centerx*self.transform['scale'][0], centery*self.transform['scale'][0]
            s = self.transform['scale'][0]
        else:
            self.transform1['rotate'] = (degree, centerx, centery)
            s = 1
        self.transform['rotate'] = (degree, centerx, centery)
        self.transform1['rotate'] = (degree, centerx*s, centery*s)
        
        # get updated point coords
        self.ax1, self.ay1 = helper.rotate([self.ax1, self.ay1], self.transform1['rotate'][1:], -1*degree)[:2]
        self.bx1, self.by1 = helper.rotate([self.bx1, self.by1], self.transform1['rotate'][1:], -1*degree)[:2]
        self.cx1, self.cy1 = helper.rotate([self.cx1, self.cy1], self.transform1['rotate'][1:], -1*degree)[:2]
        
        self.xmin, self.xmax = min(self.ax1, self.bx1, self.cx1), max(self.ax1, self.bx1, self.cx1)
        self.ymin, self.ymax = min(self.ay1, self.by1, self.cy1), max(self.ay1, self.by1, self.cy1)

        return self
        
    def translate(self, tx, ty=None):
        if "scale" in self.transform.keys():
            s = self.transform['scale'][0]
        else:
            s = 1
        self.ax1 = self.ax1 + tx*s
        self.ay1 = self.ay1 + ty*s
        self.bx1 = self.bx1 + tx*s
        self.by1 = self.by1 + ty*s
        self.cx1 = self.cx1 + tx*s
        self.cy1 = self.cy1 + ty*s
        
        self.xmin,self.xmax = self.xmin + tx*s, self.xmax + tx*s
        self.ymin,self.ymax = self.ymin + ty*s, self.ymax + ty*s

        self.transform['translate'] = (tx, ty)

        return self

    @property
    def xmlValues(self):
         return repr({"points": [[self.ax1, self.ay1], [self.bx1, self.by1], [self.cx1, self.cy1]],
                      "transform": self.transform,
                      "limits": [self.xmin, self.ymin, self.xmax, self.ymax]})

    @property
    def simpleTri(self):
        """After three transformations: SRT, we can create a new Rectangle object from what has been done
           Only rotate operation needs to be kept, the other two operations can be integrated into parameter change
        """
        clearUpTriangle = Triangle(self.ax1, self.ay1, self.bx1, self.by1, self.cx1, self.cy1,
                                    transform=self.transform1, 
                                    limits=[self.xmin, self.ymin, self.xmax, self.ymax])
        return clearUpTriangle

    def writeSvg(self, xml=None) -> object:
        # Write an cllipse object for later use, can't make a whole xml
        # SHOULD I WRITE A NEW FUNCTION TO DO THIS??

        if xml == None:
            #  Create a new xml file
            pass
        else:
            pass
            #  continue writing with the xml file
        # return svg

    def coco() -> object:
        pass
        # return cocoXml



if __name__ == '__main__':
    t = Triangle(100, 10, 150, 190, 50, 190)
    t.scale(2).rotate(30).translate(100, 200)
    print(t.xmlValues)
    a = t.simpleTri
    print(a.xmlValues)