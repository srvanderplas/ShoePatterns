import svgelements 
import helper

# s = SVG()
# # s1 = SVG()
# # s2 = s1.parse("output6.svg")
# s.width = 1500
# s.height = 1000
# s.viewbox = Viewbox(0, 0, 1500, 1000)

class Ellipse:
    def __init__(self, cx, cy, rx, ry, transform=None, stroke=None, stroke_width=None) -> None:
        self.cx = cx
        self.cy = cy
        self.rx = rx
        self.ry = ry
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.transform = transform if transform is not None else {}
        self.svgelement = svgelements.Ellipse(self.cx, self.cy, self.rx, self.ry, stroke=stroke, stroke_width=stroke_width)
    
    # We require the transformation follows Scale, Rotate, Translate order
    def srt(self, scale=None, rotate=None, translate=None):
        """_summary_

        Args:
            sscale (list): _description_
            rotate (list): _description_
            translate (list): _description_

        Returns:
            _type_: _description_
        """
        if scale is not None:
           self.transform['scale'] = scale if len(scale)>1 else [scale[0], scale[0]]
        if rotate is not None:
            self.transform['rotate'] = rotate    
        if translate is not None:
            self.transform['translate'] = translate

        self.svgelement = self.svgelement * helper.svgTransformStr(self.transform)
    
    @property
    def bbox(self):
        bbox = list(self.svgelement.bbox())
        return bbox
    @property
    def boxparam(self):
        bbox = self.bbox
        return bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]
    @property
    def params(self):
        return {"cx,cy,rx,ry":(self.cx, self.cy, self.rx, self.ry),
                "transform": helper.svgTransformStr(self.transform),
                "svg rec": (self.boxparam)}
    
    def simpleEllise(self):
        bbox = self.svgelement.bbox()
        simpE = Ellipse((bbox[0]+bbox[2])/2, (bbox[1]+bbox[3])/2, 
                        self.rx*self.transform['scale'][0], self.ry*self.transform['scale'][1], 
                        transform="rotate({},{},{})".format(self.transform['rotate'][0],
                                                           (bbox[0]+bbox[2])/2, 
                                                           (bbox[1]+bbox[3])/2))
        return simpE
    
    def svgelement(self):
        """In case we need to access the svgelement directly

        Returns:
            _type_: An SvgElement object
        """
        return self.svgelement
    
    def matrixTransformXML(self):
        return self.svgelement.string_xml()
    
    @property
    def affineMAtrix(self):
        return self.svgelement.transform
    

class Rectangle:
    def __init__(self, x, y, width, height, transform=None, stroke=None, stroke_width=None) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.transform = transform if transform is not None else {}
        self.svgelement = svgelements.Rect(x, y, width, height, stroke=stroke, stroke_width=stroke_width)

    def srt(self, scale=None, rotate=None, translate=None):
        if scale is not None:
           self.transform['scale'] = scale if len(scale)>1 else [scale[0], scale[0]]
        if rotate is not None:
            self.transform['rotate'] = rotate    
        if translate is not None:
            self.transform['translate'] = translate

        self.svgelement = self.svgelement * helper.svgTransformStr(self.transform)
    
    @property
    def bbox(self):
        bbox = list(self.svgelement.bbox())
        return bbox
    
    @property
    def boxparam(self):
        bbox = self.bbox
        return bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]
    
    @property
    def params(self):
        return {"x,y,width,height":(self.x, self.y, self.width, self.height),
                "transform": self.transform,
                "svg rec": (self.boxparam)}
    
    def simpleRect(self):
        if "scale" in self.transform.keys():
            if len(set(self.transform['scale']))>1:
                raise ValueError("Only uniform scaling is allowed")
        swidth, sheight = self.width*self.transform['scale'][0], self.height*self.transform['scale'][1]
        bbox = self.svgelement.bbox()
        centerx, centery = (bbox[0]+bbox[2])/2, (bbox[1]+bbox[3])/2
        simpR = Rectangle(centerx-swidth/2, centery-sheight/2, swidth, sheight,
                        transform="rotate({},{},{})".format(self.transform['rotate'][0],
                                                           (bbox[0]+bbox[2])/2, 
                                                           (bbox[1]+bbox[3])/2))
        return simpR
    
    def svgelement(self):
        """In case we need to access the svgelement directly

        Returns:
            _type_: An SvgElement object
        """
        return self.svgelement
    
    def matrixTransformXML(self):
        return self.svgelement.string_xml()
    
    @property
    def affineMatrix(self):
        return self.svgelement.transform
    

class Triangle:
    def __init__(self, ax, ay, bx, by, cx, cy, transform=None, stroke=None, stroke_width=None) -> None:
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.cx = cx
        self.cy = cy
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.transform = transform if transform is not None else {}
        self.svgelement = svgelements.Polygon([(ax, ay), (bx, by), (cx, cy)], stroke=stroke, stroke_width=stroke_width)

    def srt(self, scale=None, rotate=None, translate=None):
        if scale is not None:
           self.transform['scale'] = scale if len(scale)>1 else [scale[0], scale[0]]
        if rotate is not None:
            self.transform['rotate'] = rotate    
        if translate is not None:
            self.transform['translate'] = translate

        self.svgelement = self.svgelement * helper.svgTransformStr(self.transform)

    @property
    def bbox(self):
        bbox = list(self.svgelement.bbox())
        return bbox
    
    @property
    def boxparam(self):
        bbox = self.bbox
        return bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]
    
    @property
    def params(self):
        return {"points": [[self.ax, self.ay], [self.bx, self.by], [self.cx, self.cy]],
                "transform": self.transform,
                "svg rec": (self.boxparam)}
    
    def simpleTri(self):
        locStr = self.svgelement.d().split(" ")
        locLst = [locStr[1], locStr[3], locStr[5]]
        locLst = sum([i.split(",") for i in locLst], [])
        locLst = [i for i in map(float, locLst)]
        simpT = Triangle(locLst[0], locLst[1], locLst[2], locLst[3], locLst[4], locLst[5])
        return simpT
    
    def svgelement(self):
        """In case we need to access the svgelement directly

        Returns:
            _type_: An SvgElement object
        """
        return self.svgelement  
    
    def matrixTransformXML(self):
        return self.svgelement.string_xml()
    
    @property
    def affineMatrix(self):
        return self.svgelement.transform
    
class Circle:
    def __init__(self, cx, cy, r, transform=None, stroke=None, stroke_width=None) -> None:
        self.cx = cx
        self.cy = cy
        self.r = r
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.transform = transform if transform is not None else {}
        self.svgelement = svgelements.Circle(cx, cy, r, stroke=stroke, stroke_width=stroke_width)
        
    def srt(self, scale=None, rotate=None, translate=None):
        if scale is not None:
            if set(scale) > 1:
               raise ValueError("Only uniform scaling is allowed, please use Ellipse instead")
            self.transform['scale'] = scale if len(scale)>1 else [scale[0], scale[0]]
        if rotate is not None:
            self.transform['rotate'] = rotate    
        if translate is not None:
            self.transform['translate'] = translate

        self.svgelement = self.svgelement * helper.svgTransformStr(self.transform)

    @property
    def bbox(self):
        bbox = list(self.svgelement.bbox())
        return bbox
    
    @property
    def boxparam(self):
        bbox = self.bbox
        return bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]
    
    @property
    def params(self):
        return {"cx,cy,r":(self.cx, self.cy, self.r),
                "transform": self.transform,
                "svg rec": (self.boxparam)}
    
    def simpleCircle(self):
        bbox = self.svgelement.bbox()
        simpC = Circle((bbox[0]+bbox[2])/2, (bbox[1]+bbox[3])/2, 
                        self.r*self.transform['scale'][0])
        return simpC
    
    def svgelement(self):
        """In case we need to access the svgelement directly

        Returns:
            _type_: An SvgElement object
        """
        return self.svgelement
    
    def matrixTransformXML(self):
        return self.svgelement.string_xml()
    
    @property
    def affineMatrix(self):
        return self.svgelement.transform
    




if __name__ == "__main__":
    pass
    e = Ellipse(400, 300, 100, 50)
    print(e.params)
    e.srt(scale=[2], rotate=[30, 400, 300], translate=[40, 30])
    print(e.bbox)
    print(e.transform)
    e.simpleEllise().bbox
    print(e.matrixTransformXML())

    e1 = Ellipse(400, 300, 100, 50)
    e1.srt(scale=[2], translate=[40, 30])
    # print(e1.params)
    # e1.srt(rotate=[30], translate=[40, 30])
    e2 = svgelements.Ellipse(400, 300, 100, 50)
    # e2=e2*"rotate(15)translate(40,30)"
    


    rec = svgelements.Rect(400, 300, 200, 100)
    rec = rec * "scale(0.3)rotate(30, 400, 300)translate(100, 200)"

    rec1 = Rectangle(400, 300, 200, 100)
    rec1.srt(scale=[0.3], rotate=[30, 400, 300], translate=[100, 200])


    t = Triangle(100, 10, 150, 190, 50, 190)
    t.srt(scale=[2], rotate=[30], translate=[100, 200])

