import svgelements as elements
import drawsvg as draw
import math
import numpy as np

def eleObjType(ele):
    import svgelements
    if isinstance(ele, svgelements.Group):
        return "Group"
    if isinstance(ele, svgelements.Path):
        return "Path"
    if isinstance(ele, svgelements.Circle):
        return "Circle"
    if isinstance(ele, svgelements.Rect):
        return "Rect"
    if isinstance(ele, svgelements.Ellipse):
        return "Ellipse"

def elePathType(elePath):
    import svgelements as svgelement
    if isinstance(elePath, svgelement.svgelements.Move):
        return "Move"
    if isinstance(elePath, svgelement.svgelements.Line):
        return "Line"
    if isinstance(elePath, svgelement.svgelements.CubicBezier):
        return "CubicBezier"
    if isinstance(elePath, svgelement.svgelements.QuadraticBezier):
        return "QuadraticBezier"
    if isinstance(elePath, svgelement.svgelements.Close):
        return "Close"
    if isinstance(elePath, svgelement.svgelements.Arc):
        return "Arc"

def arc_rotation(EleArc):
    """For arc objext only, calculate the rotation angle of the arc"""
    if elePathType(EleArc) == "Arc": # if isinstance(arc[1], svgelements.svgelements.Arc):
        v = EleArc.center - EleArc.start
        return math.degrees(math.atan2(v.x, v.y))
    else:
        raise Exception("Not an svgelements Arc object in path") 
    
# element to draw
# ele为单个元素
def eleone2Draw(ele):
    eleType = eleObjType(ele)
    if eleType == "Circle":
        drawCircle =draw.Circle(ele.cx, ele.cy, ele.implicit_r,
                        fill=ele.fill if hasattr(ele, "fill") else "none",
                        stroke=ele.stroke if hasattr(ele, "stroke") else "black",
                        stroke_width=ele.stroke_width if hasattr(ele, "stroke_width") else 1,
                        id = ele.id if hasattr(ele, "id") else "circle",
                        transform = ele.transform if hasattr(ele, "transform") else elements.Matrix(1, 0, 0, 1, 0, 0),
                        stroke_dasharray = ele.values["stroke-dasharray"] if "stroke-dasharray" in ele.values.keys() else "none",
                        stoke_opacity = ele.values["stroke-opacity"] if "stroke-dasharray" in ele.values.keys() else "none")
        return drawCircle
    if eleType == "Ellipse":
        drawEllipse = draw.Ellipse(ele.cx, ele.cy, ele.rx, ele.ry,
                         fill=ele.fill if hasattr(ele, "fill") else "none",
                        stroke=ele.stroke if hasattr(ele, "stroke") else "black",
                        stroke_width=ele.stroke_width if hasattr(ele, "stroke_width") else 1,
                        id = ele.id if hasattr(ele, "id") else "ellipse",
                        transform = ele.transform if hasattr(ele, "transform") else elements.Matrix(1, 0, 0, 1, 0, 0),
                        stroke_dasharray = ele.values["stroke-dasharray"] if "stroke-dasharray" in ele.values.keys() else "none",
                        stoke_opacity = ele.values["stroke-opacity"] if "stroke-dasharray" in ele.values.keys() else "none")
        return drawEllipse
    if eleType == "Path":
        drawPath = draw.Path(stroke = ele.stroke if hasattr(ele, "stroke") else "black",
                            stroke_width = ele.stroke_width if hasattr(ele, "stroke_width") else 1,
                            fill = ele.fill if hasattr(ele, "fill") else "none",
                            fill_opacity = ele.fill_opacity if hasattr(ele, "fill_opacity") else 1,
                            id = ele.id if hasattr(ele, "id") else "path",
                            transform = ele.transform if hasattr(ele, "transform") else elements.Matrix(1, 0, 0, 1, 0, 0),
                            stroke_dasharray = ele.values["stroke-dasharray"] if "stroke-dasharray" in ele.values.keys() else "none",
                            stoke_opacity = ele.values["stroke-opacity"] if "stroke-dasharray" in ele.values.keys() else "none"
                            )
        for elePath in ele:
            elePType = elePathType(elePath)
            if elePType == "Move":
                m = elePath.d().split()[1].split(',')
                drawPath.M(m[0], m[1])
#                 drawPath.M(elePath.x, elePath.y)
            if elePType == "Line":
                l = elePath.d().split()[1].split(',')
                drawPath.L(l[0], l[1])
#                 drawPath.L(elePath.x, elePath.y)
            if elePType == "Close":
                drawPath.Z()
            if elePType == "CubicBezier":
                drawPath.C(elePath.control1.x, elePath.control1.y, elePath.control2.x, elePath.control2.y, elePath.end.x, elePath.end.y)
            if elePType == "QuadraticBezier":
                drawPath.Q(elePath.control1.x, elePath.control1.y, elePath.end.x, elePath.end.y)
            if elePType == "Arc": # for ellipse ONLY, otherwise, need work on large_arc, sweep flags
                drawPath.A(rx=elePath.rx, 
                    ry=elePath.ry,
                    large_arc = 0,
                    rot = elePath.get_rotation()*360/np.pi/2, 
                    sweep = 1, 
                    ex = elePath.end.x, 
                    ey = elePath.end.y)
        return drawPath
    
    if eleType == "Rect":
        drawRect = draw.Rectangle(ele.x, ele.y, ele.width, ele.height, 
                        fill=ele.fill if hasattr(ele, "fill") else "none",
                        stroke=ele.stroke if hasattr(ele, "stroke") else "black",
                        stroke_width=ele.stroke_width if hasattr(ele, "stroke_width") else 1,
                        id = ele.id if hasattr(ele, "id") else "rect",
                        transform = ele.transform if hasattr(ele, "transform") else elements.Matrix(1, 0, 0, 1, 0, 0),
                        stroke_dasharray = ele.values["stroke-dasharray"] if "stroke-dasharray" in ele.values.keys() else "none",
                        stoke_opacity = ele.values["stroke-opacity"] if "stroke-dasharray" in ele.values.keys() else "none"
            )
        return drawRect



def ele2Draw(eles):
    eleType = eleObjType(eles) #多元素，group
    if eleType == "Group":
        drawGroup = draw.Group(id = eles.id if hasattr(eles, "id") else "group",
                               transform = eles.transform if hasattr(eles, "transform") else elements.Matrix(1, 0, 0, 1, 0, 0)
                               )
        for ele in eles:
            drawEle = ele2Draw(ele)
            drawGroup.append(drawEle)
        return drawGroup
    else:
        return eleone2Draw(eles)
    
if __name__ == "__main__":
    import svgelements as svgelements
    import drawsvg as draw
    # read the SVG file
    svg = svgelements.SVG.parse("rec.svg")

    d00 = draw.Drawing(1500, 1500)
    ele0 = [i for i in svg.elements()][0]
    for i in range(len(ele0)):
        if i==0:
            pass
        d00.append(ele2Draw(ele0[i]))
    # d00.save_png("")
    # d00.rasterize()
    # d00.save_png("demo.png")
    d00
    
    