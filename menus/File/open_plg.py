import wx,os,sys
from scipy.misc import imread
import cStringIO, urllib2
from core import managers
import IPy

from core.engines import Free

class OpenFile(Free):
    title = 'Open'
    para = {'path':''}
    
    def show(self):
        filt = 'BMP files (*.bmp)|*.bmp|PNG files (*.png)|*.png|JPG \
        files (*.jpg)|*.jpg|GIF files (*.gif)|*.gif|TIF files (*.tif)|*.tif'
        return IPy.getpath('Open..', filt, self.para)
    #process
    def run(self, para = None):
        path = para['path']
        recent = __import__("menus.File.Open Recent.recent_plgs",'','',[''])
        recent.add(path)

        fp, fn = os.path.split(path)
        fn, fe = os.path.splitext(fn) 
        img = imread(path)
        if img.ndim==3 and img.shape[2]==4:
            img = img[:,:,:3].copy()
        IPy.show_img([img], fn)

class OpenUrl(Free):
    title = 'Open Url'
    para = {'url':'http://data.imagepy.org/testdata/yxdragon.jpg'}
    view = [('lab', 'Input the URL, eg. http://data.imagepy.org/testdata/yxdragon.jpg'),
            (str, 'Url:', 'url', '')]
    
    def run(self, para = None):
        try:
            fp, fn = os.path.split(para['url'])
            fn, fe = os.path.splitext(fn) 
            cont = urllib2.urlopen(para['url'])
            stream = cStringIO.StringIO(cont.read())
            img = imread(stream)
            IPy.show_img([img], fn)
        except Exception, e:
            IPy.write('Open url failed!\tErrof:%s'%sys.exc_info()[1])
        
plgs = [OpenFile, OpenUrl]
    
if __name__ == '__main__':
    print Plugin.title
    app = wx.App(False)
    Plugin().run()