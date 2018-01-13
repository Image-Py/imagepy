from wx.py.shell import Shell
import wx

# -*- coding: utf-8 -*-
import wx
from wx.py.shell import Shell
import scipy.ndimage as ndimg
import numpy as np
from imagepy import IPy

## There is something wrong!
## To be fixed!

def get_ips():
    ips = IPy.get_ips()
    if ips is None:
        print('no image opened!')
    return ips

def update():
    ips = IPy.get_ips()
    if not ips is None : 
        ips.update='pix'

class Macros(dict):
    def __init__(self):
        for i in list(PluginsManager.plgs.keys()):
            if not isinstance(i, str) or i == 'Command Line':
                #print(PluginsManager.plgs[i])
                continue
            name = ''.join(list(filter(str.isalnum, i)))
            ### TODO:Fixme! 
            #exec('self.run_%s = lambda para=None, 
            #      plg=PluginsManager.plgs[i]:plg().start(para)'%name)
            #self['run_%s'%i] = lambda para=None, plg=PluginsManager.plgs[i]:plg().start(para)
            exec('self.run_%s = lambda para=None, plg=PluginsManager.plgs[i]:plg().start(para)'%name)
            #exec('self._%s = PluginsManager.plgs[i]().start'%name)
        print(self)

cmds = {'IPy':IPy, 'ndimg':ndimg, 'update':update, 'curips':get_ips}

class ShellPanel ( Shell ):
	def __init__( self, parent ):
		Shell.__init__ ( self, parent, size = wx.Size( 500,300 ), locals=cmds)
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		self.shell = Shell( self)
		bSizer1.Add( self.shell, 1, wx.EXPAND |wx.ALL, 5 )
		self.SetSizer( bSizer1 )
		self.Layout()
	
	def __del__( self ): pass

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = wx.Frame(None)
    shell = ShellPanel(frame)
    frame.Fit()
    frame.Show(True)
    app.MainLoop() 