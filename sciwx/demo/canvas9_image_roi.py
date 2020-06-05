import sys
sys.path.append('../../')
from skimage.data import astronaut, camera
from sciwx.canvas import ICanvas
from sciapp.action import Tool
from sciapp.object import ROI, Line
import wx

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None)
    canvas = ICanvas(frame, autofit=True)
    canvas.set_img(camera())
    roi = ROI([Line([(0,0),(100,100),(300,500)])])
    canvas.image.roi = roi
    frame.Show()
    app.MainLoop()