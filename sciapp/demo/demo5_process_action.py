import sys
sys.path.append('../../')

from sciapp import App, Manager
from sciapp.action import SciAction
import os.path as osp
from skimage.io import imread, imsave
from skimage.data import camera
from scipy.ndimage import gaussian_filter

# overwrite the imread, read_csv, to make the demo works
# you can annotation it, but you need give a true path in this demo
def imread(path): return camera()

ReaderManager = Manager()
ReaderManager.add('png', imread)

class ImageReader(SciAction):
    '''supporting different image format'''
    name = 'ImageReader'

    def start(self, app, para=None):
        path = input('input the file path, or just a.png for test:')
        name, ext = osp.splitext(osp.split(path)[1])
        reader = ReaderManager.get(ext[1:])
        if reader is None:
            return app.alert('no reader for %s!'%ext[1:])
        app.show_img([reader(path)], name)

WriterManager = Manager()
WriterManager.add('png', imsave)

class ImageWriter(SciAction):
    '''write current image'''
    name = 'ImageWriter'

    def start(self, app, para=None):
        img = app.get_img()
        if img is None: return app.alert('no image')
        path = input('input the file path to save:')
        name, ext = osp.splitext(osp.split(path)[1])
        writer = WriterManager.get(ext[1:])
        if writer is None: 
            return app.alert('no writer for %s!'%ext[1:])
        writer(path, img.img)

class ImageAction(SciAction):
    name = 'ImageAction'
    para, view = None, None

    def run(self, img, para):pass

    def start(self, app, para=None): 
        image = app.get_img()
        if image is None: return app.alert('no image!')
        if self.para != None:
            app.show_para(self.name, self.para, self.view)
        self.run(image.img, self.para)

class Gaussian(ImageAction):
    '''now a gaussian filter should be like this'''
    name = 'Gaussian'
    para = {'sigma':5}
    view = [(int, 'sigma', (0,30), 0, 'sigma', 'px')]

    def run(self, img, para):
        img[:] = gaussian_filter(img, para['sigma'])

def read_gaussian_write():
    app = App()
    ImageReader().start(app)
    Gaussian().start(app)
    ImageWriter().start(app)

if __name__ == '__main__':
    read_gaussian_write()
