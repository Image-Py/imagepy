# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 03:32:05 2016

@author: yxl
"""
from ui.panelconfig import ParaDialog
from core.managers import TextLogManager
import IPy
import wx

class Simple:
    title = 'SimpleFilter'
    note = []
    para = None
    'all, 8_bit, 16_bit, rgb, float, req_roi, stack, stack2d, stack3d'
    view = None
    
    def __init__(self, ips=None):
        if ips==None:ips = IPy.get_ips()
        self.dialog = None
        self.ips = ips
    
    def load(self, ips):
        return True
        
    def show(self):
        if self.view==None:return wx.ID_OK
        self.dialog = ParaDialog(IPy.get_window(), self.title)
        self.dialog.init_view(self.view, self.para, modal=True)
        return self.dialog.ShowModal()
    
    def run(self, ips, imgs, para = None):pass
        
    def check(self, ips):
        note = self.note
        if ips == None:
            IPy.alert('no image opened!')
            return False
        elif 'req_roi' in note and ips.roi == None:
            IPy.alert('no Roi found!')
            return False
        elif not 'all' in note:
            if ips.get_imgtype()=='rgb' and not 'rgb' in note:
                IPy.alert('do not surport rgb image')
                return False
            elif ips.get_imgtype()=='8-bit' and not '8-bit' in note:
                IPy.alert('do not surport 8-bit image')
                return False
            elif ips.get_imgtype()=='16-bit' and not '16-bit' in note:
                IPy.alert('do not surport 16-bit image')
                return False
            elif ips.get_imgtype()=='float' and not 'float' in note:
                IPy.alert('do not surport float image')
                return False
        elif sum([i in note for i in ('stack','stack2d','stack3d')])>0:
            if ips.get_nslices()==1:
                IPy.alert('stack required!')
                return False
            elif 'stack2d' in note and ips.is3d:
                IPy.alert('stack2d required!')
                return False
            elif 'stack3d' in note and not ips.is3d:
                IPy.alert('stack3d required!')
                return False
            
        return True
        
    def start(self, para=None):
        #print self.title, para
        if not self.check(self.ips):return
        if not self.load(self.ips):return
        if para!=None or self.show() == wx.ID_OK:
            if para == None:para = self.para
            win = TextLogManager.get('Recorder')
            if win!=None: win.append('%s>%s'%(self.title, para))
            self.run(self.ips, self.ips.imgs, para)
            self.ips.update = 'pix'
        if self.dialog!=None:self.dialog.Destroy()