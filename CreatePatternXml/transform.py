# https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform

def matrix(coord:list, m:list) -> list:
    """ SVG tranform attribute
    Transforming (x,y) using a matrix
       [a c e]
    m= [b d f] 
       [0 0 1]
    (xNew yNew 1)' = m %*% (xPrev yPrev 1)'
    xNew = a*xPrev + c*yPrev + e
    yNew = b*xPrev + d*yPrev + f

    Args:
        coord (list): [x, y], both are float
        m (list): [a, b, c, d, e, f], both are float

    Returns:
        list:[xNew, yNew]
    """
    x,y = coord[0], coord[1]
    a,b,c,d,e,f = m[0], m[1], m[2], m[3], m[4], m[5]

    xNew = a*x + c*y + e
    yNew = b*x + d*y + f
    
    return [xNew, yNew]

def translate(coord:list, v:list) -> list:
    """translate
    xNew = x + a
    yNew = x + b

    Args:
        coord (list): [x, y], both are float
        v (list): [a, b], both are float

    Returns:
        list: [xNew, yNew]
    """
    x, y = coord[0], coord[1]
    a, b = v[0], v[1]
    xNew = x + a
    yNew = y + b
    
    return [xNew, yNew]

def scale(coord:list, s:list) -> list:
    """Scale a transform
    I DONT QUITE GET HOW IT WORKS AS COORD

    Args:
        coord (list): _description_
        s (list): _description_
    """


def rotation(coord:list, r:list)-> list: 
    """rotate the shape by angle a at point (rx, ry)

    Args:
        coord (list): [x, y]
        r (list): [a, rx, ry]

     Returns:
        list: [xNew, yNew]
    """
    
