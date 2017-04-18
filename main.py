import wx
from ui.imagepy import ImagePy
import numpy
app = wx.App(False)
mainFrame = ImagePy(None)
mainFrame.Show()
app.MainLoop()
# conda install -c newville wxpython-phoenix
