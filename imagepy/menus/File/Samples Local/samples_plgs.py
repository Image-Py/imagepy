from sciapp.action import Free
from skimage import data
from scipy import misc
import numpy as np

class Data(Free):
    def __init__(self, title):
        self.title = title
        if hasattr(data, title):
            self.data = getattr(data, title)
        else : self.data = getattr(misc, title)

    def run(self, para = None):
        img = self.data()
        if isinstance(img, tuple):
            return self.app.show_img(list(img), self.title)
        if img.dtype == 'bool': 
            img.dtype = np.uint8
            img *= 255
        self.app.show_img([img], self.title)

    def __call__(self): return self

datas = ['face', 'ascent', '-', 'binary_blobs', 'brick', 'astronaut', 
    'camera', 'cell', 'checkerboard', 'chelsea', 'clock', 'coffee', 'coins',
    'colorwheel', 'grass', 'gravel', 'horse', 'hubble_deep_field', 
    'immunohistochemistry', 'microaneurysms', 'moon', 'page', 
    'text', 'retina', 'rocket', 'shepp_logan_phantom', 'stereo_motorcycle']

plgs = [i if i=='-' else Data(i) for i in datas]