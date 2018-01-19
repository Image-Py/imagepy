# -*- coding: utf-8 -*-
import wx
from wx.py.shell import Shell
import scipy.ndimage as ndimg
import numpy as np
from imagepy import IPy

from imagepy.core.engine import Free
from imagepy.core.manager import PluginsManager

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

class Plugin(wx.Panel):
    title = 'Command Line'
    single = None
    def __init__(self, parent):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, 
                                pos = wx.DefaultPosition, size = wx.Size( 500,300 ), 
                                style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        shell = Shell(self, locals=cmds)
        bSizer = wx.BoxSizer( wx.VERTICAL )
        bSizer.Add( shell, 1, wx.EXPAND|wx.ALL, 5 )
        self.SetSizer(bSizer)
        cmds['plgs'] = Macros()
        shell.run('# numpy(np) and scipy.ndimage(ndimg) has been imported!\n')
        shell.run('# plgs.run_name() to call a ImagePy plugin.\n')
        shell.run('# IPy is avalible here, and curips() to get the current ImagePlus, update() to redraw.\n')