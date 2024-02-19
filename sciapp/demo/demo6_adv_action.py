import sys
sys.path.append('../../')

from sciapp.action.advanced import dataio, Filter
from scipy.ndimage import gaussian_filter
from skimage.io import imread, imsave
from skimage.data import camera
from sciapp import App

def imread(path): return camera()

for i in ('bmp', 'jpg', 'tif', 'png'):
    dataio.ReaderManager.add(i, imread, 'img')
    dataio.WriterManager.add(i, imsave, 'img')

class OpenFile(dataio.Reader):
    title = 'Open'

    def load(self):
        self.filt = sorted(dataio.ReaderManager.names())
        return True

class SaveImage(dataio.ImageWriter):
    title = 'Save Image'

    def load(self, ips):
        self.filt = sorted(dataio.WriterManager.names())
        return True

class Gaussian(Filter):
    title = 'Gaussian'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    para = {'sigma':2}
    view = [(float, 'sigma', (0,30), 1,  'sigma', 'pix')]
    
    def run(self, ips, snap, img, para = None):
        gaussian_filter(snap, para['sigma'], output=img)

def io_process_test():
    app = App(asyn=False)
    OpenFile().start(app)
    Gaussian().start(app)
    SaveImage().start(app)

def macros_test():
    app = App(asyn=False)
    for i in [OpenFile, SaveImage, Gaussian]:
        app.add_plugin(i.title, i)
        
    app.run_macros([('Open', None),
                    ('Gaussian', None),
                    ('Save Image', None)])

def macros_with_para():
    app = App(asyn=False)
    for i in [OpenFile, SaveImage, Gaussian]:
        app.add_plugin(i.title, i)
        
    app.run_macros([('Open', {'path':'camera.png'}),
                    ('Gaussian', {'sigma':2}),
                    ('Save Image', {'path':'blur.png'})])
    
if __name__ == '__main__':
    #io_process_test()
    #macros_test()
    macros_with_para()
