from imagepy.core.manager import RoiManager
from imagepy.core.engine import Free

class Plugin(Free):
    title = 'Roi Setting'

    def load(self):
    	Plugin.para = {'color':RoiManager.get_color(),
    				 'lw':RoiManager.get_lw()}
    	Plugin.view = [('color', 'color', 'roi', 'color'),
    				 (int, 'lw', (1,5), 0, 'line width', 'pix')]
    	return True

    def run(self, para=None):
        RoiManager.set_color(para['color'])
        RoiManager.set_lw(para['lw'])