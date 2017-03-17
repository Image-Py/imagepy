# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 23:33:52 2016

@author: yxl
"""

from ui.logwindow import TextLog
from core.managers import PluginsManager
from core.engines import Macros
import wx, IPy

class MacrosEditor(TextLog):
    def __init__(self, title='Macros Editor'):
        TextLog.__init__(self, title)
        m = wx.Menu()
        m_run = m.Append(-1, 'Run Macros\tF5')
        m_line = m.Append(-1, 'Run Line\tF6')
        self.menuBar.Insert(2,m,'Run(&R)')
        self.Bind(wx.EVT_MENU, self.run, m_run)
        self.Bind(wx.EVT_MENU, self.run_line, m_line)
        
    def run(self, event):
        cmds = self.text.GetValue().split('\n')
        Macros(None, cmds).start()
        
    def run_line(self, event):
        cmds = self.text.GetStringSelection().split('\n')
        Macros(None, cmds).start()
        
if __name__ == '__main__':

    app=wx.App(False)
    win = MacrosEditor()
    win.Show()
    win.append('abc')
    app.MainLoop()