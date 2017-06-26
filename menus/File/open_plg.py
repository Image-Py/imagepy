import wx,os,sys
from scipy.misc import imread

if sys.version_info[0]==2:
    from urllib2 import urlopen
    from cStringIO import StringIO
else: 
    from urllib.request import urlopen
    from io import BytesIO as StringIO

from imagepy.core import manager
from imagepy import IPy
from imagepy.core.engine import Free
from imagepy.core.util import fileio
from imagepy.core.manager import ReaderManager

class OpenFile(fileio.Reader):
    title = 'Open'

    def load(self):
        self.filt = sorted(ReaderManager.all())
        return True

class OpenUrl(Free):
    title = 'Open Url'
    para = {'url':'http://data.imagepy.org/testdata/yxdragon.jpg'}
    view = [('lab', 'Input the URL, eg. http://data.imagepy.org/testdata/yxdragon.jpg'),
            (str, 'Url:', 'url', '')]
    
    def run(self, para = None):
        try:
            fp, fn = os.path.split(para['url'])
            fn, fe = os.path.splitext(fn) 
            response = urlopen(para['url'])
            ## TODO: Fixme!
            stream = StringIO(response.read())
            img = imread(stream)
            IPy.show_img([img], fn)
        except Exception as e:
            IPy.write('Open url failed!\tErrof:%s'%sys.exc_info()[1])
        
plgs = [OpenFile, OpenUrl]
    
if __name__ == '__main__':
    print(Plugin.title)
    app = wx.App(False)
    Plugin().run()