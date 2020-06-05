import sys
sys.path.append('../../')
from sciapp.object import mark2shp, Layer, json2shp
from sciapp.action import PointEditor, LineEditor, PolygonEditor, \
RectangleEditor, EllipseEditor, FreeLineEditor, FreePolygonEditor, BaseEditor
from sciwx.canvas import VectorFrame
from sciwx.plugins.filters import Gaussian
import wx

ellipse = {'type':'ellipse', 'body':(100,100,100,-50,1)}
rectangles = {'type':'rectangles', 'body':[(100,100,80,50),(200,200,80,100)]}
layer = {'type':'layer', 'num':-1, 'color':(0,0,255), 'fill':False, 'body':[rectangles, ellipse]}

if __name__ == '__main__':
    app = wx.App()
    frame = VectorFrame(None)
    frame.set_shp(mark2shp(layer))
    bar = frame.add_toolbar()
    
    bar.add_tool('E', BaseEditor)
    bar.add_tool('P', PointEditor)
    bar.add_tool('L', LineEditor)
    bar.add_tool('M', PolygonEditor)
    bar.add_tool('R', RectangleEditor)
    bar.add_tool('O', EllipseEditor)
    bar.add_tool('S', FreeLineEditor)
    bar.add_tool('&', FreePolygonEditor)
    
    frame.Show()
    app.MainLoop()
