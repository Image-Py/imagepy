import wx
from .canvas import CanvasFrame
from .grid import GridFrame
from .text import MDFrame, TextFrame
from .plot import PlotFrame
from .mesh import Canvas3DFrame
from .widgets import ParaDialog
from sciapp.util.surfutil import *

app = None

def new_app():
    global app
    if app is None: app = wx.App()

def imshow(img, cn=0, log=False, autofit=True):
    new_app()
    cf = CanvasFrame(None, autofit)
    cf.set_img(img)
    cf.set_cn(cn)
    cf.set_log(log)
    cf.Show()
    return cf

def imstackshow(imgs, cn=0, log=False, autofit=True):
    new_app()
    cf = CanvasFrame(None, autofit)
    cf.set_imgs(imgs)
    cf.set_cn(cn)
    cf.set_log(log)
    cf.Show()
    return cf

def tabshow(tab):
    new_app()
    gf = GridFrame(None)
    gf.set_data(tab)
    gf.Show()
    return gf

def meshshow():
    new_app()
    cf = Canvas3DFrame(None)
    cf.Show()
    return cf

def txtshow(txt):
    new_app()
    tf = TextFrame(None)
    tf.append(txt)
    tf.Show()
    return tf

def mdshow(txt):
    new_app()
    new_app()
    mf = MDFrame(None)
    mf.set_cont(txt)
    mf.Show()
    return mf

def figure():
    new_app()
    pf = PlotFrame(None)
    pf.Show()
    return pf

def parashow(para, view, modal=True):
    new_app()
    pd = ParaDialog(None, 'Test')
    pd.init_view(view, para, preview=True, modal=modal)
    pd.pack()
    if modal: pd.ShowModal()
    else: pd.Show()
    return para

def show(): app.MainLoop()
