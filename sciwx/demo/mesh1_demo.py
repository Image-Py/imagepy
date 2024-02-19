import sys, wx
import numpy as np
sys.path.append('../../')

from sciapp.object import Mesh, Scene
from sciwx.mesh import Canvas3D, MCanvas3D, Canvas3DFrame, Canvas3DNoteBook, Canvas3DNoteFrame
from sciapp.util import meshutil

# vts, fs, ns, cs = surfutil.build_ball((100,100,100), 50, (1,0,0))
verts, faces = meshutil.create_ball((0,0,0), 1)
ball = Mesh(verts=verts, faces=faces, colors=verts[:,2], cmap='jet')
ball2 = Mesh(verts=verts, faces=faces, colors=verts[:,2], mode='grid')
ball3 = Mesh(verts=verts, faces=faces, colors=verts[:,2], mode='grid')

def canvas3d_test():
    frame = wx.Frame(None, title='Canvas3D')
    canvas3d = Canvas3D(parent=frame)
    canvas3d.SetBackgroundColour((255,0,0))
    canvas3d.add_obj('ball', ball)
    frame.Show()

def mcanvas3d_test():
    frame = wx.Frame(None, title='MCanvas3D')
    canvas3d = MCanvas3D(frame)
    canvas3d.add_obj('ball', ball)
    frame.Show()

def canvas3d_frame_test():
    cnf = Canvas3DFrame(None)
    cnf.add_obj('ball', ball)
    cnf.Show()

def canvas3d_note_book():
    frame = wx.Frame(None, title='Canvas3D NoteBook')
    cnb = Canvas3DNoteBook(frame)
    canvas1 = cnb.add_canvas()
    canvas1.add_obj('ball', ball)
    canvas2 = cnb.add_canvas()
    canvas2.add_obj('ball2', ball2)
    canvas3 = cnb.add_canvas()
    canvas3.add_obj('ball3', ball3)
    frame.Show()

def canvas3d_note_frame():
    cnf = Canvas3DNoteFrame(None)
    canvas1 = cnf.add_canvas()
    canvas1.add_obj('ball1', ball)
    canvas2 = cnf.add_canvas()
    canvas2.add_obj('ball2', ball2)
    canvas2 = cnf.add_canvas()
    canvas2.add_obj('ball3', ball3)
    cnf.Show()
    
if __name__ == '__main__':
    app = wx.App()
    canvas3d_note_book()
    app.MainLoop()
