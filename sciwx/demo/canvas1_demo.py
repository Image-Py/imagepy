import sys
sys.path.append('../../')
from skimage.data import astronaut, camera
from numpy.fft import fft2, fftshift
from sciwx.canvas import ICanvas as Canvas
from sciapp.object import Image
import wx

def gray_test():
    frame = wx.Frame(None, title='gray test')
    canvas = Canvas(frame, autofit=True)
    canvas.set_img(camera())
    frame.Show()

def rgb_test():
    frame = wx.Frame(None, title='gray test')
    canvas = Canvas(frame, autofit=True)
    canvas.set_img(astronaut())
    canvas.set_cn((0,1,2))
    frame.Show()

def rgb_gray_blend():
    frame = wx.Frame(None, title='blend')
    canvas = Canvas(frame, autofit=True)
    canvas.set_img(astronaut())
    canvas.set_cn((2,-1,-1))
    canvas.set_img(camera(), True)
    canvas.set_cn(0, True)
    canvas.set_mode(0.5)
    frame.Show()

def complex_test():
    frame = wx.Frame(None, title='fft')
    canvas = Canvas(frame, autofit=True)
    canvas.set_img(fftshift(fft2(camera())))
    canvas.set_rg((0,31015306))
    canvas.set_log(True)
    frame.Show()

if __name__ == '__main__':
    app = wx.App()
    gray_test()
    rgb_test()
    rgb_gray_blend()
    complex_test()
    app.MainLoop()
    
