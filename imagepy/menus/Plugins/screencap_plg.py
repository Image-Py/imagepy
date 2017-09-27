from PIL import Image,ImageGrab
from imagepy import IPy
from imagepy.core.engine import Free
import numpy as np

class Plugin(Free):
    title = 'Screen Capture'
    
    def run(self, para = None):
        IPy.show_img([np.array(ImageGrab.grab())], 'Screen Capture')