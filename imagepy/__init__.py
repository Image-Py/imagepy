#from __future__ import absolute_import
import os.path as osp
import sys, os, wx

from wx.adv import SplashScreen as SplashScreen
import wx.lib.agw.advancedsplash as AS

from .IPy import *
from .core import ImagePlus, TablePlus
root_dir = osp.abspath(osp.dirname(__file__))
os.chdir(root_dir)

import matplotlib
matplotlib.use('WxAgg')
# sys.path.append(root_dir)

from .ui.mainframe import ImagePy

def show(ui = True):
	app = wx.App(False)
	
	bitmap = wx.Bitmap('data/logolong.png', wx.BITMAP_TYPE_PNG)
	shadow = wx.Colour(255,255,255)
	# SplashScreen(bitmap, wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT, 3000, None, -1)
	
	asp = AS.AdvancedSplash(None, bitmap=bitmap, timeout=1000,
		agwStyle=AS.AS_TIMEOUT |
		AS.AS_CENTER_ON_PARENT |
		AS.AS_SHADOW_BITMAP,
		shadowcolour=shadow)

	ImagePy(None).Show()
	app.MainLoop()
	
	