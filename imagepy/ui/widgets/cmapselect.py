#!/usr/bin/env python

import wx, sys
import wx.adv
import numpy as np

if sys.version_info[0]==2:memoryview=np.getbuffer
class CMapSelPanel(wx.adv.OwnerDrawnComboBox):
    def __init__(self, parent):
        wx.adv.OwnerDrawnComboBox.__init__(self, parent, choices=[], 
            style=wx.CB_READONLY, pos=(20,40), size=(256, 30))
        self.handle = self.handle_
        self.Bind( wx.EVT_COMBOBOX, self.on_sel)

    def SetItems(self, ks, vs):
        self.Clear()
        if 'Grays' in ks:
            i = ks.index('Grays')
            ks.insert(0, ks.pop(i))
            vs.insert(0, vs.pop(i))
        self.AppendItems(ks)
        self.Select(0)
        self.ks, self.vs = ks, vs
    # Overridden from OwnerDrawnComboBox, called to draw each
    # item in the list
    def OnDrawItem(self, dc, rect, item, flags):
        if item == wx.NOT_FOUND:
            # painting the control, but there is no valid item selected yet
            return
        r = wx.Rect(*rect)  # make a copy
        r.Deflate(3, 5)
        cmap = None


        pen = wx.Pen(dc.GetTextForeground(), 3)
        dc.SetPen(pen)

        # for painting the items in the popup
        dc.DrawText(self.GetString( item),
                    r.x + 3,
                    (r.y + 0) + ( (r.height/2) - dc.GetCharHeight() )/2
                    )
        #dc.DrawLine( r.x+5, r.y+((r.height/4)*3)+1, r.x+r.width - 5, r.y+((r.height/4)*3)+1 )
        arr = np.zeros((10,256,3),dtype=np.uint8)
        arr[:] = self.vs[item]
        bmp = wx.Bitmap.FromBuffer(256,10, memoryview(arr))
        dc.DrawBitmap(bmp, r.x, r.y+15)


    # Overridden from OwnerDrawnComboBox, called for drawing the
    # background area of each item.
    def OnDrawBackground(self, dc, rect, item, flags):
        # If the item is selected, or its item # iseven, or we are painting the
        # combo control itself, then use the default rendering.
        if (item & 1 == 0 or flags & (wx.adv.ODCB_PAINTING_CONTROL |
                                      wx.adv.ODCB_PAINTING_SELECTED)):
            wx.adv.OwnerDrawnComboBox.OnDrawBackground(self, dc, rect, item, flags)
            return

    def GetValue(self):
        return self.ks[self.GetSelection()]


    # Overridden from OwnerDrawnComboBox, should return the height
    # needed to display an item in the popup, or -1 for default
    def OnMeasureItem(self, item):
        return 30
        # Simply demonstrate the ability to have variable-height items
        if item & 1:
            return 36
        else:
            return 24

    # Overridden from OwnerDrawnComboBox.  Callback for item width, or
    # -1 for default/undetermined
    def OnMeasureItemWidth(self, item):
        return -1; # default - will be measured from text width

    def handle_(slef):return

    def set_handle(self, handle=None):
        if handle is None: self.handle = self.handle_
        else: self.handle = handle

    def on_sel(self, event):
        print('aaa')
        self.handle()

if __name__ == '__main__':
    from glob import glob
    import os
    import numpy as np
    filenames = glob('../../data/luts/*.lut')
    keys = [os.path.split(filename)[-1][:-4] for filename in filenames]
    values = [np.fromfile(filename, dtype=np.uint8).reshape((3,256)).T.copy() for filename in filenames]
    lut = dict(zip(keys, values))

    app = wx.PySimpleApp()
    frame = wx.Frame(None)
    panel = wx.Panel(frame)
    pscb = CMapSelPanel(panel, choices=[], style=wx.CB_READONLY,
                                pos=(20,40), size=(256, 30))
    pscb.SetItems(keys, values)
    panel.Fit()
    frame.Fit()
    frame.Show(True)
    app.MainLoop() 