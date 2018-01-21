from imagepy.core.engine import Free
from imagepy.core.manager import ConfigManager
from imagepy import IPy

class ImageJStyle(Free):
    title = 'Pay Tribute To ImageJ'
    asyn = False
    #process
    def run(self, para = None):
        ConfigManager.set('uistyle', 'ij')
        IPy.alert('Shown in ImageJ style when next setup!')

class ImagePyStyle(Free):
    title = 'Elegant ImagePy Style'
    asyn = False
    def run(self, para = None):
        ConfigManager.set('uistyle', 'ipy')
        IPy.alert('Shown in ImagePy style when next setup!')

plgs = [ImageJStyle, ImagePyStyle]