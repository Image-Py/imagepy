#encoding:utf-8
from __future__ import absolute_import
from __future__ import print_function

import os,sys
root_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0,root_dir)

from . import core
from . import menus
from . import tools
from . import ui
from . import IPy
from . import IPyGL

__version__ = "ImagePy v0.2"

def show():
    import wx
    from ui.imagepy import ImagePy
    app = wx.App(False)
    mainFrame = ImagePy(None)
    mainFrame.Show()
    app.MainLoop()
