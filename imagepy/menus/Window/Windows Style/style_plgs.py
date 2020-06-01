from imagepy.core.engine import Free
from sciapp import Source

class ImageJStyle(Free):
    title = 'Pay Tribute To ImageJ'
    asyn = False
    def run(self, para = None):
        Source.manager('config').set('uistyle', 'ij')
        self.app.alert('Shown in ImageJ style when next setup!')

class ImagePyStyle(Free):
    title = 'Elegant ImagePy Style'
    asyn = False
    def run(self, para = None):
        Source.manager('config').set('uistyle', 'ipy')
        self.app.alert('Shown in ImagePy style when next setup!')

plgs = [ImageJStyle, ImagePyStyle]