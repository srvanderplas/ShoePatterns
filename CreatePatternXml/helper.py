import numpy as np

def generateColor(rand=True, print=False):
    '''
    Randomly generating a color hexcode'''
    import random
    r = lambda: random.randint(0,255)
    code = '#%02X%02X%02X' % (r(),r(),r())
    if print==True:
        print(code)
    return code

def rotate(point: list, origin: list, degrees) -> list:
    """This function rotates (px,py) counter-clockwisely against (ox, oy) in d degrees (NOT RADIANS!!!)
       SVG rotation is clockwise, so always go with NEGATIVE here

    (1,0) 

    Args:
        point (list): coordinate [px, py] both are floats
        origin (list): coordinate [ox, oy] both are floats
        degrees (float or int): d rotation degree

    Returns:
       list: coordinate after rotation
    """
    radians = np.deg2rad(degrees)
    cos_rad = np.cos(radians)
    sin_rad = np.sin(radians)

    x,y = point
    xOffset, yOffset = origin
    
    xAdjusted = x - xOffset
    yAdjusted = y - yOffset
    
    xNew = xOffset + cos_rad * xAdjusted + sin_rad * yAdjusted
    yNew = yOffset + -sin_rad * xAdjusted + cos_rad * yAdjusted
    if np.abs(xNew) < 10**(-6):
        xNew = 0
    if np.abs(yNew) < 10**(-6):
        yNew = 0
    return [xNew, yNew]


# if __name__ == "__main__":
#     print(rotate([1,0], [0,0], degrees=180 ))