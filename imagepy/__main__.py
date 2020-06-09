import wx, sys, os
sys.path.append('../')
from imagepy.core.app import loader, ImagePy
from imagepy import root_dir

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

def extend_wgts(wgt):
    if isinstance(wgt, tuple) and isinstance(wgt[1], list):
        return (wgt[0].title, extend_wgts(wgt[1]))
    elif isinstance(wgt, list): return [extend_wgts(i) for i in wgt]
    else: return (wgt.title, wgt)

if __name__ == '__main__':
    from skimage.data import camera, astronaut
    import wx.lib.agw.advancedsplash as AS
    
    app = wx.App(False)

    bitmap = wx.Bitmap(os.path.join(root_dir, 'data/logolong.png'), wx.BITMAP_TYPE_PNG)
    shadow = wx.Colour(255,255,255)
    # SplashScreen(bitmap, wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT, 3000, None, -1)
    
    asp = AS.AdvancedSplash(None, bitmap=bitmap, timeout=1000,
        agwStyle=AS.AS_TIMEOUT |
        AS.AS_CENTER_ON_PARENT |
        AS.AS_SHADOW_BITMAP,
        shadowcolour=shadow)

    
    frame = ImagePy(None)
    
    frame.load_menu(extend_plgs(loader.build_plugins('menus')))

    frame.load_tool(extend_tols(loader.build_tools('tools')), 'Transform')

    frame.load_widget(extend_wgts(loader.build_widgets('widgets')))
    
    #frame.show_img([camera()], 'camera')
    #frame.show_img([astronaut()], 'astronaut')
    frame.Show()
    app.MainLoop()