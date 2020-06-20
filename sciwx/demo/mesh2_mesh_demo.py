import sys, wx
sys.path.append('../../')

from sciwx.mesh import Canvas3D, MCanvas3D, MeshSet
from sciapp.util import surfutil
from sciapp.object import Surface
from sciwx.mesh import Canvas3DFrame, Canvas3DNoteBook, Canvas3DNoteFrame

vts, fs, ns, cs = surfutil.build_ball((100,100,100),50, (1,0,0))

def add_with_para():
    cnf = Canvas3DFrame(None)
    surf = Surface(vts, fs, ns, cs, mode='grid')
    cnf.add_surf('gridball', surf)
    cnf.Show()
    
def mesh_obj_test():
    cnf = Canvas3DFrame(None)
    meshes = MeshSet()
    vts, fs, ns, cs = surfutil.build_ball((100,100,100),50, (1,0,0))
    redball = Surface(vts, fs, ns, cs)
    meshes.add_surf('redball', redball)
    vts, fs, ns, cs = surfutil.build_ball((300,100,100),50, (1,1,0))
    yellowball = Surface(vts, fs, ns, cs, mode='grid')
    meshes.add_surf('yellowball', yellowball)
    hideball = Surface(vts, fs, ns, cs)
    vts, fs, ns, cs = surfutil.build_ball((300,-300,100),50, (0,1,0))
    hideball = Surface(vts, fs, ns, cs, visible=False)
    hideball = meshes.add_surf('hideball', hideball)
    meshes.background = (0, 0, 0.3)
    cnf.set_mesh(meshes)
    cnf.Show()

if __name__ == '__main__':
    app = wx.App()
    add_with_para()
    mesh_obj_test()
    app.MainLoop()
