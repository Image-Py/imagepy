import os.path as osp
import sys, os, wx

from . import IPy
from . import core
from . import menus
from . import tools
from . import ui

__version__ = "image v0.2"

import wx, os, sys
root_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(root_dir)

def show():
    from ui.imagepy import ImagePy
    app = wx.App(False)
    mainFrame = ImagePy(None)
    mainFrame.Show()
    app.MainLoop()

