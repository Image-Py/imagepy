import sys
sys.path.append('../../')
from skimage.data import astronaut, camera
from sciwx.canvas import MCanvas
import wx

def mcanvas_test():
    frame = wx.Frame(None, title='gray test1')
    canvas = MCanvas(frame, autofit=True)
    canvas.set_img(astronaut())
    canvas.set_cn((0,1,2))
    frame.Show()

def channels_test():
    frame = wx.Frame(None, title='gray test2')
    canvas = MCanvas(frame, autofit=True)
    canvas.set_img(astronaut())
    canvas.set_cn(0)
    frame.Show()

def sequence_test():
    frame = wx.Frame(None, title='gray test3')
    canvas = MCanvas(frame, autofit=True)
    canvas.set_imgs([astronaut(), 255-astronaut()])
    canvas.set_cn(0)
    frame.Show()

if __name__ == '__main__':
    app = wx.App()
    mcanvas_test()
    sequence_test()
    channels_test()
    app.MainLoop()
