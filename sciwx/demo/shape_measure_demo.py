import sys
sys.path.append('../../')
from sciapp.action import DistanceTool, AngleTool, SlopTool, AreaTool, CoordinateTool
from sciwx.canvas import CanvasFrame
from skimage.data import astronaut, camera
from sciapp.object import ROI, Line
import wx

ellipse = {'type':'ellipse', 'body':(100,100,100,-50,1)}
rectangles = {'type':'rectangles', 'body':[(100,100,80,50),(200,200,80,100)]}
layer = {'type':'layer', 'num':-1, 'color':(0,0,255), 'fill':False, 'body':[rectangles, ellipse]}

if __name__ == '__main__':
    app = wx.App()
    frame = CanvasFrame(None)
    bar = frame.add_toolbar()
    
    bar.add_tool('C', CoordinateTool)
    bar.add_tool('D', DistanceTool)
    bar.add_tool('A', AngleTool)
    bar.add_tool('T', SlopTool)
    bar.add_tool('S', AreaTool)

    frame.Show()
    frame.canvas.set_img(camera())
    app.MainLoop()