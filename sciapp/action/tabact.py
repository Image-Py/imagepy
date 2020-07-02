from .action import SciAction

class TabAction(SciAction):
    title = 'Table Action'
    note, para, view = [], None, None

    def __init__(self): pass

    def show(self):
        tps, data, snap = self.tps, self.tps.data, self.tps.snap
        f = lambda p: self.run(tps, data, snap, p) or tps.update()
        return self.app.show_para(self.title, self.para, self.view, f, on_ok=None, 
            on_cancel=lambda x=self.tps:self.cancel(x), 
            preview='preview' in self.note, modal=True)

    def cancel(self, tps):
        tps.data[:] = pts.snap
        tps.update()

    def run(self, tps, snap, data, para = None):
        print('I am running!!!')

    def start(self, app, para=None, callback=None):
        self.app, self.tps = app, app.get_table()
        if 'auto_snap' in self.note:
            if 'auto_msk' in self.note: mode = True
            elif 'msk_not' in self.note: mode = False
            else: mode = None
            self.tps.snapshot(mode, 'num_only' in self.note)
        if para!=None:
            self.ok(self.tps, para, callback)
        elif self.view==None:
            if not self.__class__.show is Table.show:
                if self.show():
                    self.run(self.tps, para, callback)
            else: self.ok(self.tps, para, callback)
        elif self.modal:
            if self.show():
                self.ok(self.tps, para, callback)
            else:self.cancel(self.tps)
            if not self.dialog is None: self.dialog.Destroy()
        else: self.show()