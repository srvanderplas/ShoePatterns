import random
import drawsvg as draw
import draw2Ele

import random
import svgelements as element
import drawsvg as draw
import ele2draw
import draw2Ele
# pip install -U ipykernel

# import 
def colorGen():
    '''randomly generate a hexcode of color'''
    return '#{:06x}'.format(random.randint(0, 0xFFFFFF))

def opacityGen(start=0, end=1):
    return round(random.uniform(start, end), 1)
# if __name__ == "main":
#     colorGen()
def coordGen(width, height, initx=0, inity=0):
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
    
def rotationGen():
    deg = round(random.uniform(0, 360), 1)
    rotation = random.choice(['rotation({})'.format(deg), "none"])
    return rotation

def parallelogramParamsGen(width, height):
    Mx, My = coordGen(width, height)
    Hx1 = round(random.uniform(Mx, width), 1)
    
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

def createSimpleRect(rectID='rect', width=400, height=300):
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
                                0, 0)

    # The largest stroke width can be 1/10 of the rectangle short edge
    strokeWidth = opacityGen(0,min(recWidth, recHeight)/20)


    # optional stroke dash array
    # num-pixel dash, num-pixel gap
    strokeDashArray = random.choice(['none', strokeDashArrayGen()])

    # Optional round cornors
    # 
    isRoundCornor = random.choice([0,1])
    if isRoundCornor == 0:
        rx, ry = "none", "none"
    else:
        rx, ry = roundCornorGen(recWidth, recHeight)
    
    # generate rotation 
    transform = rotationGen()
        
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
    strokeWidth = opacityGen(0, min(abs(Hx1-Mx), abs(Ly-My))/20)

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
    strokeWidth = opacityGen(0, min(abs(Hx1-Mx), abs(Ly-My))/20)

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

if __name__ == "main":

    width, height = 500, 250
    d = draw.Drawing(width, height, origin=(0,0))
    bg = draw.Rectangle(0,0, width, height, 
                     fill="white",
                    opacity=0.1)
    d.append(bg)
    
    rect = createSimpleRect("rect1")
    d.append(rect)

    d
    # print(len(d.all_elements()))