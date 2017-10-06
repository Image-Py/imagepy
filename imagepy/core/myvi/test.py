import sys, wx
sys.path.append('..')
from scipy.misc import imread
import threading
import myvi

def dem(frm):
	img = imread('C:/Users/Administrator/Desktop/dem.png')
	frm.add_surf2d('dem', img, lut=None, ds=1, smooth=0)

	frm.add_balls('ball', [(100,100,100)],[50], [(1,0,0)])

if __name__ == '__main__':
	app = wx.App(False)
	frm = myvi.GLFrame.get_frame(None, title='GLCanvas Sample')
	t = threading.Thread(target=dem,args=(frm,))
	t.setDaemon(True)
	t.start()
	app.MainLoop()