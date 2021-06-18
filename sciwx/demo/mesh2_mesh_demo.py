import sys, wx
sys.path.append('../../')

from sciwx.mesh import Canvas3D, MCanvas3D
from sciapp.util import meshutil
from sciapp.object import Scene, Mesh
from sciwx.mesh import Canvas3DFrame, Canvas3DNoteBook, Canvas3DNoteFrame

verts, faces = meshutil.create_sphere(16, 16, 16)
ball = Mesh(verts=verts, faces=faces, colors=(1,0,0), mode='grid')

def add_with_para():
    cnf = Canvas3DFrame(None)
    cnf.add_obj('gridball', ball)
    cnf.Show()
    
def mesh_obj_test():
    cnf = Canvas3DFrame(None)
    scene = cnf.canvas.scene3d
    verts, faces = meshutil.create_sphere(16, 16, 16)
    redball = Mesh(verts=verts*50+(100,100,100), faces=faces, colors=(1,0,0))
    scene.add_obj('redball', redball)
    verts, faces = meshutil.create_sphere(16, 16, 16)
    yellowball = Mesh(verts=verts*50+(300,100,100), faces=faces, colors=(1,1,0))
    scene.add_obj('yellowball', yellowball)
    verts, faces = meshutil.create_sphere(16, 16, 16)
    hideball = Mesh(verts=verts*50+(300,-300,100), faces=faces, colors=(0,1,0), visible=False)
    scene.add_obj('hideball', hideball)
    cnf.Show()

if __name__ == '__main__':
    app = wx.App()
    # add_with_para()
    mesh_obj_test()
    app.MainLoop()
