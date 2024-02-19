import sys, wx, numpy as np
sys.path.append('../../')
from sciwx.widgets import CMapPanel, CMapSelPanel, CurvePanel, HistPanel

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None)
    sizer = wx.BoxSizer(wx.VERTICAL)

    cmap = CMapPanel(frame)
    cmap.set_hist(np.random.rand(256)+2)
    sizer.Add(cmap, 0, 0, 0)

    cmapsel = CMapSelPanel(frame, 'color map')
    cmap = np.arange(256*3, dtype=np.uint8).reshape((3,-1)).T
    cmapsel.SetItems({'gray':cmap})
    sizer.Add(cmapsel, 0, 0, 0)

    hist = HistPanel(frame)
    hist.SetValue(np.random.rand(256))
    sizer.Add(hist, 0, 0, 0)

    curve = CurvePanel(frame, l=230)
    curve.set_hist(np.random.rand(256)+2)
    sizer.Add(curve, 0, 0, 0)

    frame.SetSizer(sizer)
    frame.Fit()
    frame.Show()
    app.MainLoop()
