from sciapp.action import Filter
from skimage.measure import marching_cubes, mesh_surface_area
import numpy as np
import pandas as pd

class Plugin(Filter):
    modal = False
    title = 'Measure Surface And Volume'
    note = ['8-bit', 'not_slice', 'not_channel', 'preview']
    para = {'ds':2, 'thr':128, 'step':1}
    view = [('slide', 'thr', (0,255), 0, 'threshold'),
            (int, 'ds',   (1,20), 0, 'down scale', 'pix'),
            (int, 'step', (1,20), 0, 'march step', 'pix')]

    def load(self, ips):
        if not ips.is3d:
            IPy.alert('stack3d required!')
            return False
        self.buflut = ips.lut
        ips.lut = ips.lut.copy()
        return True
    
    def preview(self, ips, para):
        ips.lut[:] = self.buflut
        ips.lut[:para['thr']] = [255,0,0]
        ips.update()

    def cancel(self, ips):
        ips.lut = self.buflut
        ips.update()

    def run(self, ips, snap, img, para = None):
        ips.lut = self.buflut
        k, unit = ips.unit
        lev, ds, step = para['thr'], para['ds'], para['step']
        scube = np.cumprod(ips.imgs.shape)[-1] * k**3
        sfront = (ips.imgs[::ds,::ds,::ds]>lev).sum() * ds ** 3 * k**3
        sback = scube - sfront
        print(scube, sfront, sback)
        vts, fs, ns, cs =  marching_cubes_lewiner(ips.imgs[::ds,::ds,::ds], lev, step_size=step)
        area = mesh_surface_area(vts, fs) * (ds**2 * k **2)
        rst = [round(i,3) for i in [scube, sfront, sback, sfront/scube, area, area/sfront]]
        titles = ['Cube Volume', 'Volume', 'Blank', 'Volume/Cube', 'Surface', 'Volume/Surface']
        IPy.show_table(pd.DataFrame([rst], columns=titles), ips.title+'-Volume Measure')