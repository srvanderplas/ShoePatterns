import random
import svgelements as element
import drawsvg as draw
import ele2Draw
import draw2Ele
import numpy as np
# pip install -U ipykernel

def lineAngles(u, v):
    u = np.array(u)
    v = np.array(v)
    dot_product = np.dot(u, v)
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    cos_theta = dot_product / (norm_u * norm_v)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    angle = np.degrees(np.arccos(cos_theta))
    return angle

def angleL1L2(eleQuad):
    """The angle of first two lines from a quad
    Return in degrees
    """
    L1 = np.array(list(eleQuad[1].start))-np.array(list(eleQuad[1].end))
    L2 = np.array(list(eleQuad[2].end))-np.array(list(eleQuad[2].start))
    theta = lineAngles(L1, L2)
    return theta

def colorGen():
    '''randomly generate a hexcode of color'''
    return '#{:06x}'.format(random.randint(0, 0xFFFFFF))

def opacityGen(start=0.01, end=1):
    return round(random.uniform(start, end), 1)

def coordGen(width, height, initx=1, inity=1):
    '''randomly generate a coordinate value between width and height'''
    x = round(random.uniform(initx, width),1)
    y = round(random.uniform(inity, height),1)
    return x,y

def strokeDashArrayGen():
    num = random.choice([2,3,4]) #decide how many params will generate
    parm1,parm2,parm3,parm4 = random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10)
    if num == 2:
        return str(parm1)+','+str(parm2)
    elif num == 3:
        return str(parm1)+','+str(parm2)+','+str(parm3)
    else:
        return str(parm1)+','+str(parm2)+','+str(parm3)+','+str(parm4)
    
def roundCornorGen(recWidth, recHeight):
    rand = random.choice([0,1])
    
    num = random.choice([1,2])
    if num == 2:
        if rand == 0:
            rx, ry = random.randint(0, int(recWidth/3)),random.randint(0, int(recHeight))
        else:
            rx, ry = random.randint(0, int(recWidth)),random.randint(0, int(recHeight/3))
        return str(rx), str(ry)
    if num == 1:
        r = random.randint(0, int(max(recWidth, recHeight)/3))
        return str(r), str(r)


def rotationGen(start=0, end=360):
    deg = round(random.uniform(start, end), 1)
    rotation = random.choice(['rotate({})'.format(deg), "none"])
    return rotation


def rotationCenterGen(cx, cy, start=0, end=360):
    deg = round(random.uniform(start, end), 1)
    rotation = random.choice([f"rotate({deg}, {cx}, {cy})", "none"])
    return rotation


def parallelogramParamsGen(width, height):
    Mx, My = coordGen(width, height)
#     Hx1 = round(random.uniform(Mx, width), 1)
    Hx1 = round(random.uniform(0.1, width), 1)
    
    Hx2 = -1
    while Hx2>width or Hx2<0:
        Lx, Ly = coordGen(width, height)
        Hx2 = Lx-Hx1+Mx
    return Mx,My,Hx1,Lx,Ly,Hx2

def trapezoidParamsGen(width, height):
    Mx, My = coordGen(width, height)
    Hx1 = round(random.uniform(Mx, width), 1)
    Lx, Ly = coordGen(width, height)
    if Mx<Hx1:
        Hx2 = round(random.uniform(0, Lx), 1)
    else:
        Hx2 = round(random.uniform(Lx, width), 1)
    return Mx,My,Hx1,Lx,Ly,Hx2

def getDrawParallelogramParams(paraDraw):
    M, H1, L, H2 = paraDraw.args['d'].split(" ")[:4]
    Mx, My = [float(i) for i in M[1:].split(",")]
    Hx1 = float(H1[1:])
    Lx, Ly = [float(i) for i in L[1:].split(",")]
    Hx2 = float(H2[1:])
    return Mx,My,Hx1,Lx,Ly,Hx2


def createSimpleRect(rectID='rect', width=400, height=300,
                     randCornor=True,  randStrokeDashArray=True):
    mainColor = random.choice(["green", colorGen()])

    # Selecting stroke color between black and a random color
    strokeColor = random.choice(["black", colorGen(), "none"])

    # Selecting opacity as any number between 0 and 1
    fillOpacity = random.choice([opacityGen(), "1"])
    strokeOpacity = random.choice([opacityGen(), "1"])

    # Selecting left corner coord which is inside the canvas
    coordx, coordy = coordGen(width, height)

    # Selecting rectangle width and height
    # Stroke width is considered to make sure the rectangle is inside the canvas
    # recWidth, recHeight= coordGen(width-strokeWidth-coordx, height-strokeWidth-coordy, 
    #                             0, 0)
    recWidth, recHeight= coordGen(width-coordx, height-coordy, 
                                1, 1)

    # The largest stroke width can be 1/10 of the rectangle short edge
    strokeWidth = opacityGen(0.01,min(recWidth, recHeight)/5)


    # optional stroke dash array
    # num-pixel dash, num-pixel gap
    if randStrokeDashArray == False:
        strokeDashArray = "none"
    else:
        strokeDashArray = random.choice(['none', strokeDashArrayGen()])

    # Optional round cornors
    if randCornor == False:
        rx, ry = "none", "none"
    else: 
        isRoundCornor = random.choice([0,1])
        if isRoundCornor == 0:
            rx, ry = "none", "none"
        else:
            rx, ry = roundCornorGen(recWidth, recHeight)
    
    # generate rotation 
    transform = rotationCenterGen(coordx+recWidth/2, coordy+recHeight/2)
        
    rect = draw.Rectangle(coordx, coordy, recWidth, recHeight,
                    fill = mainColor,
                    fill_opacity = fillOpacity,
                    stroke = strokeColor,
                    stroke_opacity = strokeOpacity,
                    stroke_width = strokeWidth,
                    stroke_dasharray = strokeDashArray,
                    rx = rx,
                    ry = ry,
                    id = rectID,
                    transform = transform)
    boxXmin, boxYmin, boxXmax, boxYmax = draw2Ele.draw2Ele(rect).bbox()
    if boxXmin>0 and boxXmax<width and boxYmin>0 and boxYmax<height:
        return rect
    while boxXmin<0 or boxXmax>width or boxYmin<0 or boxYmax>height:
        createSimpleRect(rectID)


def createParallelogram(paraID="parallelogram", width=400, height=300):
#     fill_opacity and stroke width can't be 0 at the same time
    Mx,My,Hx1,Lx,Ly,Hx2 = parallelogramParamsGen(width, height)
    
    mainColor = random.choice(["green", colorGen()])

    # Selecting stroke color between black and a random color
    strokeColor = random.choice(["black", colorGen(), "none"])

    # Selecting opacity as any number between 0 and 1
    fillOpacity = random.choice([opacityGen(), "1"])
    strokeOpacity = random.choice([opacityGen(), "1"])

    # The largest stroke width can be 1/10 of the rectangle short edge
    strokeWidth = opacityGen(0.01, min(abs(Hx1-Mx), abs(Ly-My))/20)

    # optional stroke dash array
    # num-pixel dash, num-pixel gap
    strokeDashArray = random.choice(['none', strokeDashArrayGen()])
    
    # generate rotation 
    transform = rotationGen()
    
    para = draw.Path(stroke=strokeColor,
                     fill=mainColor,
                     fill_opacity = fillOpacity,
                     stroke_width = strokeWidth,
                     stroke_opacity = strokeOpacity,
                     stroke_dasharray = strokeDashArray,
                     transform = transform).M(Mx, My).H(Hx1).L(Lx, Ly).H(Hx2).Z()
    
    boxXmin, boxYmin, boxXmax, boxYmax = draw2Ele.draw2Ele(para).bbox()
    if boxXmin>0 and boxXmax<width and boxYmin>0 and boxYmax<height:
        return para
    while boxXmin<0 or boxXmax>width or boxYmin<0 or boxYmax>height:
        createParallelogram(paraID)
        
        

def createTrapezoid(trapeID="parallelogram", width=400, height=300):
    Mx,My,Hx1,Lx,Ly,Hx2 = trapezoidParamsGen(width=width, height=height)
    
    mainColor = random.choice(["green", colorGen()])

    # Selecting stroke color between black and a random color
    strokeColor = random.choice(["black", colorGen(), "none"])

    # Selecting opacity as any number between 0 and 1
    fillOpacity = random.choice([opacityGen(), "1"])
    strokeOpacity = random.choice([opacityGen(), "1"])

    # The largest stroke width can be 1/10 of the rectangle short edge
    strokeWidth = opacityGen(0.01, min(abs(Hx1-Mx), abs(Ly-My))/20)

    # optional stroke dash array
    # num-pixel dash, num-pixel gap
    strokeDashArray = random.choice(['none', strokeDashArrayGen()])
    
    # generate rotation 
    transform = rotationGen()
    
    trape = draw.Path(stroke=strokeColor,
                     fill=mainColor,
                     fill_opacity = fillOpacity,
                     stroke_width = strokeWidth,
                     stroke_opacity = strokeOpacity,
                     stroke_dasharray = strokeDashArray,
                     transform = transform).M(Mx, My).H(Hx1).L(Lx, Ly).H(Hx2).Z()
    boxXmin, boxYmin, boxXmax, boxYmax = draw2Ele.draw2Ele(trape).bbox()
    if boxXmin>0 and boxXmax<width and boxYmin>0 and boxYmax<height:
#         print("return")
        return trape
    while boxXmin<0 or boxXmax>width or boxYmin<0 or boxYmax>height:
        createTrapezoid(trapeID)
        
        
def createChevronPara(paraDraw):
    Mx,My,Hx1,Lx,Ly,Hx2 = getDrawParallelogramParams(paraDraw)

    # convert Draw to Element
    pEle = draw2Ele.draw2Ele(paraDraw)
    # Flip on x-axis and translate back to the initial M point as a Draw object
    pEleflipTranslate = abs(pEle*"translate({},0) scale(-1,1)".format(2* pEle[1].start[0])) #translate in x only
    # Calculate rotate angle
    if Mx<=Hx1 and Ly>My and Hx2<Mx:
        rotate = 180-2*angleL1L2(pEle)
#         print(1)
    if Mx<Hx1 and Ly>My and Hx2>Mx:
        rotate = 180-2*angleL1L2(pEle)
#         print(2)
    if Mx<Hx1 and Ly<My and Hx2>Mx:
        rotate = 2*angleL1L2(pEle)-180
#         print(3)
    if Mx<Hx1 and Ly<My and Hx2<Mx:
        rotate = 2*angleL1L2(pEle)-180
#         print(4)
    if Mx>Hx1 and Ly>My and Hx2<Mx:
        rotate = 2*angleL1L2(pEle)-180
#         print(5)
    if Mx>Hx1 and Ly>My and Hx2>Mx:
        rotate = 2*angleL1L2(pEle)-180
#         print(6)
    if Mx>Hx1 and Ly<My and Hx2>Mx:
        rotate = 180-2*angleL1L2(pEle)
#         print(7)
    if Mx>Hx1 and Ly<My and Hx2<Mx:
        rotate = 180-2*angleL1L2(pEle)
#         print(8)
    pEle2 = abs(pEleflipTranslate*"rotate({},{},{})".format(rotate, pEle[1].start[0], pEle[1].start[1]))
    para2 = ele2Draw(pEle2)
    
    mainColor = random.choice(["green", colorGen()])
    para2.args['fill'] = mainColor
    strokeColor = random.choice(["black", colorGen(), "none"])
    para2.args['stroke'] = strokeColor
    fillOpacity = random.choice([opacityGen(), "1"])
    para2.args['fill-opacity'] = fillOpacity
    strokeOpacity = random.choice([opacityGen(), "1"])
    para2.args['stroke-opacity'] = strokeOpacity
    strokeWidth = opacityGen(0, min(abs(Hx1-Mx), abs(Ly-My))/20)
    para2.args['stroke-width'] = strokeWidth
    strokeDashArray = random.choice(['none', strokeDashArrayGen()])
    para2.args['stroke-dasharray'] = strokeDashArray

    return para2, pEle2


def createChevron(chevID="chevron", width=400, height=300):
    p = createParallelogram(width=width, height=height)
    p2, pEle2 = createChevronPara(p)
    boxXmin, boxYmin, boxXmax, boxYmax = pEle2.bbox()
    if boxXmin>0 and boxXmax<width and boxYmin>0 and boxYmax<height:
        return p, p2
    while boxXmin<0 or boxXmax>width or boxYmin<0 or boxYmax>height:
        return createChevron(chevID, width, height)
    
    
def createSimpleCircle(circID="circle", width=400, height=300):
    cx,cy = coordGen(width, height, initx=1, inity=1)
    maxr = min(cx, width-cx, cy, height-cy)
    r = opacityGen(start=1, end=maxr)
    mainColor = random.choice(["green", colorGen()])

    # Selecting stroke color between black and a random color
    strokeColor = random.choice(["black", colorGen(), "none"])

    # Selecting opacity as any number between 0 and 1
    fillOpacity = random.choice([opacityGen(), "1"])
    strokeOpacity = random.choice([opacityGen(), "1"])


    # The largest stroke width can be 1/10 of the rectangle short edge
    strokeWidth = opacityGen(0, r/2)


    # optional stroke dash array
    # num-pixel dash, num-pixel gap
    strokeDashArray = random.choice(['none', strokeDashArrayGen()])
    
    circle = draw.Circle(cx, cy, r,
                    fill = mainColor,
                    fill_opacity = fillOpacity,
                    stroke = strokeColor,
                    stroke_opacity = strokeOpacity,
                    stroke_width = strokeWidth,
                    stroke_dasharray = strokeDashArray,
                    id = circID)
#     boxXmin, boxYmin, boxXmax, boxYmax = draw2Ele.draw2Ele(rect).bbox() #not yet ready
#     if boxXmin>0 and boxXmax<width and boxYmin>0 and boxYmax<height:
#         return rect
#     while boxXmin<0 or boxXmax>width or boxYmin<0 or boxYmax>height:
#         createSimpleRect(rectID)
    return circle

def createSimpleEllipse(ellipseID="ellipse", width=400, height=300):
    cx,cy = coordGen(width, height, initx=1, inity=1)
    maxr = min(cx, width-cx, cy, height-cy)
    rx, ry = opacityGen(start=0.011, end=maxr), opacityGen(start=0.01, end=maxr)
    mainColor = random.choice(["green", colorGen()])

    # Selecting stroke color between black and a random color
    strokeColor = random.choice(["black", colorGen(), "none"])

    # Selecting opacity as any number between 0 and 1
    fillOpacity = random.choice([opacityGen(), "1"])
    strokeOpacity = random.choice([opacityGen(), "1"])

    # rotation
    transform = rotationCenterGen(cx, cy)

    # The largest stroke width can be 1/10 of the rectangle short edge
    strokeWidth = opacityGen(0, min(rx, ry)/2)


    # optional stroke dash array
    # num-pixel dash, num-pixel gap
    strokeDashArray = random.choice(['none', strokeDashArrayGen()])

    ellipse = draw.Ellipse(cx, cy, rx, ry,
                    fill = mainColor,
                    fill_opacity = fillOpacity,
                    stroke = strokeColor,
                    stroke_opacity = strokeOpacity,
                    stroke_width = strokeWidth,
                    stroke_dasharray = strokeDashArray,
                    id = ellipseID,
                    transform = transform)
    boxXmin, boxYmin, boxXmax, boxYmax = draw2Ele.draw2Ele(ellipse).bbox() #not yet ready
    if boxXmin>0 and boxXmax<width and boxYmin>0 and boxYmax<height:
        return ellipse
    while boxXmin<0 or boxXmax>width or boxYmin<0 or boxYmax>height:
        createSimpleEllipse(ellipseID, width, height)


def createSimpleTriangle(rectID='triangle', width=400, height=300):
    mainColor = random.choice(["green", colorGen()])

    # Selecting stroke color between black and a random color
    strokeColor = random.choice(["black", colorGen(), "none"])

    # Selecting opacity as any number between 0 and 1
    fillOpacity = random.choice([opacityGen(), "1"])
    strokeOpacity = random.choice([opacityGen(), "1"])

    # optional stroke dash array
    # num-pixel dash, num-pixel gap
    strokeDashArray = random.choice(['none', strokeDashArrayGen()])

    Px1, Py1 = coordGen(width, height)
    Px2, Py2 = coordGen(width, height)
    Px3, Py3 = coordGen(width, height)
    
    # The largest stroke width can be 1/10 of the rectangle short edge
    strokeWidth = opacityGen(0,min(abs(Px1-Px2), abs(Px2-Px3), abs(Px1-Px3),
                                  abs(Py1-Py2), abs(Py2-Py3), abs(Py1-Py3))/20)

    # generate rotation 
    transform = rotationCenterGen((Px1+Px2+Px3)/3, (Py1+Py2+Py3)/3)

    triangle = draw.Lines(Px1, Py1, Px2, Py2, Px3, Py3, 
                          close="true",
                         stroke=strokeColor,
                         fill=mainColor,
                         fill_opacity = fillOpacity,
                         stroke_width = strokeWidth,
                         stroke_opacity = strokeOpacity,
                         stroke_dasharray = strokeDashArray,
                         transform = transform)
    boxXmin, boxYmin, boxXmax, boxYmax = draw2Ele.draw2Ele(triangle).bbox()
    if boxXmin>0 and boxXmax<width and boxYmin>0 and boxYmax<height:
        return triangle
    while boxXmin<0 or boxXmax>width or boxYmin<0 or boxYmax>height:
        createSimpleTriangle(rectID, width, height)
           

if __name__ == "__main__":
    i=0
    ratios = []
    while i <= 1000:
        width, height = 400, 300
        d = draw.Drawing(width, height, origin=(0,0))
        bg = draw.Rectangle(0,0, width, height, 
                          fill="white",
                          opacity=1)
        d.append(bg)
        try:
            rect = createSimpleTriangle("triangle")
            eleRect = draw2Ele.draw2Ele(rect)
            # cmin, cmax = min(eleRect.cx, eleRect.cy), max(eleRect.cx, eleRect.cy)
            d.append(rect)
            d.save_png( f'C:\\Users\\HUA\OneDrive - University of Nebraska-Lincoln\\Inkscape\\deep-learning-for-image-processing\\data_set\\shape_data3\\Triangle\\triangle{i}.png')
            # ratios.append(cmax/cmin)
            eleRect.write_xml(f'C:\\Users\\HUA\OneDrive - University of Nebraska-Lincoln\\Inkscape\\deep-learning-for-image-processing\\data_set\\shape_data3\\TriangleXml\\triangle{i}')
            i += 1
        except RecursionError:
            pass
        except AttributeError:
            pass
        except TypeError:
            pass
    # import pickle
    # with open("ellipseRatio.pkl", "wb") as f:
    #     pickle.dump(ratios, f)
with o