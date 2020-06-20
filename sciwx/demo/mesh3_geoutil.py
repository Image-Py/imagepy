import sys, wx
sys.path.append('../../')

from sciwx.mesh import Canvas3D, MCanvas3D
from sciapp.util import surfutil
from sciapp.object import Surface, MarkText
from sciwx.mesh import Canvas3DFrame, Canvas3DNoteBook, Canvas3DNoteFrame
import sys, wx

import scipy.ndimage as ndimg
from skimage.data import moon, camera
import numpy as np

def dem_test():
    cnf = Canvas3DFrame(None)
    vts, fs, ns, cs = surfutil.build_surf2d(moon(), ds=1, k=0.3, sigma=2)
    cnf.add_surf('dem', Surface(vts, fs, ns, cs))
    cnf.Show()

def ball_test():
    cnf = Canvas3DFrame(None)
    vts, fs, ns, cs = geoutil.build_ball((100,100,100),50, (1,0,0))
    cnf.add_surf('ball', vts, fs, ns, cs)
    cnf.Show()

def random_ball_test():
    cnf = Canvas3DFrame(None)
    os = np.random.rand(30).reshape((-1,3))
    rs = np.random.rand(10)/5
    cs = (np.random.rand(10)*255).astype(np.uint8)
    cs = geoutil.linear_color('jet')[cs]/255
    vts, fs, ns, cs = geoutil.build_balls(os, rs, cs)
    cnf.add_surf('ball', vts, fs, ns, cs)
    cnf.Show()

def line_test():
    cnf = Canvas3DFrame(None)
    vts = np.array([(0,0,0),(1,1,0),(2,1,0),(1,0,0)], dtype=np.float32)
    fs = np.array([(0,1,2),(1,2,3)], dtype=np.uint32)
    ns = np.ones((4,3), dtype=np.float32)

    n_mer, n_long = 6, 11
    pi = np.pi
    dphi = pi / 1000.0
    phi = np.arange(0.0, 2 * pi + 0.5 * dphi, dphi)
    mu = phi * n_mer
    x = np.cos(mu) * (1 + np.cos(n_long * mu / n_mer) * 0.5)
    y = np.sin(mu) * (1 + np.cos(n_long * mu / n_mer) * 0.5)
    z = np.sin(n_long * mu / n_mer) * 0.5

    vts, fs, ns, cs = geoutil.build_line(x, y, z, (1, 0, 0))
    cs[:] = geoutil.auto_lookup(vts[:,2], geoutil.linear_color('jet'))/255
    cnf.add_surf('ball', vts, fs, ns, cs, mode='grid')
    cnf.Show()

def mesh_test():
    cnf = Canvas3DFrame(None)
    dphi, dtheta = np.pi/16.0, np.pi/16.0  
    [phi,theta] = np.mgrid[0:np.pi+dphi*1.5:dphi,0:2*np.pi+dtheta*1.5:dtheta]  
    m0 = 4; m1 = 3; m2 = 2; m3 = 3; m4 = 6; m5 = 2; m6 = 6; m7 = 4;  
    r = np.sin(m0*phi)**m1 + np.cos(m2*phi)**m3 + np.sin(m4*theta)**m5 + np.cos(m6*theta)**m7  
    x = r*np.sin(phi)*np.cos(theta)  
    y = r*np.cos(phi)  
    z = r*np.sin(phi)*np.sin(theta)  
    vts, fs, ns, cs = geoutil.build_mesh(x, y, z)
    cs[:] = geoutil.auto_lookup(vts[:,2], geoutil.linear_color('jet'))/255
    cnf.add_surf('ball', vts, fs, ns, cs)
    cnf.Show()


def ball_ring_test():
    cnf = Canvas3DFrame(None)
    os = np.random.rand(30).reshape((-1,3))
    rs = np.random.rand(10)/7
    cs = (np.random.rand(10)*255).astype(np.uint8)
    cs = geoutil.linear_color('jet')[cs]/255

    vts_b, fs_b, ns_b, cs_b = geoutil.build_balls(list(os), list(rs), list(cs))
    vts_l, fs_l, ns_l, cs_l = geoutil.build_line(os[:,0], os[:,1], os[:,2], list(cs))
    vts_c, fs_c, ns_c, cs_c = geoutil.build_cube((0,0,0), (1,1,1))
    cnf.add_surf('balls', vts_b, fs_b, ns_b, cs_b)
    cnf.add_surf('line', vts_l, fs_l, ns_l, cs_l, mode='grid')
    cnf.add_surf('box', vts_c, fs_c, ns_c, cs_c, mode='grid')
    cnf.Show()

def balls_mark_rest():
    cnf = Canvas3DFrame(None)
    os = np.random.rand(30).reshape((-1,3))
    rs = np.random.rand(10)/7+0.01
    cs = (np.random.rand(10)*255).astype(np.uint8)
    cs = surfutil.linear_color('jet')[cs]/255

    vts_b, fs_b, ns_b, cs_b = surfutil.build_balls(os, rs, cs)
    cont = ['ID:%s'%i for i in range(10)]
    vtss, fss, pps, h, color = surfutil.build_marks(cont, os, rs, 0.05, (1,1,1))
    cnf.add_surf('balls', Surface(vts_b, fs_b, ns_b, cs_b))
    cnf.add_surf('line', MarkText(vtss, fss, pps, h, color))
    cnf.Show()

def surface2d_test():
    cnf = Canvas3DFrame(None)
    x, y = np.ogrid[-2:2:20j, -2:2:20j]  
    z = x * np.exp( - x**2 - y**2)
    vts, fs, ns, cs = surfutil.build_surf2d(z, ds=1, k=20, sigma=2)
    cs[:] = surfutil.auto_lookup(vts[:,2], surfutil.linear_color('jet'))/255
    dem = Surface(vts, fs, ns, cs)
    cnf.add_surf('dem', dem)
    cnf.Show()

def arrow_test():
    cnf = Canvas3DFrame(None)
    v1, v2 = np.array([[[0,0,0],[5,5,5]],[[0,15,5],[2,8,3]]], dtype=np.float32)
    vts, fs, ns, cs = geoutil.build_arrows(v1, v2, 1, 1, 1, 1, (1,0,0))
    cnf.add_surf('arrow', vts, fs, ns, cs)
    cnf.Show()

def cube_test():
    cnf = Canvas3DFrame(None)
    vts, fs, ns, cs = geoutil.build_cube((0,0,0), (1,1,1))
    cnf.add_surf('box', vts, fs, ns, cs, mode='grid')
    cnf.Show()

def cube_surf_test():
    cnf = Canvas3DFrame(None)
    lut = np.zeros((256,3), dtype=np.uint8)
    lut[:,0] = np.arange(256)
    imgs = np.array([camera()[:300,::]]*256)
    vts, fs, ns, cs = geoutil.build_img_cube(imgs)
    obj = cnf.add_surf('cube', vts, fs, ns, cs)
    vts, fs, ns, cs = geoutil.build_img_box(imgs)
    cnf.add_surf('box', vts, fs, ns, cs, mode='grid')
    cnf.Show()

def volume_test():
    cnf = Canvas3DFrame(None)
    cube = np.zeros((100,100,100), dtype=np.float32)
    x,y,z = np.random.randint(10,90,900).reshape(3,-1)
    cube[x,y,z] = 1000
    cube = ndimg.gaussian_filter(cube, 3)
    vts, fs, ns, vs = geoutil.build_surf3d(cube, 1, 2)
    cnf.add_surf('volume', vts, fs, ns, (1,0,0))
    cnf.Show()
    
if __name__ == '__main__':
    app = wx.App()
    '''
    balls_mark_rest()
    dem_test()
    ball_test()
    random_ball_test()
    line_test()
    mesh_test()
    ball_ring_test()
    balls_mark_rest()
    surface2d_test()
    arrow_test()
    cube_test()
    cube_surf_test()
    volume_test()
    '''
    dem_test()
    app.MainLoop()
