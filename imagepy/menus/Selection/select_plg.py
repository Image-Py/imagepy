from sciapp.action import Simple, Free
from sciapp.object import ROI, Rectangle
from sciapp.util.shputil import geom2shp, geom_flatten, geom_union, mark2shp
from imagepy.app import ConfigManager
import json, time

class SelectAll(Simple):
    title = 'Select All'
    note = ['all']

    def run(self, ips, imgs, para = None):
        ips.roi = ROI(Rectangle([0, 0, ips.shape[1], ips.shape[0]]))

class SelectNone(Simple):
    title = 'Select None'
    note = ['all']

    def run(self, ips, imgs, para = None):
        ips.roi = None
        time.sleep(0.1)
        
class Add2Manager(Simple):
    title = 'ROI Add'
    note = ['all', 'req_roi']
    para = {'name':''}
    view = [(str, 'name', 'Name', '')]

    def run(self, ips, imgs, para = None):
        self.app.manager('roi').add(obj=ips.roi.to_mark(), name=para['name'])
        
class RemoveFManager(Simple):
    title = 'ROI Remove'
    note = ['all']
    para = {'name':''}

    def load(self, ips):
        titles = self.app.manager('roi').names()
        if len(titles)==0: 
            self.app.alert('No roi in manager!')
            return False
        self.para['name'] = titles[0]
        RemoveFManager.view = [(list, 'name', titles, str, 'Name', '')]
        return True

    def run(self, ips, imgs, para = None):
        self.app.manager('roi').remove(name=para['name'])

class LoadRoi(Simple):
    title = 'ROI Load'
    note = ['all']
    para = {'name':''}
    
    def load(self, ips):
        titles = self.app.manager('roi').names()
        if len(titles)==0: 
            self.app.alert('No roi in manager!')
            return False
        self.para['name'] = titles[0]
        LoadRoi.view = [(list, 'name', titles, str, 'Name', '')]
        return True

    def run(self, ips, imgs, para = None):
        ips.roi = mark2shp(self.app.manager('roi').get(name=para['name']))
        
class Inflate(Simple):
    title = 'ROI Inflate'
    note = ['all', 'req_roi']
    para = {'r':5}
    view = [(int, 'r', (1,100),0, 'radius', 'pix')]

    def run(self, ips, imgs, para = None):
        geom = ips.roi.to_geom().buffer(para['r'])
        ips.roi = ROI(geom2shp(geom_flatten(geom)))
        
class Shrink(Simple):
    title = 'ROI Shrink'
    note = ['all', 'req_roi']
    para = {'r':5}
    view = [(int, 'r', (1,100),0, 'radius', 'pix')]

    def run(self, ips, imgs, para = None):
        geom = ips.roi.to_geom().buffer(-para['r'])
        ips.roi = ROI(geom2shp(geom_flatten(geom)))
        
class Convex(Simple):
    title = 'ROI Convex Hull'
    note = ['all', 'req_roi']
    
    def run(self, ips, imgs, para = None):
        geom = ips.roi.to_geom().convex_hull
        ips.roi = ROI(geom2shp(geom_flatten(geom)))
        
class Box(Simple):
    title = 'ROI Bound Box'
    note = ['all', 'req_roi']
    
    def run(self, ips, imgs, para = None):
        a,b,c,d = ips.roi.to_geom().bounds
        ips.roi = ROI(Rectangle([a,b,c-a,d-b]))
        
class Clip(Simple):
    title = 'ROI Clip'
    note = ['all', 'req_roi']
    
    def run(self, ips, imgs, para = None):
        rect = Rectangle([0, 0, ips.shape[1], ips.shape[0]])
        geom = rect.to_geom().intersection(geom_flatten(ips.roi.to_geom()))
        ips.roi = ROI(geom2shp(geom_flatten(geom)))
        
class Invert(Simple):
    title = 'ROI Invert'
    note = ['all', 'req_roi']
    
    def run(self, ips, imgs, para = None):
        rect = Rectangle([0, 0, ips.shape[1], ips.shape[0]])
        geom = rect.to_geom().difference(geom_flatten(ips.roi.to_geom()))
        ips.roi = ROI(geom2shp(geom_flatten(geom)))
        
class Save(Simple):
    title = 'ROI Save'
    note = ['all', 'req_roi']
    para={'path':''}

    def show(self):
        self.para['path'] = self.app.get_path('ROI Save', ['roi'], 'save')
        return not self.para['path'] is None

    def run(self, ips, imgs, para = None):
        with open(para['path'], 'w') as f:
            f.write(json.dumps(ips.roi.to_mark()))

class Open(Simple):
    title = 'ROI Open'
    note = ['all']
    para={'path':''}

    def show(self):
        self.para['path'] = self.app.get_path('ROI Save', ['roi'], 'open')
        return not self.para['path'] is None

    def run(self, ips, imgs, para = None):
        with open(para['path']) as f:
            ips.roi = ROI(mark2shp(json.loads(f.read())))
       
class Intersect(Simple):
    title = 'ROI Intersect'
    note = ['all', 'req_roi']
    para = {'name':''}
    
    def load(self, ips):
        titles = self.app.manager('roi').names()
        if len(titles)==0: 
            self.app.alert('No roi in manager!')
            return False
        self.para['name'] = titles[0]
        self.view = [(list, 'name', titles, str, 'Name', '')]
        return True

    def run(self, ips, imgs, para = None):
        obj = mark2shp(self.app.manager('roi').get(name=para['name'])).to_geom()
        roi = geom_flatten(ips.roi.to_geom())
        ips.roi = ROI(geom2shp(geom_flatten(roi.intersection(obj))))

class Union(Simple):
    title = 'ROI Union'
    note = ['all', 'req_roi']
    para = {'name':''}
    
    def load(self, ips):
        titles = self.app.manager('roi').names()
        if len(titles)==0: 
            self.app.alert('No roi in manager!')
            return False
        self.para['name'] = titles[0]
        self.view = [(list, 'name', titles, str, 'Name', '')]
        return True

    def run(self, ips, imgs, para = None):
        obj = mark2shp(self.app.manager('roi').get(name=para['name'])).to_geom()
        roi = geom_flatten(ips.roi.to_geom())
        ips.roi = ROI(geom2shp(geom_flatten(roi.union(obj))))

class Diff(Simple):
    title = 'ROI Difference'
    note = ['all', 'req_roi']
    para = {'name':''}
    
    def load(self, ips):
        titles = self.app.manager('roi').names()
        if len(titles)==0: 
            self.app.alert('No roi in manager!')
            return False
        self.para['name'] = titles[0]
        self.view = [(list, 'name', titles, str, 'Name', '')]
        return True

    def run(self, ips, imgs, para = None):
        print(self.app.manager('roi').get(name=para['name']))
        obj = mark2shp(self.app.manager('roi').get(name=para['name'])).to_geom()
        roi = geom_flatten(ips.roi.to_geom())
        ips.roi = ROI(geom2shp(geom_flatten(roi.difference(obj))))

class SymDiff(Simple):
    title = 'ROI Symmetric Diff'
    note = ['all', 'req_roi']
    para = {'name':''}
    
    def load(self, ips):
        titles = self.app.manager('roi').names()
        if len(titles)==0: 
            self.app.alert('No roi in manager!')
            return False
        self.para['name'] = titles[0]
        self.view = [(list, 'name', titles, str, 'Name', '')]
        return True

    def run(self, ips, imgs, para = None):
        obj = mark2shp(self.app.manager('roi').get(name=para['name'])).to_geom()
        roi = geom_flatten(ips.roi.to_geom())
        ips.roi = ROI(geom2shp(geom_flatten(roi.symmetric_difference(obj))))

class Setting(Free):
    title = 'ROI Setting'
    para = ROI.default.copy()
    view = [('color', 'color', 'line', 'color'),
            ('color', 'fcolor', 'face', 'color'),
            ('color', 'tcolor', 'text', 'color'),
            (int, 'lw', (1,10), 0, 'width', 'pix'),
            (int, 'size', (1,30), 0, 'text', 'size'),
            (bool, 'fill', 'solid fill')]

    def run(self, para=None):
        for i in para: ROI.default[i] = para[i]
        ConfigManager.set('roi_style', para)

plgs = [SelectAll, SelectNone, 
        '-', Inflate, Shrink, Convex, Box, Clip, Invert, 
        '-', Open, Save, Add2Manager, LoadRoi, RemoveFManager,
        '-', Intersect, Union, Diff, SymDiff, '-', Setting]