import wx, sys
sys.path.append('../../')
from sciwx.app import SciApp
from sciwx.canvas import CanvasFrame
from sciapp.action import ImgAction, Tool, DefaultTool
from sciwx.plugins.curve import Curve
from sciwx.plugins.channels import Channels
from sciwx.plugins.histogram import Histogram
from sciwx.plugins.viewport import ViewPort

from sciwx.plugins.filters import Gaussian, Undo
from sciwx.plugins.pencil import Pencil
from sciwx.plugins.io import Open, Save

if __name__ == '__main__':
    from skimage.data import camera
    
    app = wx.App(False)
    frame = SciApp(None)
    
    logo = 'C:/Users/54631/Documents/projects/imagepy/imagepy/tools/Standard/magic.gif'
    frame.load_menu(('menu',[('File',[('Open', Open),
                                      ('Save', Save)]),
                             ('Filters', [('Gaussian', Gaussian),
                                          ('Undo', Undo)])]))
    frame.load_tool(('tools',[('standard', [('P', Pencil),
                                            ('D', DefaultTool)]),
                              ('draw', [('X', Pencil),
                                        ('X', Pencil)])]), 'draw')
    frame.load_widget(('widgets', [('Histogram', [('Histogram', Histogram),
                                                  ('Curve', Curve),
                                                  ('Channels', Channels)]),
                                   ('Navigator', [('Viewport', ViewPort)])]))
    
    frame.show_img(camera())
    frame.show_img(camera())
    frame.Show()
    app.MainLoop()
