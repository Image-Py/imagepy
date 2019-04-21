# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 22:31:12 2016

@author: yxl
"""
from imagepy.core.manager import RoiManager
from imagepy.core.engine import Simple, Free
from imagepy.core.roi import RectangleRoi
from imagepy.core.roi import roiio
from imagepy import IPy

class SelectAll(Simple):
    """SelectAll: derived from imagepy.core.engine.Simple """
    title = 'Select All'
    note = ['all']

    def run(self, ips, imgs, para = None):
        ips.roi = RectangleRoi(0,0,ips.size[1],ips.size[0])

class SelectNone(Simple):
    """SelectNone: derived from imagepy.core.engine.Simple """
    title = 'Select None'
    note = ['all']

    def run(self, ips, imgs, para = None):
        ips.roi = None
        
class Add2Manager(Simple):
    """Add2Manager: derived from imagepy.core.engine.Simple """
    title = 'ROI Add'
    note = ['all', 'req_roi']
    para = {'name':''}
    view = [(str, 'name', 'Name', '')]

    def run(self, ips, imgs, para = None):
        RoiManager.add(para['name'], ips.roi)
        
class RemoveFManager(Simple):
    """Add2Manager: derived from imagepy.core.engine.Simple """
    title = 'ROI Remove'
    note = ['all']
    para = {'name':''}

    def load(self, ips):
        titles = list(RoiManager.rois.keys())
        if len(titles)==0: 
            IPy.alert('No roi in manager!')
            return False
        self.para['name'] = titles[0]
        RemoveFManager.view = [(list, 'name', titles, str, 'Name', '')]
        return True

    def run(self, ips, imgs, para = None):
        RoiManager.remove(para['name'])

class LoadRoi(Simple):
    """LoadRoi: derived from imagepy.core.engine.Simple """
    title = 'ROI Load'
    note = ['all']
    para = {'name':''}
    
    def load(self, ips):
        titles = list(RoiManager.rois.keys())
        if len(titles)==0: 
            IPy.alert('No roi in manager!')
            return False
        self.para['name'] = titles[0]
        LoadRoi.view = [(list, 'name', titles, str, 'Name', '')]
        return True

    def run(self, ips, imgs, para = None):
        ips.roi = RoiManager.get(para['name'])
        
class Inflate(Simple):
    """Inflate: derived from imagepy.core.engine.Simple """
    title = 'ROI Inflate'
    note = ['all', 'req_roi']
    para = {'r':5}
    view = [(int, 'r', (1,100),0, 'radius', 'pix')]

    def run(self, ips, imgs, para = None):
        ips.roi = ips.roi.buffer(para['r'])
        
class Shrink(Simple):
    """Shrink: derived from imagepy.core.engine.Simple """
    title = 'ROI Shrink'
    note = ['all', 'req_roi']
    para = {'r':5}
    view = [(int, 'r', (1,100),0, 'radius', 'pix')]

    def run(self, ips, imgs, para = None):
        ips.roi = ips.roi.buffer(-para['r'])
        
class Convex(Simple):
    """Convex: derived from imagepy.core.engine.Simple """
    title = 'ROI Convex Hull'
    note = ['all', 'req_roi']
    
    def run(self, ips, imgs, para = None):
        ips.roi = ips.roi.convex()
        
class Box(Simple):
    """Box: derived from imagepy.core.engine.Simple """
    title = 'ROI Bound Box'
    note = ['all', 'req_roi']
    
    def run(self, ips, imgs, para = None):
        ips.roi = ips.roi.bounds()
        
class Clip(Simple):
    """Clip: derived from imagepy.core.engine.Simple """
    title = 'ROI Clip'
    note = ['all', 'req_roi']
    
    def run(self, ips, imgs, para = None):
        rect = RectangleRoi(0,0,ips.size[1],ips.size[0])
        ips.roi = ips.roi.clip(rect)
        
class Invert(Simple):
    """Invert: derived from imagepy.core.engine.Simple """
    title = 'ROI Invert'
    note = ['all', 'req_roi']
    
    def run(self, ips, imgs, para = None):
        rect = RectangleRoi(0,0,ips.size[1],ips.size[0])
        ips.roi = ips.roi.invert(rect)
        
class Save(Simple):
    """Save: save roi as a wkt file """
    title = 'ROI Save'
    note = ['all', 'req_roi']
    para={'path':''}

    def show(self):
        filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in ['roi', 'wkt']])
        return IPy.getpath('Save..', filt, 'save', self.para)

    def run(self, ips, imgs, para = None):
        file = para['path']
        if file[-3:] == 'wkt':roiio.savewkt(ips.roi, file)
        if file[-3:] == 'roi':roiio.saveroi(ips.roi, file)

class Open(Simple):
    """Save: save roi as a wkt file """
    title = 'ROI Open'
    note = ['all']
    para={'path':''}

    def show(self):
        filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in ['roi', 'wkt']])
        return IPy.getpath('Save..', filt, 'open', self.para)

    def run(self, ips, imgs, para = None):
        file = para['path']

        if file[-3:] == 'wkt':ips.roi = roiio.readwkt(file)
        if file[-3:] == 'roi':ips.roi = roiio.readroi(file)
       
class Intersect(Simple):
    """Union: derived from imagepy.core.engine.Simple """
    title = 'ROI Intersect'
    note = ['all', 'req_roi']
    para = {'name':''}
    
    def load(self, ips):
        titles = list(RoiManager.rois.keys())
        if len(titles)==0: 
            IPy.alert('No roi in manager!')
            return False
        self.para['name'] = titles[0]
        self.view = [(list, 'name', titles, str, 'Name', '')]
        return True

    def run(self, ips, imgs, para = None):
        ips.roi = ips.roi.intersect(RoiManager.get(para['name']))

class Union(Simple):
    """Union: derived from imagepy.core.engine.Simple """
    title = 'ROI Union'
    note = ['all', 'req_roi']
    para = {'name':''}
    
    def load(self, ips):
        titles = list(RoiManager.rois.keys())
        if len(titles)==0: 
            IPy.alert('No roi in manager!')
            return False
        self.para['name'] = titles[0]
        self.view = [(list, 'name', titles, str, 'Name', '')]
        return True

    def run(self, ips, imgs, para = None):
        ips.roi = ips.roi.union(RoiManager.get(para['name']))

class Diff(Simple):
    """Diff: derived from imagepy.core.engine.Simple """
    title = 'ROI Difference'
    note = ['all', 'req_roi']
    para = {'name':''}
    
    def load(self, ips):
        titles = list(RoiManager.rois.keys())
        if len(titles)==0: 
            IPy.alert('No roi in manager!')
            return False
        self.para['name'] = titles[0]
        self.view = [(list, 'name', titles, str, 'Name', '')]
        return True

    def run(self, ips, imgs, para = None):
        ips.roi = ips.roi.diff(RoiManager.get(para['name']))

class SymDiff(Simple):
    """Diff: derived from imagepy.core.engine.Simple """
    title = 'ROI Symmetric Diff'
    note = ['all', 'req_roi']
    para = {'name':''}
    
    def load(self, ips):
        titles = list(RoiManager.rois.keys())
        if len(titles)==0: 
            IPy.alert('No roi in manager!')
            return False
        self.para['name'] = titles[0]
        self.view = [(list, 'name', titles, str, 'Name', '')]
        return True

    def run(self, ips, imgs, para = None):
        ips.roi = ips.roi.symmetric_diff(RoiManager.get(para['name']))

class Setting(Free):
    title = 'ROI Setting'

    def load(self):
        Setting.para = {'color':RoiManager.get_color(),
                     'lw':RoiManager.get_lw()}
        Setting.view = [('color', 'color', 'roi', 'color'),
                     (int, 'lw', (1,5), 0, 'line width', 'pix')]
        return True

    def run(self, para=None):
        RoiManager.set_color(para['color'])
        RoiManager.set_lw(para['lw'])

plgs = [SelectAll, SelectNone, 
        '-', Inflate, Shrink, Convex, Box, Clip, Invert, 
        '-', Open, Save, Add2Manager, LoadRoi, RemoveFManager,
        '-', Intersect, Union, Diff, SymDiff, '-', Setting]