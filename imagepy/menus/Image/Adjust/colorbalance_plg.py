# -*- coding: utf-8 -*-
import numpy as np
from sciapp.action import Filter

class Plugin(Filter):
  title = 'Color Balance'
  note = ['rgb', 'auto_msk', 'auto_snap', 'not_channel', 'preview']

  para = {'bc_r':(0, 45), 'bc_g':(0, 45), 'bc_b':(0, 45)}

  def load(self, ips):
      hists = [ips.histogram(chans=i, step=512) for i in (0,1,2)]
      self.view =  [('hist', 'bc_r', 'bc', hists[0], (-255,255), 0),
                    ('hist', 'bc_g', 'bc', hists[1], (-255,255), 0),
                    ('hist', 'bc_b', 'bc', hists[2], (-255,255), 0)]
      return True

  def run(self, ips, snap, img, para = None):
      for i, c in zip([0,1,2], 'rgb'):
          mid = 128-para['bc_'+c][0]
          length = 255/np.tan(para['bc_'+c][1]/180.0*np.pi)
          xs = np.linspace(0,255,256)
          ys = 128 + (xs-mid)*(255/length)
          index = np.clip(ys, 0, 255).astype(np.uint8)
          img[:,:,i] = index[snap[:,:,i]]