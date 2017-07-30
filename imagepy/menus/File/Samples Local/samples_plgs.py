from imagepy import IPy
from imagepy.core.engine import Free
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
        if img.dtype != np.uint8: 
            img = img.astype(np.uint8)
        IPy.show_img([img], self.title)

    def __call__(self):
        return self

datas = ['face', 'ascent', '-', 'page', 'astronaut', 'horse', 'camera', 
    'hubble_deep_field', 'coins', 'immunohistochemistry', 'moon']

plgs = [i if i=='-' else Data(i) for i in datas]