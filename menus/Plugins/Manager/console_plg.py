# -*- coding: utf-8 -*-
import wx
from core.engines import Free
from core.managers import PluginsManager
from wx.py.shell import ShellFrame
from core.managers import PluginsManager
import numpy as np
import scipy.ndimage as ndimg
import IPy

def getips():
    ips = IPy.get_ips()
    if ips is None:print 'no image opened!'
    return ips

def update():
    ips = IPy.get_ips()
    if not ips is None : ips.update='pix'

class Macros(dict):
    def __init__(self):
        for i in PluginsManager.plgs.keys():
            if not isinstance(i, str) or i == 'Command Line':
                print PluginsManager.plgs[i]
                continue
            name = filter(str.isalnum, i)
            exec('self.run_%s = lambda para=None, plg=PluginsManager.plgs[i]:plg().start(para)'%name)
            #exec('self._%s = PluginsManager.plgs[i]().start'%name)

cmds = {'IPy':IPy, 'ndimg':ndimg, 'update':update, 'curips':get_ips}

class Plugin(Free):
    title = 'Command Line'
    def __init__(self):
        cmds['plgs'] = Macros()

    def run(self, para=None):
        frame = ShellFrame(IPy.curapp, locals=cmds)
        frame.shell.run('# numpy(np) and scipy.ndimage(ndimg) has been imported!\n')
        frame.shell.run('# plgs.run_name() to call a ImagePy plugin.\n')
        frame.shell.run('# IPy is avalible here, and curips() to get the current ImagePlus, update() to redraw.\n')
        frame.Show(True)