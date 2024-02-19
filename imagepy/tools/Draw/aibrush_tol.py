from sciapp.action import ImageTool
import numpy as np
from time import time
from skimage.morphology import flood_fill, flood
from skimage.draw import line, disk
from skimage.segmentation import felzenszwalb
from sciapp.util import mark2shp
from scipy.ndimage import binary_fill_holes, binary_dilation, binary_erosion

def fill_normal(img, r, c, color, con, tor):
    img = img.reshape((img.shape+(1,))[:3])
    msk = np.ones(img.shape[:2], dtype='bool')
    for i in range(img.shape[2]):
        msk &= flood(img[:,:,i], (r, c), connectivity=con, tolerance=tor)
    img[msk] = color

def local_brush(img, back, r, c, color, sigma, msize):
    lab = felzenszwalb(back, 1, sigma, msize)
    msk = flood(lab, (r, c), connectivity=2)
    img[msk] = color

def local_pen(img, r, c, R, color):
    img = img.reshape((img.shape+(1,))[:3])
    rs, cs = disk((r, c), R/2+1e-6, shape=img.shape)
    img[rs, cs] = color

def local_in_fill(img, r, c, R, color, bcolor):
    img = img.reshape((img.shape+(1,))[:3])
    msk = (img == color).min(axis=2)
    filled = binary_fill_holes(msk)
    filled ^= msk
    rs, cs = disk((r, c), R/2+1e-6, shape=img.shape)
    msk[:] = 0
    msk[rs, cs] = 1
    msk &= filled
    img[msk] = bcolor

def local_out_fill(img, r, c, R, color, bcolor):
    img = img.reshape((img.shape+(1,))[:3])
    msk = (img != color).max(axis=2)
    rs, cs = disk((r, c), R/2+1e-6, shape=img.shape)
    buf = np.zeros_like(msk)
    buf[rs, cs] = 1
    msk &= buf
    img[msk] = bcolor

def local_sketch(img, r, c, R, color, bcolor):
    img = img.reshape((img.shape+(1,))[:3])
    msk = (img == color).min(axis=2)
    dilation = binary_dilation(msk, np.ones((3,3)))
    dilation ^= msk
    rs, cs = disk((r, c), R/2+1e-6, shape=img.shape)
    msk[:] = 0
    msk[rs, cs] = 1
    msk &= dilation
    img[msk] = bcolor

def global_both_line(img, r, c, color):
    img = img.reshape((img.shape+(1,))[:3])
    msk = np.ones(img.shape[:2], dtype='bool')
    for i in range(img.shape[2]):
        msk &= flood(img[:,:,i], (r, c), connectivity=2)
    dilation = binary_dilation(msk, np.ones((3,3)))
    dilation ^= msk
    img[dilation] = color

def global_out_line(img, r, c, color):
    img = img.reshape((img.shape+(1,))[:3])
    msk = np.ones(img.shape[:2], dtype='bool')
    for i in range(img.shape[2]):
        msk &= flood(img[:,:,i], (r, c), connectivity=2)
    msk = binary_fill_holes(msk)
    dilation = binary_dilation(msk, np.ones((3,3)))
    dilation ^= msk
    img[dilation] = color

def global_in_line(img, r, c, color):
    img = img.reshape((img.shape+(1,))[:3])
    msk = np.ones(img.shape[:2], dtype='bool')
    for i in range(img.shape[2]):
        msk &= flood(img[:,:,i], (r, c), connectivity=2)
    inarea = binary_fill_holes(msk)
    inarea ^= msk
    inarea ^= binary_erosion(inarea, np.ones((3,3)))
    img[inarea] = color

def global_in_fill(img, r, c, color):
    img = img.reshape((img.shape+(1,))[:3])
    msk = np.ones(img.shape[:2], dtype='bool')
    for i in range(img.shape[2]):
        msk &= flood(img[:,:,i], (r, c), connectivity=2)
    filled = binary_fill_holes(msk)
    filled ^= msk
    img[filled] = color

def global_out_fill(img, r, c, color):
    img = img.reshape((img.shape+(1,))[:3])
    ori = np.ones(img.shape[:2], dtype='bool')
    for i in range(img.shape[2]):
        ori &= flood(img[:,:,i], (r, c), connectivity=2)
    filled = binary_fill_holes(ori)
    dilation = binary_dilation(ori)
    dilation ^= filled
    rs, cs = np.where(dilation)
    if len(rs)==0: return
    msk = ((img == img[r,c]).min(axis=2)).astype(np.uint8)
    flood_fill(msk, (rs[0], cs[0]), 2, connectivity=2, inplace=True)
    img[msk==2] = color

'''
general: size

>>> local ===================================
block: minsize              | left
in fill: r                  | left shift
pen: r                      | left ctrl
sketch: r                   | left alt
out fill: r                 | left ctrl + alt

>>> global ==================================
flood:                      | right
in fill:                    | right shift
out line:                   | right ctrl
in line:                    | right alt
out fill:                   | right ctrl + alt

scale and move:             | wheel
'''

class Plugin(ImageTool):
    title = 'AI Brush'
    
    para = {'win':48, 'tor':10, 'con':'8-connect', 'ms':30, 'r':2, 'color':(255,0,128)}
    view = [(int, 'win', (28, 64), 0, 'window', 'size'),
            ('color', 'color', 'color', 'mark'),
            ('lab', None, '======= Brush ======='),
            (float, 'ms', (10, 50), 0, 'stickiness', 'pix'),
            ('lab', None, '=======  Pen  ======='),
            (int, 'r', (1, 30), 0, 'radius', 'pix'),
            ('lab', None, '======= Flood ======='),
            (int, 'tor', (0,1000), 0, 'tolerance', 'value'),
            (list, 'con', ['4-connect', '8-connect'], str, 'connect', 'pix')]
    
    def __init__(self):
        self.status = None
        self.pickp = (0,0)
        self.oldp = (0,0)
        
    def mouse_down(self, ips, x, y, btn, **key):
        if btn==2: 
            self.oldp = key['canvas'].to_panel_coor(x,y)
            self.status = 'move'
            return

        self.oldp = self.pickp = (y, x)
        color = self.app.manager('color').get('front')
        x = int(round(min(max(x,0), ips.img.shape[1])))
        y = int(round(min(max(y,0), ips.img.shape[0])))
        color = (np.mean(color), color)[ips.img.ndim==3]
        self.pickcolor = ips.img[y, x]
        ips.snapshot()

        if btn==1 and key['ctrl'] and key['alt']:
            self.status = 'local_out'
        elif btn==1 and key['ctrl']:
            self.status = 'local_pen'
        elif btn==1 and key['alt']:
            self.status = 'local_sketch'
        elif btn==1 and key['shift']:
            self.status = 'local_in'
        elif btn==1:
            self.status = 'local_brush'
        elif btn==3 and key['ctrl'] and key['alt']:
            self.status = 'global_out_fill'
            global_out_fill(ips.img, y, x, color)
            ips.update()
        elif btn==3 and key['ctrl']:
            self.status = 'global_out_line'
            global_out_line(ips.img, y, x, color)
            ips.update()
        elif btn==3 and key['alt']:
            self.status = 'global_in_line'
            global_in_line(ips.img, y, x, color)
            ips.update()
        elif btn==3 and key['shift']:
            self.status = 'global_in_fill'
            global_in_fill(ips.img, y, x, color)
            ips.update()
        elif btn==3:
            if (ips.img[y, x] - color).sum()==0: return
            conn = {'4-connect':1, '8-connect':2}
            conn = conn[self.para['con']]
            tor = self.para['tor']
            fill_normal(ips.img, y, x, color, conn, tor)
            ips.update()
    
    def mouse_up(self, ips, x, y, btn, **key):
        if btn==1 and (y,x)==self.pickp and key['ctrl']:
            x = int(round(min(max(x,0), ips.img.shape[1])))
            y = int(round(min(max(y,0), ips.img.shape[0])))
            self.app.manager('color').add('front', ips.img[y, x])
        self.status = None
        ips.mark = None
        ips.update()
    
    def make_mark(self, x, y):
        wins = self.para['win']
        rect = {'type':'rectangle', 'body':(x-wins, y-wins, wins*2, wins*2), 'color':self.para['color']}
        mark = {'type':'layer', 'body':[rect]}
        r = 2 if self.status=='local_brush' else self.para['r']/2
        mark['body'].append({'type':'circle', 'body':(x, y, r), 'color':self.para['color']})

        mark['body'].append({'type':'text', 'body':(x-wins, y-wins, 
            'S:%s W:%s'%(self.para['ms'], self.para['win'])), 'pt':False, 'color':self.para['color']})
        return mark2shp(mark)

    def mouse_move(self, ips, x, y, btn, **key):
        if self.status == None and ips.mark != None:
            ips.mark = None
            ips.update()
        if not self.status in ['local_pen','local_brush',
            'local_sketch','local_in','local_out','move']:  return
        img, color = ips.img, self.app.manager('color').get('front')
        x = int(round(min(max(x,0), img.shape[1])))
        y = int(round(min(max(y,0), img.shape[0])))
        
        if self.status == 'move':
            x,y = key['canvas'].to_panel_coor(x,y)
            key['canvas'].move(x-self.oldp[0], y-self.oldp[1])
            self.oldp = x, y
            ips.update()
            return

        rs, cs = line(*[int(round(i)) for i in self.oldp + (y, x)])
        np.clip(rs, 0, img.shape[0]-1, out=rs)
        np.clip(cs, 0, img.shape[1]-1, out=cs)

        color = (np.mean(color), color)[img.ndim==3]

        for r,c in zip(rs, cs):
            start = time()
            w = self.para['win']
            sr = (max(0,r-w), min(img.shape[0], r+w))
            sc = (max(0,c-w), min(img.shape[1], c+w))
            r, c = min(r, w), min(c, w)
            backclip = imgclip = img[slice(*sr), slice(*sc)]
            if not ips.back is None: 
                backclip = ips.back.img[slice(*sr), slice(*sc)]

            if self.status == 'local_pen':
                local_pen(imgclip, r, c, self.para['r'], color)
            if self.status == 'local_brush':
                if (imgclip[r,c] - color).sum()==0: continue
                local_brush(imgclip, backclip, r, c, color, 0, self.para['ms'])
            if self.status == 'local_in':
                local_in_fill(imgclip, r, c, self.para['r'], self.pickcolor, color)
            if self.status == 'local_sketch':
                local_sketch(imgclip, r, c, self.para['r'], self.pickcolor, color)
            if self.status=='local_out':
                local_out_fill(imgclip, r, c, self.para['r'], self.pickcolor, color)


        ips.mark = self.make_mark(x, y)
        self.oldp = (y, x)
        ips.update()
        
    def mouse_wheel(self, ips, x, y, d, **key):
        if key['shift']:
            if d>0: self.para['ms'] = min(50, self.para['ms']+1)
            if d<0: self.para['ms'] = max(10, self.para['ms']-1)
            ips.mark = self.make_mark(x, y)
        elif key['ctrl'] and key['alt']:
            if d>0: self.para['win'] = min(64, self.para['win']+1)
            if d<0: self.para['win'] = max(28, self.para['win']-1)
            ips.mark = self.make_mark(x, y)
        elif key['ctrl']:
            if d>0: self.para['r'] = min(30, self.para['r']+1)
            if d<0: self.para['r'] = max(2, self.para['r']-1)
            ips.mark = self.make_mark(x, y)
        elif self.status == None:
            if d>0:key['canvas'].zoomout(x, y, 'data')
            if d<0:key['canvas'].zoomin(x, y, 'data')
        ips.update()