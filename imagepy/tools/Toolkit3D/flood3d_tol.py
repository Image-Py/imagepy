from sciapp.action import ImageTool
import numpy as np
from skimage.morphology import flood_fill, flood
from sciapp.action import Filter, Simple

class FloodFill3D(Simple):
    title = 'Flood Fill 3D'
    note = ['all', 'stack3d']

    def run(self, ips, imgs, para = None):
        flood_fill(imgs, para['seed'], para['color'], connectivity=para['conn'], tolerance=para['tor'], inplace=True)

class Plugin(ImageTool):
    title = 'Flood Fill 3D'
    para = {'tor':10, 'con':'8-connect'}
    view = [(int, 'tor', (0,1000), 0, 'torlorance', 'value'),
            (list, 'con', ['4-connect', '8-connect'], str, 'fill', 'pix')]
        
    def mouse_down(self, ips, x, y, btn, **key):
        FloodFill3D().start(self.app, {'seed':(ips.cur, int(y), int(x)), 
            'color':np.mean(self.app.manager('color').get('front')),
            'conn':(self.para['con']=='8-connect')+1, 'tor':self.para['tor']})
    
    def mouse_up(self, ips, x, y, btn, **key):
        pass
    
    def mouse_move(self, ips, x, y, btn, **key):
        pass
        
    def mouse_wheel(self, ips, x, y, d, **key):
        pass

