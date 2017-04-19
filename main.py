import wx, numpy

from ui.imagepy import ImagePy
import numpy
app = wx.App(False)
mainFrame = ImagePy(None)
mainFrame.Show()
app.MainLoop()
