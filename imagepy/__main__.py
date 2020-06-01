import wx, sys
sys.path.append('../')
from imagepy.core.app import ImagePy
from imagepy.core.loader import loader

from sciapp.action import ImgAction, Tool, DefaultTool
from sciwx.plugins.curve import Curve
from sciwx.plugins.channels import Channels
from sciwx.plugins.histogram import Histogram
from sciwx.plugins.viewport import ViewPort
from sciwx.plugins.filters import Gaussian, Undo
from sciwx.plugins.pencil import Pencil
from sciwx.plugins.io import Open, Save

def extend_plgs(plg):
    if isinstance(plg, tuple):
        return (plg[0].title, extend_plgs(plg[1]))
    elif isinstance(plg, list):
        return [extend_plgs(i) for i in plg]
    elif isinstance(plg, str): return plg
    else: return (plg.title, plg)

def extend_tols(tol):
    if isinstance(tol, tuple) and isinstance(tol[1], list):
        return (tol[0].title, extend_tols(tol[1]))
    elif isinstance(tol, tuple) and isinstance(tol[1], str):
        return (tol[1], tol[0])
    elif isinstance(tol, list): return [extend_tols(i) for i in tol]

if __name__ == '__main__':
    from skimage.data import camera, astronaut
    
    app = wx.App(False)
    frame = ImagePy(None)
    
    #frame.load_menu(('menu',[('File',[('Open', Open),
    #                                  ('Save', Save)]),
    #                         ('Filters', [('Gaussian', Gaussian),
    #                                      ('Undo', Undo)])]))
    
    frame.load_menu(extend_plgs(loader.build_plugins('menus')))

    #frame.load_tool(('tools',[('standard', [('P', Pencil),
    #                                        ('D', DefaultTool)]),
    #                          ('draw', [('X', Pencil),
    #                                    ('X', Pencil)])]), 'draw')

    frame.load_tool(extend_tols(loader.build_tools('tools')), 'Transform')

    frame.load_widget(('widgets', [('Histogram', [('Histogram', Histogram),
                                                  ('Curve', Curve),
                                                  ('Channels', Channels)]),
                                   ('Navigator', [('Viewport', ViewPort)])]))
    
    frame.show_img([camera()], 'camera')
    frame.show_img([astronaut()], 'astronaut')
    frame.Show()
    app.MainLoop()