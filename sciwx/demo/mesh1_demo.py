import sys, wx
sys.path.append('../../')

from sciapp.object import Surface, MarkText, MeshSet
from sciwx.mesh import Canvas3DFrame, Canvas3DNoteBook, Canvas3DNoteFrame
from sciapp.util import surfutil
vts, fs, ns, cs = surfutil.build_ball((100,100,100),50, (1,0,0))

def canvas3d_test():
    frame = wx.Frame(None, title='Canvas3D')
    canvas3d = Canvas3D(frame)
    canvas3d.add_surf('ball', vts, fs, ns, cs)
    frame.Show()

def mcanvas3d_test():
    frame = wx.Frame(None, title='MCanvas3D')
    canvas3d = MCanvas3D(frame)
    canvas3d.add_surf('ball', vts, fs, ns, cs)
    frame.Show()

def canvas3d_frame_test():
    cnf = Canvas3DFrame(None)
    cnf.add_surf('ball', vts, fs, ns, cs)
    cnf.Show()

def canvas3d_note_book():
    frame = wx.Frame(None, title='Canvas3D NoteBook')
    cnb = Canvas3DNoteBook(frame)
    canvas1 = cnb.add_canvas()
    canvas1.add_surf('ball', vts, fs, ns, cs)
    canvas2 = cnb.add_canvas()
    canvas2.add_surf('ball', vts, fs, ns, cs, mode='grid')
    frame.Show()

def canvas3d_note_frame():
    cnf = Canvas3DNoteFrame(None)
    canvas1 = cnf.add_canvas()
    ball = Surface(vts, fs, ns, cs)
    canvas1.add_surf('ball', ball)
    canvas2 = cnf.add_canvas()
    ball = Surface(vts, fs, ns, cs)
    meshset = MeshSet('ABC', {'ball':ball})
    ball.mode = 'grid'
    canvas2.set_mesh(meshset)
    cnf.Show()
    
if __name__ == '__main__':
    app = wx.App()
    canvas3d_note_frame()
    app.MainLoop()
