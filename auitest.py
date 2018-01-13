#!/usr/bin/env python

import wx
import wx.aui as aui



#----------------------------------------------------------------------


class ParentFrame(aui.AuiMDIParentFrame):
    def __init__(self, parent):
        aui.AuiMDIParentFrame.__init__(self, parent, -1,
                                          title="AuiMDIParentFrame",
                                          size=(640,480),
                                          style=wx.DEFAULT_FRAME_STYLE)
        self.count = 0
        self.mb = self.MakeMenuBar()
        self.SetMenuBar(self.mb)
        self.CreateStatusBar()
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def MakeMenuBar(self):
        mb = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "New child window\tCtrl-N")
        self.Bind(wx.EVT_MENU, self.OnNewChild, item)
        item = menu.Append(-1, "Close parent")
        self.Bind(wx.EVT_MENU, self.OnDoClose, item)
        mb.Append(menu, "&File")
        return mb

    def OnNewChild(self, evt):
        self.count += 1
        child = ChildFrame(self, self.count)
        print('aaa', child.GetClientSize())
        #child.Show()

    def OnDoClose(self, evt):
        self.Close()

    def OnCloseWindow(self, evt):
        # Close all ChildFrames first else Python crashes
        for m in self.GetChildren():
            if isinstance(m, aui.AuiMDIClientWindow):
                for k in list(m.GetChildren()):
                    if isinstance(k, ChildFrame):
                        k.Close()
        evt.Skip()


#----------------------------------------------------------------------

class ChildFrame(aui.AuiMDIChildFrame):
    def __init__(self, parent, count):
        aui.AuiMDIChildFrame.__init__(self, parent, -1,
                                         title="Child: %d" % count)
        mb = parent.MakeMenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "This is child %d's menu" % count)
        mb.Append(menu, "&Child")
        self.SetMenuBar(mb)

        p = wx.Panel(self)
        wx.StaticText(p, -1, "This is child %d" % count, (10,10))
        p.SetBackgroundColour('light blue')

        sizer = wx.BoxSizer()
        sizer.Add(p, 1, wx.EXPAND)
        self.SetSizer(sizer)

        wx.CallAfter(self.Layout)

if __name__ == '__main__':
    app = wx.App(False)
    pf = ParentFrame(None)
    pf.Show()
    app.MainLoop()
