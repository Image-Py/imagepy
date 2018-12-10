from imagepy import IPy
from imagepy.core.engine import Simple
from imagepy.core import myvi
import numpy as np

class Plugin(Simple):
    title = 'RGB Points Cloud'
    note = ['rgb']
    para = {'name':'undifine', 'num':100, 'r':1}
    view = [(str, 'name', 'Name', ''),
            (int, 'num', (10,1024), 0, 'number', 'points'),
            (float, 'r', (0.1,30), 1, 'radius', '')]
    
    def load(self, para):
        self.frame = myvi.Frame3D.figure(IPy.curapp, title='3D Canvas')
        return True

    def run(self, ips, imgs, para = None):
        num,r = para['num'], para['r']
        if ips.roi != None: pts = ips.img[ips.get_msk()]
        else: pts = ips.img.reshape((-1,3))
        pts = pts[::len(pts)//num]
        vts, fs, ns, cs = myvi.build_balls(pts, np.ones(len(pts))*r, pts/255)
        self.frame.viewer.add_surf_asyn(para['name'], vts, fs, ns, cs)
        (r1,g1,b1),(r2,g2,b2) = (0,0,0),(1,1,1)
        rs = (r1,r2,r2,r1,r1,r1,r1,r1,r1,r2,r2,r1,r2,r2,r2,r2)
        gs = (g1,g1,g1,g1,g1,g2,g2,g1,g2,g2,g2,g2,g2,g1,g1,g2)
        bs = (b1,b1,b2,b2,b1,b1,b2,b2,b2,b2,b1,b1,b1,b1,b2,b2)
        vts, fs, ns, cs = myvi.build_cube((0,0,0),(255,255,255))
        cs = list(zip(rs,gs,bs))
        self.frame.viewer.add_surf_asyn('cube', vts, fs, ns, cs, mode='grid')
        self.frame.Raise()
        self.frame = None
        #self.frame.add_surf2d('dem', ips.img, ips.lut, scale, sigma)

if __name__ == '__main__':
    pass