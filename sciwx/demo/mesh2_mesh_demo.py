import sys, wx
sys.path.append('../../')

from sciwx.mesh import Canvas3D, MCanvas3D, MeshSet, geoutil
from sciwx.mesh import Canvas3DFrame, Canvas3DNoteBook, Canvas3DNoteFrame

vts, fs, ns, cs = geoutil.build_ball((100,100,100),50, (1,0,0))

def add_with_para():
    cnf = Canvas3DFrame(None)
    cnf.add_surf('gridball', vts, fs, ns, cs, mode='grid')
    cnf.Show()
    
def mesh_obj_test():
    cnf = Canvas3DFrame(None)
    meshes = MeshSet()
    vts, fs, ns, cs = geoutil.build_ball((100,100,100),50, (1,0,0))
    redball = meshes.add_surf('redball', vts, fs, ns, cs)
    vts, fs, ns, cs = geoutil.build_ball((300,100,100),50, (1,1,0))
    yellowball = meshes.add_surf('yellowball', vts, fs, ns, cs)
    yellowball.mode = 'grid'
    vts, fs, ns, cs = geoutil.build_ball((300,-300,100),50, (0,1,0))
    hideball = meshes.add_surf('hideball', vts, fs, ns, cs)
    hideball.visible = False
    meshes.background = (0, 0, 0.3)
    cnf.set_mesh(meshes)
    cnf.Show()

if __name__ == '__main__':
    app = wx.App()
    add_with_para()
    mesh_obj_test()
    app.MainLoop()
