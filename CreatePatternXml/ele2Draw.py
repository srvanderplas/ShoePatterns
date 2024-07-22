import svgelements as element
import drawsvg as draw
# element object
def eleObjType(ele):
    import svgelements
    """object from element, always in a group"""
    if isinstance(ele, svgelements.Group):
        if len(ele)>1:
                return "Group"
        else:
            ele = ele[0]
            if isinstance(ele, svgelements.Path):
                return "Path"
            if isinstance(ele, svgelements.Circle):
                return "Circle"
            if isinstance(ele, svgelements.Rect):
                return "Rect"
    else:
        if isinstance(ele, svgelements.Path):
            return "Path"
        if isinstance(ele, svgelements.Circle):
            return "Circle"
        if isinstance(ele, svgelements.Rect):
            return "Rect"

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

# element to draw
# ele为单个元素
def eleone2draw(ele):
    import svgelements as element
    import drawsvg as draw
    eleType = eleObjType(ele)
    if eleType == "Circle":
        pass #等circle的时候再写
    if eleType == "Path":
        drawPath = draw.Path(stroke = ele.stroke if hasattr(ele, "stroke") else "black",
                            stroke_width = ele.stroke_width if hasattr(ele, "stroke_width") else 1,
                            fill = ele.fill if hasattr(ele, "fill") else "none",
                            fill_opacity = ele.fill_opacity if hasattr(ele, "fill_opacity") else 1,
                            id = ele.id if hasattr(ele, "id") else "path",
                            transform = ele.transform if hasattr(ele, "transform") else element.Matrix(1,0,0,1,0,0))
                            
        
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
                drawPath.C(elePath.x1, elePath.y1, elePath.x2, elePath.y2, elePath.x, elePath.y)
            if elePType == "QuadraticBezier":
                drawPath.Q(elePath.x1, elePath.y1, elePath.x, elePath.y)
        return drawPath
    if eleType == "Rect":
        drawRect = draw.Rectangle(ele.x, ele.y, ele.width, ele.height, 
                                fill=ele.fill if hasattr(ele, "fill") else "none",
                                stroke=ele.stroke if hasattr(ele, "stroke") else "black",
                                stroke_width=ele.stroke_width if hasattr(ele, "stroke_width") else 1,
                                id = ele.id if hasattr(ele, "id") else "rect",
                                transform = ele.transform if hasattr(ele, "transform") else element.Matrix(1,0,0,1,0,0))
            
        return drawRect



def ele2draw(eles):
    eleType = eleObjType(eles) #多元素，group
    if eleType == "Group":
        drawGroup = draw.Group(id = eles.id if hasattr(eles, "id") else "group",
                               transform = eles.transform if hasattr(eles, "transform") else element.Matrix(1,0,0,1,0,0))
                               
        for ele in eles:
            drawEle = eleone2draw(ele)
            drawGroup.append(drawEle)
        return drawGroup
    else:
        ele = eles[0]
        return eleone2draw(ele)