# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 00:56:00 2016

@author: yxl
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 22:56:50 2016

@author: yxl
"""
from core.engines import Filter
from ui.panelconfig import ParaDialog
from ui.widgets import HistCanvas
import IPy
import numpy as np

class Balance_Dialog(ParaDialog):
    def init_view(self, para, img):
        hists = [np.histogram(img[:,:,i],range(257))[0] for i in (0,1,2)]
        hists = [(i*(100.0/i.max())).astype(np.uint8) for i in hists]
        self.redcvs = HistCanvas(self)
        self.redcvs.set_hist(hists[0])
        self.greencvs = HistCanvas(self)
        self.greencvs.set_hist(hists[1])
        self.bluecvs = HistCanvas(self)
        self.bluecvs.set_hist(hists[2])
        
        self.add_ctrl('red', self.redcvs)
        self.parse(('slide', (0,255), 'Low', 't1_red', ''))
        self.parse(('slide', (0,255), 'High', 't2_red', ''))
        self.add_ctrl('green', self.greencvs)
        self.parse(('slide', (0,255), 'Low', 't1_green', ''))
        self.parse(('slide', (0,255), 'High', 't2_green', ''))
        self.add_ctrl('blue', self.bluecvs)
        self.parse(('slide', (0,255), 'Low', 't1_blue', ''))
        self.parse(('slide', (0,255), 'High', 't2_blue', ''))
        
        self.add_check('Preview', 'preview')
        self.add_confirm(True)
        self.reset(para)
        self.pack()
        
    def para_check(self, para, key):
        self.redcvs.set_lim(para['t1_red'], para['t2_red'])
        self.greencvs.set_lim(para['t1_green'], para['t2_green'])
        self.bluecvs.set_lim(para['t1_blue'], para['t2_blue'])
        if key == 't1_red':para['t2_red']=max(para['t2_red'], para['t1_red'])
        if key == 't2_red':para['t1_red']=min(para['t2_red'], para['t1_red'])
        if key == 't1_green':para['t2_green']=max(para['t2_green'], para['t1_green'])
        if key == 't2_green':para['t1_green']=min(para['t2_green'], para['t1_green'])
        if key == 't1_blue':para['t2_blue']=max(para['t2_blue'], para['t1_blue'])
        if key == 't2_blue':para['t1_blue']=min(para['t2_blue'], para['t1_blue'])
        self.reset()
        return True
        
class Plugin(Filter):
    title = 'Color Stairs'
    note = ['all', 'auto_msk', 'auto_snap', 'not_channel', 'preview']
    
    #parameter
    para = {'t1_red':0, 't2_red':255,'t1_green':0, 't2_green':255,'t1_blue':0, 't2_blue':255}
        
    def show(self):
        self.dialog = Balance_Dialog(IPy.get_window(), self.title)
        self.dialog.init_view(self.para, self.ips.get_img())
        self.dialog.set_handle(lambda x:self.preview(self.para))
        return self.dialog.ShowModal()

    #process
    def run(self, ips, img, buf, para = None):
        if para == None: para = self.para
        for i, c in zip([0,1,2],['red','green','blue']):
            buf[:,:,i] = img[:,:,i]
            buf[:,:,i] -= para['t1_'+c]
            buf[:,:,i] *= 255.0/max(para['t2_'+c]-para['t1_'+c], 1)
            buf[:,:,i][img[:,:,i]<para['t1_'+c]] = 0
            buf[:,:,i][img[:,:,i]>para['t2_'+c]] = 255
        return buf