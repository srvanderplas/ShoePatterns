import drawsvg as draw
import svgelements as elements

def drawObjType(draw):
    import drawsvg as draw2    
#     if len(draw)>1:
    if isinstance(draw, draw2.elements.Group):
        return "Group"
    if isinstance(draw, draw2.elements.Rectangle):
        return "Rectangle"
    if isinstance(draw, draw2.elements.Path):
        return "Path"

def drawone2Ele(draw):
#     convert single draw obj to element obj
    drawType = drawObjType(draw)
    if drawType == "Rectangle":
        args = draw.args
        rect = elements.Rect(args['x'], args['y'], args['width'], args['height'],
                             transform = draw.args['transform'] if "transform" in draw.args.keys() else elements.Matrix(1, 0, 0, 1, 0, 0)
#                       fill = args['fill'] if 'fill' in args.keys() else elements.Color("None"),
#                       stroke = args['stroke'] if 'stroke' in args.keys() else elements.Color("#000000"),
#                       stroke_width = args['stroke_width'] if 'stroke_width' in args.keys() else 1,
#                       id = args['id'] if 'id' in args.keys() else "rect"
                     )
        return rect
    if drawType == "Path":
        path = elements.Path() + draw.args['d']
        return path


def draw2Ele(draws):
    dType = drawObjType(draws)
    if dType == "Group":
        g = elements.Group(id=draws.id, 
                       transform = draws.args['transform'] if "transform" in draws.args.keys() else elements.Matrix(1, 0, 0, 1, 0, 0)
#                       can write more attr
                      )
        for drawobj in draws.children:
            g.append(drawone2Ele(drawobj))
        return g
    else:
        return (drawone2Ele(draws))