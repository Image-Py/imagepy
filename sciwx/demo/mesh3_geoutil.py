import sys, wx
sys.path.append('../../')

from sciwx.mesh import Canvas3D, MCanvas3D
from sciapp.util import surfutil, meshutil
from sciapp.object import Scene, Mesh, Surface2d, Surface3d, TextSet, Volume3d
from sciwx.mesh import Canvas3DFrame, Canvas3DNoteBook, Canvas3DNoteFrame
import sys, wx
import scipy.ndimage as ndimg
from skimage.data import moon, camera
import numpy as np

def dem_test():
    cnf = Canvas3DFrame(None)
    cnf.add_obj('dem', Surface2d(img=moon(), sample=1, sigma=1, k=0.3, cmap='jet'))
    cnf.Show()

def ball_test():
    cnf = Canvas3DFrame(None)
    vts, fs = meshutil.create_ball((100,100,100), 1)
    cnf.add_obj('ball', Mesh(vts, fs, colors=(1,0,0)))
    cnf.add_obj('line', TextSet(texts=['TEXT'], verts=[(101,100,100)], size=256))
    cnf.Show()

def random_ball_test():
    cnf = Canvas3DFrame(None)
    os = np.random.rand(30).reshape((-1,3))
    rs = np.random.rand(10)/7+0.05
    cs = np.random.rand(10)
    vts_b, fs_b, cs_b = meshutil.create_balls(os, rs, cs)
    cnf.add_obj('balls', Mesh(verts=vts_b, faces=fs_b, colors=cs_b, cmap='jet'))
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

    vts = np.array([x, y, z]).T.astype(np.float32)

    fs = np.arange(len(x), dtype=np.uint32)
    fs = np.array([fs[:-1], fs[1:]]).T

    # cs[:] = geoutil.auto_lookup(vts[:,2], geoutil.linear_color('jet'))/255
    cnf.add_obj('ball', Mesh(vts, fs, colors=vts[:,2], mode='grid', cmap='jet'))
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
    vts, fs = meshutil.create_grid_mesh(x, y, z)
    mesh = Mesh(vts, fs.astype(np.uint32), vts[:,2], mode='grid', cmap='jet')
    cnf.add_obj('ball', mesh)
    cnf.Show()


def ball_ring_test():
    cnf = Canvas3DFrame(None)
    os = np.random.rand(30).reshape((-1,3))
    rs = np.random.rand(10)/7 + 0.05
    cs = np.random.rand(10)
    vts_b, fs_b, cs_b = meshutil.create_balls(os, rs, cs)
    cnf.add_obj('balls', Mesh(verts=vts_b, faces=fs_b, colors=cs_b, cmap='jet'))
    
    vts_l, fs_l = meshutil.create_line(*os.T)
    cnf.add_obj('line', Mesh(verts=vts_l, faces=fs_l, colors=cs, cmap='jet', mode='grid'))
    # vts_c, fs_c, ns_c, cs_c = geoutil.build_cube((0,0,0), (1,1,1))

    vts_c, ls_c = meshutil.create_bound((0,0,0), (1,1,1), 3, 3, 3)
    cnf.add_obj('box', Mesh(verts=vts_c, faces=ls_c, ))
    cnf.Show()

def balls_mark_rest():
    cnf = Canvas3DFrame(None)
    os = np.random.rand(30).reshape((-1,3))
    rs = np.random.rand(10)/7+0.05
    cs = np.random.rand(10)
    vts_b, fs_b, cs_b = meshutil.create_balls(os, rs, cs)
    cont = ['ID:%s'%i for i in range(10)]

    # vtss, fss, pps, h, color = surfutil.build_marks(cont, os, rs, 0.05, (1,1,1))
    # cnf.add_obj('balls', Mesh(verts=vts_b.astype(np.float32), faces=fs_b.astype(np.uint32), colors=cs_b, cmap='jet'))
    cnf.add_obj('line', TextSet(texts=a, verts=b, size=1600, colors=c))
    cnf.Show()

def surface2d_test():
    cnf = Canvas3DFrame(None)
    x, y = np.ogrid[-2:2:20j, -2:2:20j]  
    z = x * np.exp( - x**2 - y**2)

    vts, fs = meshutil.create_surface2d(z, sample=1, k=10)
    dem = Mesh(verts=vts, faces=fs.astype(np.uint32), colors=z.ravel(), cmap='jet')
    cnf.add_obj('dem', dem)
    cnf.Show()

def arrow_test():
    cnf = Canvas3DFrame(None)
    v1, v2 = np.array([[[0,0,0],[5,5,5]],[[0,15,5],[2,8,3]]], dtype=np.float32)
    vts, fs, ns, cs = meshutil.build_arrows(v1, v2, 1, 1, 1, 1, (1,0,0))
    # vts, fs = meshutil.create_arrow(15, 15)
    cnf.add_obj('arrow', Mesh(vts, fs, colors=(1,0,0)))
    cnf.Show()

def cube_test():
    cnf = Canvas3DFrame(None)
    vts, fs, ls = meshutil.create_cube()
    cnf.add_obj('box', Mesh(vts, ls, colors=(1,0,0), mode='grid'))
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

def isosurface_test():
    cnf = Canvas3DFrame(None)
    cube = np.zeros((100,100,100), dtype=np.float32)
    x,y,z = np.random.randint(10,90,900).reshape(3,-1)
    cube[x,y,z] = 1000
    surf3d = Surface3d(cube, level=1.5, sigma=3, step=2, colors=(1,0,0))
    cnf.add_obj('volume', surf3d)
    cnf.Show()

def volume_test():
    cnf = Canvas3DFrame(None)
    cube = np.zeros((100,100,100), dtype=np.float32)
    x,y,z = np.random.randint(10,90,900).reshape(3,-1)
    cube[x,y,z] = 1000
    surf3d = Volume3d(cube, level=1.5, step=2, cmap='gray')
    cnf.add_obj('volume', surf3d)
    cnf.Show()
    
if __name__ == '__main__':
    app = wx.App()
    # balls_mark_rest()
    # dem_test()
    # ball_test()
    # random_ball_test()
    # line_test()
    # mesh_test()
    # ball_ring_test()
    # balls_mark_rest()
    # surface2d_test()
    # arrow_test() # bad
    # cube_test()
    # cube_surf_test() # bad
    # isosurface_test()
    volume_test()
    app.MainLoop()
