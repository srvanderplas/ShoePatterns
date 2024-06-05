import synthesis
import helper
import svgwrite

# # Create a new SVG drawing
# dwg = svgwrite.Drawing('output.svg', size=(1500, 1000), viewBox="0 0 1500 1000")


# recObj =  rectangle.Rectangle(400, 300, 200, 100)
# recObj.scale(0.3).rotate(30).translate(100, 200)

# # Add a rectangle to the SVG drawing
# # dwg.add(dwg.rect(insert=(rec.x,rec.y),
# #                  size=(rec.width, rec.height),
# #                  transform=",".join([str(k)+ str(rec.transform[k]) for k in rec.transform.keys()]),
# #                  fill="red"))
# r3 = dwg.rect(insert=(recObj.x,recObj.y),
#                        size=(recObj.width, recObj.height),
#                        transform=helper.svgTransformStr(recObj.transform))
# d = {"fill": "pink",
#      "stroke": "black",}
# for k in d.keys():
#     r3[k] = d[k]
# dwg.add(r3)

# t = triangle.Triangle(100, 10, 150, 190, 50, 190)
# t.scale(2).rotate(30).translate(100, 200)
# r4 = dwg.polygon(points=[(t.ax, t.ay), (t.bx, t.by), (t.cx, t.cy)],
#                  transform='scale(2),rotate(30, 100.0, 106),translate(100, 200)')
# for k in d.keys():
#     r4[k] = d[k]
# dwg.add(r4)
# # t1 = dwg.polygon(points=[(t.ax1, t.ay1), (t.bx1, t.by1), (t.cx1, t.cy1)],transform='scale(2),rotate(30, 100.0, 106),translate(100, 200)')

# t.transform

# e = ellipse.Ellipse(cx=0, cy=0, rx=10, ry=5)
# e.scale(2).rotate(30).translate(1, 2)
# ell = dwg.ellipse(center=(e.cx, e.cy),
#                        r=(e.rx, e.ry),
#                        transform="scale(2, 2),rotate(30, 2, 4),translate(1, 2)")
# for k in d.keys():
#     ell[k] = d[k]
# dwg.add(ell)




# Save the SVG drawing to a file
# dwg.saveas("output6.svg")

# ",".join([str(k)+ str(rec.transform[k]) for k in rec.transform.keys()])

class svgXML():
    def __init__(self, width=1500, height=1000, name="output.svg") -> None:
        """create an empty svg specifying width and hight
        viewbox="0 0 width height"
        no elements"""
        self.svg = svgwrite.Drawing(name, size=(width, height))
        self.width = width
        self.height = height
        self.name = name

    def addRect(self, recObj, dictRec=None):
        """add a Rectangle object to the svg"""
        rec = self.svg.rect(insert=(recObj.x,recObj.y),
                       size=(recObj.width, recObj.height),
                       transform=helper.svgwriteTransformStr(recObj.transform))
        if dictRec is not None:
            for k in dictRec.keys():
                rec[k] = dictRec[k]
        self.svg.add(rec)

    def addTriangle(self, triObj, dictTri=None):
        """add a Triangle object to the svg"""
        tri = self.svg.polygon(points=[(triObj.ax, triObj.ay), (triObj.bx, triObj.by), (triObj.cx, triObj.cy)],
                       transform=helper.svgwriteTransformStr(triObj.transform))
        if dictTri is not None:
            for k in dictTri.keys():
                tri[k] = dictTri[k]
        self.svg.add(tri)

    def addEllipse(self, ellObj, dictEll=None):
        """add a Ellipse object to the svg
        
        Args:
            ellObj (Ellipse ): An Ellipse object from ellipse.py
            dictEll (dict, optional): A dictionary of element features, like fill, color, opacity... . Defaults to None.
        """
        ell = self.svg.ellipse(center=(ellObj.cx, ellObj.cy),
                       r=(ellObj.rx, ellObj.ry),
                       transform=helper.svgwriteTransformStr(ellObj.transform))
        if dictEll is not None:
            for k in dictEll.keys():
                ell[k] = dictEll[k]
        self.svg.add(ell)

    def addCirle(self, circObj, dictCirc=None):
        circ = self.svg.circle(center=(circObj.cx, circObj.cy),
                               r=circObj.r,
                               transform=helper.svgwriteTransformStr(circObj.transform))
        if dictCirc is not None:
            for k in dictCirc.keys():
                circ[k] = dictCirc[k]
        self.svg.add(circ)
    
    
if __name__=="__main__":
    svg = svgXML(1500, 1000)

    recObj =  synthesis.Rectangle(400, 300, 200, 100)
    recObj.srt(scale=[0.3, 0.3], rotate=[30], translate=[100, 200])
    svg.addRect(recObj, {"fill": "pink", "stroke": "black"})
    
    t = synthesis.Triangle(100, 10, 150, 190, 50, 190)
    t.srt(scale=[2, 2], rotate=[30], translate=[100, 200])
    svg.addTriangle(t, {"fill": "pink", "stroke": "red"})

    e = synthesis.Ellipse(cx=0, cy=0, rx=10, ry=5)
    e.srt(scale=[2, 2], rotate=[30], translate=[1, 2])
    svg.addEllipse(e, {"fill": "green", "stroke": "black", "opacity": 0.5})

    svg.svg.saveas("output8.svg")



# 'cx': 300, 'cy': 400, 'rx': 100, 'ry': 50
# a = 200
# b = 100
# theta=np.deg2rad(-30)

# import numpy as np
# xr = np.sqrt((a**2)*(np.cos(theta)**2) + (b**2)*(np.sin(theta)**2))
# yr = ((b**2-a**2)*(np.sin(2*theta)))/(2* np.sqrt((a**2)*(np.cos(theta)**2) + (b**2)*(np.sin(theta)**2)))

# xl = (-1)*np.sqrt((a**2)*(np.cos(theta)**2) + (b**2)*(np.sin(theta)**2))
# yl = (-1)*(b**2-a**2)*(np.sin(2*theta))/(2* np.sqrt((a**2)*(np.cos(theta)**2) + (b**2)*(np.sin(theta)**2)))

# xt = (b**2-a**2)*(np.sin(2*theta))/(2* np.sqrt((a**2)*(np.sin(theta)**2) + (b**2)*(np.cos(theta)**2)))
# yt = np.sqrt((a**2)*(np.sin(theta)**2) + (b**2)*(np.cos(theta)**2))

# xb = (-1)*(b**2-a**2)*(np.sin(2*theta))/(2* np.sqrt((a**2)*(np.sin(theta)**2) + (b**2)*(np.cos(theta)**2)))
# yb = (-1)*np.sqrt((a**2)*(np.sin(theta)**2) + (b**2)*(np.cos(theta)**2))

# [xr,xl,xt,xb]
# [yr,yl,yt,yb]