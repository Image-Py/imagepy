import sys
sys.path.append('../../')

from skimage.data import astronaut, camera
from sciwx.canvas import CanvasFrame, CanvasNoteFrame
import wx

def canvas_frame_test():
    cf = CanvasFrame(None, autofit=True)
    cf.set_imgs([camera(), 255-camera()])
    cf.Show()

def canvas_note_test():
    cnf = CanvasNoteFrame(None)
    cv1 = cnf.add_canvas()
    cv1.set_img(camera())
    cv2 = cnf.add_canvas()
    cv2.set_img(astronaut())
    cv2.set_cn((2,1,0))
    cnf.Show()

if __name__ == '__main__':
    app = wx.App()
    canvas_frame_test()
    canvas_note_test()
    app.MainLoop()
