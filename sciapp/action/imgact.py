from .action import SciAction

class ImgAction(SciAction):
    title = 'Image Action'
    note, para, view = [], None, None

    def __init__(self): pass

    def show(self):
        ips, img, snap = self.ips, self.ips.img, self.ips.snap
        f = lambda p: self.run(ips, img, snap, p) or self.ips.update()
        return self.app.show_para(self.title, self.para, self.view, f, on_ok=None, 
            on_cancel=lambda x=self.ips:self.cancel(x), 
            preview='preview' in self.note, modal=True)

    def cancel(self, ips):
        ips.img[:] = ips.snap
        ips.update()

    def run(self, ips, img, snap, para):
        print('I am running!!!')

    def start(self, app, para=None, callback=None):
        print('Image Action Started!')
        self.app = app
        self.ips = app.get_img()
        if 'auto_snap' in self.note: self.ips.snapshot()
        if para!=None:
            self.run(self.ips, self.ips.img, self.ips.snap, para)
        elif self.view==None and self.__class__.show is ImgAction.show:
            self.run(self.ips, self.ips.img, self.ips.snap, para)
        elif self.show():
            self.run(self.ips, self.ips.img, self.ips.snap, self.para)
        elif 'auto_snap' in self.note: self.cancel(self.ips)
        self.ips.update()
