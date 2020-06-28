from sciapp.action import Simple
from sciapp.object import Surface, MarkText
from sciapp.util import surfutil
import numpy as np

class Plugin(Simple):
    title = 'RGB Points Cloud'
    note = ['rgb']
    para = {'name':'undifine', 'num':100, 'r':1}
    view = [(str, 'name', 'Name', ''),
            (int, 'num', (10,1024), 0, 'number', 'points'),
            (float, 'r', (0.1,30), 1, 'radius', '')]

    def run(self, ips, imgs, para = None):
        num,r = para['num'], para['r']
        if ips.roi != None: pts = ips.img[ips.get_msk()]
        else: pts = ips.img.reshape((-1,3))
        pts = pts[::len(pts)//num]
        vts, fs, ns, cs = surfutil.build_balls(pts, np.ones(len(pts))*r, pts/255)
        self.app.show_mesh(Surface(vts, fs, ns, cs), para['name'])
        (r1,g1,b1),(r2,g2,b2) = (0,0,0),(1,1,1)
        rs = (r1,r2,r2,r1,r1,r1,r1,r1,r1,r2,r2,r1,r2,r2,r2,r2)
        gs = (g1,g1,g1,g1,g1,g2,g2,g1,g2,g2,g2,g2,g2,g1,g1,g2)
        bs = (b1,b1,b2,b2,b1,b1,b2,b2,b2,b2,b1,b1,b1,b1,b2,b2)
        vts, fs, ns, cs = surfutil.build_cube((0,0,0),(255,255,255))
        cs = list(zip(rs,gs,bs))
        self.app.show_mesh(Surface(vts, fs, ns, cs, mode='grid'), 'cube')

if __name__ == '__main__':
    pass