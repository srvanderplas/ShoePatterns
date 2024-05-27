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


class Rectangle:
    def __init__(self, x, y, width, height, 
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
                self.x = x # upper left x
                self.y = y # upper left y
                self.width = width
                self.height = height
                self.x1 = self.x
                self.y1 = self.y
                self.width1 = self.width
                self.height1 = self.height
                if limits == None:
                    self.xmin = x
                    self.ymin = y
                    self.xmax = x + width
                    self.ymax = y + height
                else:
                    self.xmin, self.ymin, self.xmax, self.ymax = limits
                self.transform = {} # keep track of transformations
                self.transform1 = {}
                # self.opacity=1, # probably fix the input below, or just open a few
                # self.fill= "#000000"
                # self.stroke="none"
                # self.strokeWidth = 0
                # self.strokeLinejoin = "round"
                # self.strokeDasharray = "none"
                # self.strokeOpacity = 1
    
    def scale(self, sx:float, sy = None) -> list:
        """No sy allowed if there are more transformations, otherwise we will end up with an parallelogram.
           
        Args:
            sx (int): _description_
            sy (int, optional): _description_. Defaults to None.
        """
        # scale, keeping track of the real parameters and bbox coords
        if self.transform.keys():
             if sy!= None:
                  raise Exception("No sy allowed because there are other transformations")
        if sy == None:
            sy = sx
        self.x1 = sx * self.x1
        self.y1 = sy * self.y1
        self.width1 = np.abs(sx * self.width1)
        self.height1 = np.abs(sy * self.height1)
        self.transform['scale'] = (sx, sy)
        
        self.xmin = self.x1
        self.ymin = self.y1
        self.xmax = self.x1 + self.width1
        self.ymax = self.y1 + self.height1


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
        centerx, centery = self.x+0.5*self.width, self.y+0.5*self.height
        if "scale" in self.transform.keys():
            self.transform1['rotate'] = degree, centerx*self.transform['scale'][0], centery*self.transform['scale'][0]
        else:
            self.transform1['rotate'] = (degree, centerx, centery)
        self.transform['rotate'] = (degree, centerx, centery)
        
        # upper left point has a new coord pair, to track bbox not update x1, y1, because no point to do so in rec
        centerx, centery = self.transform1['rotate'][1], self.transform1['rotate'][2]
        upperLeftCoordx, upperLeftCoordy = helper.rotate([self.x1, self.y1], [centerx, centery], -1*degree)[:2]
        lowerLeftCoordx, lowerLeftCoordy = helper.rotate([self.x1, self.y1+self.height1], [centerx, centery], -1*degree)[:2]
        upperRightCoordx, upperRightCoordy = helper.rotate([self.x1+self.width1, self.y1], [centerx, centery], -1*degree)[:2]
        lowerRightCoordx, lowerRightCoordy = helper.rotate([self.x1+self.width1, self.y1+self.height1], [centerx, centery], -1*degree)[:2]
        
        self.xmin, self.xmax = min(upperLeftCoordx, lowerLeftCoordx, upperRightCoordx, lowerRightCoordx), max(upperLeftCoordx, lowerLeftCoordx, upperRightCoordx, lowerRightCoordx)
        self.ymin, self.ymax = min(upperLeftCoordy, lowerLeftCoordy, upperRightCoordy, lowerRightCoordy), max(upperLeftCoordy, lowerLeftCoordy, upperRightCoordy, lowerRightCoordy)
        # self.x1, self.y1, radians = helper.rotate([self.x1, self.y1], [], -1*degree)

        # radians = np.deg2rad(degree)
        # centerPoint = [self.cx1, self.cy1]
        # leftPointNew = helper.rotate(leftPoint, centerPoint, degree)
        # rightPointNew = helper.rotate(rightPoint, centerPoint, degree)
        # topPointNew = helper.rotate(topPoint, centerPoint, degree)
        # bottomPointNew = helper.rotate(bottomPoint, centerPoint, degree)

        # xs = [leftPointNew[0], rightPointNew[0], topPointNew[0], bottomPointNew[0]]
        # ys = [leftPointNew[1], rightPointNew[1], topPointNew[1], bottomPointNew[1]]
        # self.xmin, self.xmax, self.ymin, self.ymax = min(xs), max(xs), min(ys), max(ys)
    
    def translate(self, tx, ty=None):

        if "scale" in self.transform.keys():
            xScale, yScale = self.transform['scale']
        else:
            xScale, yScale = 1, 1
        self.x1, self.y1 = self.x1+tx*xScale, self.y1+ty*yScale
        
        
        degree, centerx, centery = self.transform1['rotate'][0], self.transform1['rotate'][1], self.transform1['rotate'][2]
        upperLeftCoordx, upperLeftCoordy = helper.rotate([self.x1, self.y1], [centerx, centery], -1*degree)[:2]
        lowerLeftCoordx, lowerLeftCoordy = helper.rotate([self.x1, self.y1+self.height1], [centerx, centery], -1*degree)[:2]
        upperRightCoordx, upperRightCoordy = helper.rotate([self.x1+self.width1, self.y1], [centerx, centery], -1*degree)[:2]
        lowerRightCoordx, lowerRightCoordy = helper.rotate([self.x1+self.width1, self.y1+self.height1], [centerx, centery], -1*degree)[:2]

        self.xmin, self.xmax = min(upperLeftCoordx, lowerLeftCoordx, upperRightCoordx, lowerRightCoordx), max(upperLeftCoordx, lowerLeftCoordx, upperRightCoordx, lowerRightCoordx)
        self.ymin, self.ymax = min(upperLeftCoordy, lowerLeftCoordy, upperRightCoordy, lowerRightCoordy), max(upperLeftCoordy, lowerLeftCoordy, upperRightCoordy, lowerRightCoordy)

        # self.xmin, self.xmax, self.ymin, self.ymax = self.xmin+tx*xScale, self.xmax+tx*yScale, self.ymin+ty*xScale, self.ymax+ty*yScale
        self.transform['translate'] = (tx, ty)

    
    @property
    def xmlValues(self):
         return repr({"x": self.x, "y": self.y, 'width':self.width, 'height':self.height, "transform": self.transform})
    
    @property
    def shapeParams(self):
         return repr({"x": self.x1, "y": self.y1, 'width':self.width1, 'height':self.height1})

    @property
    def simpleRec(self):
        """After three transformations: SRT, we can create a new Rectangle object from what has been done
           Only rotate operation needs to be kept, the other two operations can be integrated into parameter change
        """
        clearUpEllipse = Rectangle(self.x1, self.y1, self.width1, self.height1, 
                                {'rotate': self.transform['rotate']}, 
                                [self.xmin, self.ymin, self.xmax, self.ymax])
        return clearUpEllipse

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



# if __name__ == '__main__':
    pass
r = Rectangle(400, 300,200,100)
r.scale(0.3)
r.rotate(30)
r.translate(100, 200)
