import numpy as np
import helper

class Circle:
    def __init__(self, cx, cy, r, 
                 transform={}, # default to a standardized ellipse, this is for simpleEllipse method only
                 circleLimits=None # default to none, this is for simpleEllipse method only
                #, opacity=1, 
                # fill: "#000000",
                # stroke="none",
                # strokeWidth = 0,
                # strokeLinejoin = round,
                # strokeDasharray = none,
                # strokeOpacity = 1 
                ) -> None:
                self.cx = cx # to record the original shape parameters
                self.cy = cy
                self.r = r
                self.cx1 = self.cx # for intermediate calculations
                self.cy1 = self.cy
                self.r1 = self.r
                if circleLimits == None:
                    self.xmin = cx - r
                    self.ymin = cy - r
                    self.xmax = cx + r
                    self.ymax = cy + r
                else:
                    self.xmin, self.ymin, self.xmax, self.ymax = circleLimits
                self.transform = transform # keep track of transformations
                # self.opacity=1, # probably fix the input below, or just open a few
                # self.fill= "#000000"
                # self.stroke="none"
                # self.strokeWidth = 0
                # self.strokeLinejoin = "round"
                # self.strokeDasharray = "none"
                # self.strokeOpacity = 1
    
    def scale(self, sx:float) -> list:
        # scale, keeping track of the real parameters and bbox coords
        # circle can't have different sx and sy, otherwise we will get a ellipse
        sy = sx
        self.cx1 = sx * self.cx1
        self.cy1 = sy * self.cy1
        self.r1 = np.abs(sx * self.r1)
        self.transform['scale'] = (sx, sy)
        
        self.xmin = self.cx1 - self.r1
        self.ymin = self.cy1 - self.r1
        self.xmax = self.cx1 + self.r1
        self.ymax = self.cy1 + self.r1

        return self


    def rotate(self, degree):
        """keep track of true parameters after rotation, only rotate against central point

        Args:
            coord (_type_): initial coords
            origin (_type_): rotate against
            degree (_type_): clockwise degree to accomodate Inkscape
        """
        pass
        # FOR CONSISTENCY CONSIDERATION, MAY NOT NEED THIS, BECAUSE IT ROTATES AGAINST (0,0)
        # self.transform['rotate'] = degree

        # # -1 to match with clockwise rotation in Inkscape
        # self.cx1, self.cy1, radians = helper.rotate([self.cx1, self.cy1], [0,0], (-1)*degree)
        
        # self.xmin, self.xmax = self.cx1-self.r1, self.cx1+self.r1
        # self.ymin, self.ymax = self.cy1-self.r1, self.cy1+self.r1

        # return self
    
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
        clearUpEllipse = Circle(self.cx1, self.cy1, self.r1, 
                                {'rotate': self.transform['rotate']}, 
                                [self.xmin, self.ymin, self.xmax, self.ymax])
        return clearUpEllipse

    @property
    def xmlValues(self):
         return repr({"cx": self.cx, "cy": self.cy, 'r':self.r, "transform": self.transform})
    
    @property
    def shapeParams(self):
         return repr({"x": self.cx, "y": self.cy1, "r": self.r1})