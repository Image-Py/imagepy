import wx,os,sys
from glob import glob

from ..manager.openermanager import OpenerManager
from ... import IPy, root_dir
from ..engine import Free, Simple

def show(path, read):
    fp, fn = os.path.split(path)
    fn, fe = os.path.splitext(fn) 
    img = read(path)
    if img.ndim==3 and img.shape[2]==4:
        img = img[:,:,:3].copy()
    IPy.show_img([img], fn)

def add_opener(exts, read):
    for i in exts:
        OpenerManager.add(i, read, show)

class Opener(Free):
    para = {'path':''}

    def show(self):
        filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in self.filt])
        return IPy.getpath('Open..', filt, 'open', self.para)

    #process
    def run(self, para = None):
        fp, fn = os.path.split(para['path'])
        fn, fe = os.path.splitext(fn)
        read, show = OpenerManager.get(fe[1:])
        show(para['path'], read)

class Saver(Simple):
    note = ['all']
    para={'path':root_dir}

    def show(self):
        filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in self.filt])
        return IPy.getpath('Save..', filt, 'save', self.para)

    #process
    def run(self, ips, imgs, para = None):
        self.write(para['path'], ips.get_img())

class Sequence(Free):
    title = 'Sequence'
    para = {'path':root_dir, 'start':0, 'end':0, 'step':1, 'title':'sequence'}
    filt = []

    def show(self):
        filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in self.filt])
        rst = IPy.getpath('Import sequence', filt, 'open', self.para)
        if rst!=wx.ID_OK:return rst

        files = self.getfiles(self.para['path'])
        nfs = len(files)
        self.para['end'] = nfs-1
        self.view = [(str, 'Title','title',''), 
                     (int, (0, nfs-1), 0, 'Start', 'start', '0~{}'.format(nfs-1)),
                     (int, (0, nfs-1), 0, 'End', 'end', '0~{}'.format(nfs-1)),
                     (int, (0, nfs-1), 0, 'Step', 'step', '')]
        return IPy.get_para('Import sequence', self.view, self.para)


    def getfiles(self, name):
        p,f = os.path.split(name)
        s = p+'/*.'+name.split('.')[-1]
        return glob(s)

    def readimgs(self, names, read, shape, dtype):
        imgs = []
        for i in range(len(names)):
            IPy.set_progress(int(round((i+1.0)/len(names)*100)))
            img = read(names[i])
            if img.shape!=shape or img.dtype!=dtype:
                print('error:', names[i])
                continue
            imgs.append(img)
        IPy.set_progress(0)
        return imgs

    #process
    def run(self, para = None):
        fp, fn = os.path.split(para['path'])
        fn, fe = os.path.splitext(fn)
        read, show = OpenerManager.get(fe[1:])
        try:
            img = read(para['path'])
        except:
            IPy.alert('unknown img format!')
            return
        files = self.getfiles(para['path'])
        files.sort()
        imgs = self.readimgs(files[para['start']:para['end']+1:para['step']], 
                             read, img.shape, img.dtype)
        IPy.show_img(imgs, para['title'])