import sys
sys.path.append('../../')
from sciapp.object import mark2shp, Layer, json2shp
from sciapp.action import PointEditor, LineEditor, PolygonEditor, \
RectangleEditor, EllipseEditor, FreeLineEditor, FreePolygonEditor, BaseEditor
from sciwx.canvas import VCanvas as Canvas
import wx

point = {'type':'point', 'color':(255,0,0), 'lw':1, 'body':(10,10)}
points = {'type':'points', 'color':(255,0,0), 'lw':1, 'body':[(10,10),(100,200)]}
line = {'type':'line', 'color':(255,0,0), 'lw':1, 'lstyle':'-', 'body':[(10,10),(100,200),(200,200)]}
lines = {'type':'lines', 'color':(255,0,0), 'lw':1, 'lstyle':'-o', 'body':[[(10,10),(100,200),(200,200)],[(150,10),(50,250)]]}
polygon = {'type':'polygon', 'color':(255,0,0), 'fcolor':(255,255,0), 'lw':1, 'fill':False, 'lstyle':'o', 'body':[[(10,10),(100,200),(200,200)]]}
polygons = {'type':'polygons', 'color':(255,0,0), 'fcolor':(255,255,0,30), 'fill':True, 'lw':1, 'lstyle':'o', 'body':[[(10,10),(100,200),(200,200)],[(150,10),(50,250),(288,0)]]}
circle = {'type':'circle', 'color':(255,0,0), 'fcolor':(255,255,0), 'fill':False, 'body':(100,100,50)}
circles = {'type':'circles', 'color':(255,0,0), 'fcolor':(255,255,0), 'fill':True, 'lw':2, 'body':[(100,100,50),(300,300,100)]}
ellipse = {'type':'ellipse', 'color':(255,0,0), 'fcolor':(255,255,0), 'fill':False, 'body':(100,100,100,-50,1)}
ellipses = {'type':'ellipses', 'color':(255,0,0), 'fcolor':(255,255,0), 'fill':False, 'body':[(100,100,100,50,1),(200,250,50,100,3.14)]}
rectangle = {'type':'rectangle', 'color':(255,0,0), 'fcolor':(255,255,0), 'fill':True, 'body':(100,100,80,50)}
rectangles = {'type':'rectangles', 'fcolor':(255,255,0), 'fill':False, 'body':[(100,100,80,50),(200,200,80,100)]}
text = {'type':'text', 'color':(255,0,0), 'fcolor':(0,0,0), 'lw':8, 'fill':True, 'body':(100,200,'id=0')}
texts = {'type':'texts', 'color':(255,0,0), 'fcolor':(0,0,0), 'lw':8, 'fill':True, 'body':[(100,200,'id=0'),(180,250,'id=1')]}

layer = {'type':'layer', 'num':-1, 'color':(255,255,0), 'fcolor':(255,255,255), 'fill':False, 
			'body':[point, points, line, lines, polygon, polygons, circle, circles, ellipse, ellipses, rectangle, rectangles, text, texts]}

layers = {'type':'layers', 'num':-1, 'color':(255,255,0), 'fcolor':(255,255,255), 'fill':False, 'body':{2:points, 1:line, 0:layer}}

layer = {'type':'layer', 'num':-1, 'color':(0,0,255), 'fcolor':(255,255,255), 'fill':False, 'body':[ellipses, rectangles, ellipse]}

def mark_test(mark):
    frame = wx.Frame(None, title='gray test')
    canvas = Canvas(frame, autofit=False, up=True)
    canvas.set_shp(mark2shp(mark))
    frame.Show()

if __name__ == '__main__':
    app = wx.App()
    #ShapeEditor(dtype={'layer', 'rectangles'}).start(None)
    FreePolygonEditor().start(None)
    #mark_test(point)
    #mark_test(points)
    #mark_test(line)
    #mark_test(lines)
    #mark_test(polygon)
    #mark_test(polygons)
    #mark_test(circle)
    #mark_test(circles)
    #mark_test(ellipse)
    #mark_test(ellipses)
    #mark_test(rectangle)
    #mark_test(rectangles)
    #mark_test(text)
    #mark_test(texts)
    mark_test(layer)
    #mark_test(layers)
    app.MainLoop()
