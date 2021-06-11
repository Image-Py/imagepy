from math import sin, cos, pi, atan, sqrt, asin
import numpy as np
from .. import MeshTool

class MeshViewTool(MeshTool):
    def __init__(self):
        self.oldxy = None
        self.status = ''
        self.curobj = None

    def mouse_down(self, obj, x, y, btn, **key):
        self.oldxy = x, y
        if btn == 1 and not key['shift']:
            picked = key['canvas'].at(x,y) if key['ctrl'] else None
            if not picked is None: 
                self.curobj = picked
                self.curobj.set_data(high_light=0xffaaffff)
            self.status = 'view'
        if btn == 1 and key['shift']:
            self.status = 'offset'
        if btn == 2: self.status = 'offset'
        if btn == 3:
            self.status = 'right'

    def mouse_up(self, obj, x, y, btn, **key):
        if self.status == 'right':
            key['canvas'].fit()
        if not self.curobj is None:
            self.curobj.set_data(high_light=False)
        self.curobj = None
        self.oldxy = None
        self.status = ''

    def mouse_move(self, obj, x, y, btn, **key):
        if self.status == 'view':
            dx = x - self.oldxy[0]
            dy = y - self.oldxy[1]
            camera = key['canvas'].camera
            camera.orbit(-dx/2, dy/2)
            self.oldxy = x, y
        if self.status == 'offset':
            camera = key['canvas'].camera
            dx = x - self.oldxy[0]
            dy = y - self.oldxy[1]
            norm = np.mean(camera._viewbox.size)
            k = 1 / norm * camera._scale_factor
            camera = key['canvas'].camera
            dx, dy, dz = camera._dist_to_trans((-dx*k, dy*k))
            self.oldxy = x, y
            cx, cy, cz = camera.center
            camera.center = cx + dx, cy + dy, cz + dz
        if self.status in {'right', 'light'}:
            self.status = 'light'
            lx, ly, lz = obj.light_dir
            dx = (x - self.oldxy[0])/360
            dy = (y - self.oldxy[1])/360
            ay = asin(lz/sqrt(lx**2+ly**2+lz**2))-dy
            xx = cos(dx)*lx - sin(dx)*ly
            yy = sin(dx)*lx + cos(dx)*ly
            ay = max(min(pi/2-1e-4, ay), -pi/2+1e-4)
            zz, k = sin(ay), cos(ay)/sqrt(lx**2+ly**2)
            obj.set_style(light_dir = (xx*k, yy*k, zz))
            self.oldxy = x, y


    def mouse_wheel(self, obj, x, y, d, **key):
        s = 1.1 ** - d
        camera = key['canvas'].camera
        if camera._distance is not None:
            camera._distance *= s
        camera.scale_factor *= s

MeshViewTool().start(None)