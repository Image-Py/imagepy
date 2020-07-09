import wx, sys, os
from .manager import *
from . import loader
from imagepy import root_dir
from .manager import ConfigManager, DictManager

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

def load_plugins():
    data = loader.build_plugins(root_dir+'/menus')
    extends = glob(root_dir+'/plugins/*/menus')
    keydata = {}
    for i in data[1]:
        if isinstance(i, tuple): keydata[i[0].title] = i[1]
    for i in extends:
        plgs = loader.build_plugins(i)
        data[2].extend(plgs[2])
        for j in plgs[1]:
            if not isinstance(j, tuple): continue
            name = j[0].title
            if name in keydata: keydata[name].extend(j[1])
            else: data[1].append(j)
    return extend_plgs(data[:2]), data[2]

def load_tools():
    data = loader.build_tools('tools')
    extends = glob('plugins/*/tools')
    default = 'Transform'
    for i in extends:
        tols = loader.build_tools(i)
        #if len(tols)!=0: 
        data[1].extend(tols[1])
        data[2].extend(tols[2])
    return extend_tols(data[:2]), data[2]

def load_widgets():
    data = loader.build_widgets('widgets')
    extends = glob('plugins/*/widgets')
    for i in extends:
        wgts = loader.build_widgets(i)
        #if len(wgts)!=0: 
        data[1].extend(wgts[1])
        data[2].extend(wgts[2])
    return extend_wgts(data[:2]), data[2]

def load_document():
    docs = [root_dir+'/doc']
    docs += glob(root_dir+'/plugins/*/doc')
    for i in docs:loader.build_document(i)

def load_dictionary():
    lans = glob(root_dir+'/lang/*')
    lans += glob(root_dir+'/plugins/*/lang/*')
    lans = [i for i in lans if os.path.isdir(i)]
    lans = [os.path.split(i) for i in lans]
    lan = sorted(set([i[1] for i in lans]))
    DictManager.add('language', lan)
    lans = sorted(set([i[0] for i in lans]))
    for i in lans: loader.build_dictionary(i)

def start():
    from . import ImagePy, ImageJ
    import wx.lib.agw.advancedsplash as AS
    app = wx.App(False)
    bitmap = wx.Bitmap(root_dir+'/data/logolong.png', wx.BITMAP_TYPE_PNG)
    shadow = wx.Colour(255,255,255)
    asp = AS.AdvancedSplash(None, bitmap=bitmap, timeout=1000,
        agwStyle=AS.AS_TIMEOUT |
        AS.AS_CENTER_ON_PARENT |
        AS.AS_SHADOW_BITMAP,
        shadowcolour=shadow)
    asp.Update()
    load_document()
    load_dictionary()
    uistyle = ConfigManager.get('uistyle') or 'imagepy'
    frame = ImageJ(None) if uistyle == 'imagej' else ImagePy(None)
    frame.Show()
    app.MainLoop()