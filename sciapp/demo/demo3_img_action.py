import sys
sys.path.append('../../')
from sciapp import App
from sciapp.object import Image
from skimage.data import camera
from scipy.ndimage import gaussian_filter
from skimage.feature import canny
import matplotlib.pyplot as plt

class SciAction:
    '''base action, just has a start method, alert a hello'''
    name = 'SciAction'

    def start(self, app, para=None): 
        self.app = app
        app.alert('Hello, I am SciAction!\n')
		
def action_demo1():
    app = App()
    SciAction().start(app)

class GaussianAction1(SciAction):
    '''get current image object, and do a gaussian filter with sigma 5'''
    name = 'GaussianAction1'

    def start(self, app, para=None): 
        image = app.get_img()
        image.img[:] = gaussian_filter(image.img, 5)
		
def action_demo2():
    app = App()

    image = Image([camera()], 'camera')
    app.show_img(image, 'camera')
    GaussianAction1().start(app)

    plt.subplot(121).imshow(camera())
    plt.subplot(122).imshow(image.img)
    plt.show()

class GaussianAction3(SciAction):
    '''follow the version 2, use show para to get sigma'''
    name = 'GaussianAction3'

    def start(self, app, para=None): 
        image = app.get_img()
        para = {'sigma':5}
        view = [(int, 'sigma', (0,30), 0, 'sigma', 'px')]
        app.show_para('GaussianAction3', para, view)
        image.img[:] = gaussian_filter(image.img, para['sigma'])
		
def action_demo3():
    app = App()

    image = Image([camera()], 'camera')
    app.show_img(image, 'camera')
    GaussianAction3().start(app)

    plt.subplot(121).imshow(camera())
    plt.subplot(122).imshow(image.img)
    plt.show()

class GaussianAction4(SciAction):
    '''split para, view to class field, and split gaussian to run method'''
    name = 'GaussianAction4'
    para = {'sigma':5}
    view = [(int, 'sigma', (0,30), 0, 'sigma', 'px')]

    def run(self, img, para):
        img[:] = gaussian_filter(img, para['sigma'])

    def start(self, app, para=None): 
        image = app.get_img()        
        app.show_para(self.name, self.para, self.view)
        self.run(image.img, self.para)
		
def action_demo4():
    app = App()

    image = Image([camera()], 'camera')
    app.show_img(image, 'camera')
    GaussianAction3().start(app)

    plt.subplot(121).imshow(camera())
    plt.subplot(122).imshow(image.img)
    plt.show()

class ImageAction(SciAction):
    '''
    this is a general image filter action
    we just need to define the para, view
    and overwrite the run method
    the start method will help us to check if there is a image opened.
    and show parameter if needed (para, view is redefined)
    then call the run method with current image and input parameter.
    '''
    name = 'ImageAction'
    para, view = None, None

    def run(self, img, para=None):pass

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
    
def action_demo5():
    app = App()
    image = Image([camera()], 'camera')
    app.show_img(image, 'camera')
    Gaussian().start(app)

    plt.subplot(121).imshow(camera())
    plt.subplot(122).imshow(image.img)
    plt.show()
    
if __name__ == '__main__':
    action_demo1()
    action_demo2()
    action_demo3()
    action_demo4()
    action_demo5()
    # action_demo6()
    
    
