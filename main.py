import wx
from ui.imagepy import ImagePy

app = wx.App(False)
mainFrame = ImagePy(None)
mainFrame.Show()

app.MainLoop()