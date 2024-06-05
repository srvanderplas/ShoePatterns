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
    """This function rotates (px,py) CLOCKWISE around (ox, oy) by d degrees (NOT RADIANS!!!)
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
    return xNew, yNew, radians

def circumcircle(ax, ay, bx, by, cx, cy):
    """Find the circumcenter of a triangle with three points
    Args:
        ax (float): x coordinate of point A
        ay (float): y coordinate of point A
        bx (float): x coordinate of point B
        by (float): y coordinate of point B
        cx (float): x coordinate of point C
        cy (float): y coordinate of point C

    Returns:
        tuple: (x, y, r) of the circumcenter and circumradius
    """
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
    r = np.sqrt((ax - ux)**2 + (ay - uy)**2)
    return ux, uy, r


def svgTransformStr(d):
    """Convert a dictionary to a string for SVG transform attribute
    Args:
        d (dict): dictionary of transformations

    Returns:
        str: string of the SVG transform attribute
    """
    s = "".join([str(k)+ str(d[k]) for k in d.keys()])
    s = s.replace("[", "(")
    s = s.replace("]", ")")
    return s

def svgwriteTransformStr(d):
    """Convert a dictionary to a string for SVG transform attribute
    Args:
        d (dict): dictionary of transformations

    Returns:
        str: string of the SVG transform attribute
    """
    s = ",".join([str(k)+ str(d[k]) for k in d.keys()])
    s = s.replace("[", "(")
    s = s.replace("]", ")")
    return s


def rotateEllipseBbox(a, b, degree):
    theta = (-1)*np.deg2rad(degree) # -1 to match with clockwise rotation in Inkscape
    
    xr = np.sqrt((a**2)*(np.cos(theta)**2) + (b**2)*(np.sin(theta)**2))
    yr = ((b**2-a**2)*(np.sin(2*theta)))/(2* np.sqrt((a**2)*(np.cos(theta)**2) + (b**2)*(np.sin(theta)**2)))

    xl = (-1)*np.sqrt((a**2)*(np.cos(theta)**2) + (b**2)*(np.sin(theta)**2))
    yl = (-1)*(b**2-a**2)*(np.sin(2*theta))/(2* np.sqrt((a**2)*(np.cos(theta)**2) + (b**2)*(np.sin(theta)**2)))

    xt = (b**2-a**2)*(np.sin(2*theta))/(2* np.sqrt((a**2)*(np.sin(theta)**2) + (b**2)*(np.cos(theta)**2)))
    yt = np.sqrt((a**2)*(np.sin(theta)**2) + (b**2)*(np.cos(theta)**2))

    xb = (-1)*(b**2-a**2)*(np.sin(2*theta))/(2* np.sqrt((a**2)*(np.sin(theta)**2) + (b**2)*(np.cos(theta)**2)))
    yb = (-1)*np.sqrt((a**2)*(np.sin(theta)**2) + (b**2)*(np.cos(theta)**2))

    xmin0 = min(xr, xl, xt, xb)
    ymin0 = min(yr, yl, yt, yb)
    width = np.abs(xmin0)*2
    height = np.abs(ymin0)*2
    
    return xmin0, ymin0, width, height

# import matplotlib.pyplot as plt
# from matplotlib.image import imread
# from PIL import Image

# # Read the SVG file
# svg_file = "C:\Users\HUA\Desktop\drawing.svg"


# from PIL import Image

# # Display the PNG image
# img = Image.open(png_file)
# img.show()

# # Display the SVG image
# img = imread("C:\\Users\\HUA\\Desktop\\drawing30.svg")
# plt.imshow(img)
# plt.axis('off')  # Turn off axis
# plt.show()

if __name__ == "__main__":
    # print(rotate([1,0], [0,0], degrees=180 ))
    pass