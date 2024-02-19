import sys
sys.path.append('../../')
from skimage.data import astronaut, camera
from sciapp.object import Image
from sciwx.canvas import ICanvas, MCanvas
import wx

def image_canvas_test():
    obj = Image()
    obj.img = camera()
    obj.cn = 0

    frame = wx.Frame(None, title='gray test')
    canvas = ICanvas(frame, autofit=True)
    canvas.set_img(obj)
    frame.Show()

def image_mcanvas_test():
    obj = Image()
    obj.imgs = [astronaut(), 255-astronaut()]
    obj.cn = 0

    frame = wx.Frame(None, title='gray test')
    canvas = MCanvas(frame, autofit=True)
    canvas.set_img(obj)
    frame.Show()

if __name__ == '__main__':
    app = wx.App()
    image_canvas_test()
    image_mcanvas_test()
    app.MainLoop()
