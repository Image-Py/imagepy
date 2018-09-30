# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 03:55:51 2016
@author: yxl
"""
from ... import IPy
from ...core.manager import ToolsManager

from wx import *
import wx, platform
# import wx, platform

menu_titles = [ "Open",
                "Properties",
                "Rename",
                "Delete" ]

menu_title_by_id = {}
for title in menu_titles:
    # menu_title_by_id[ wxNewId() ] = title
    menu_title_by_id[ wx.NewId() ] = title

list_title = "files"
list_items = [ "binding.py",
               "clipboard.py",
               "config.py",
               "debug.py",
               "dialog.py",
               "dispatch.py",
               "error.py", ]

class Tool:
    title = 'Tool'
    view, para = None, None 
    list = None
           
    def show(self):
        if self.view == None:return
        rst = IPy.get_para(self.title, self.view, self.para)
        if rst!=None : self.config()
    
    def config(self):pass
    def load(self):pass
    def switch(self):pass
    
    def start(self):
        ips = IPy.get_ips()
        if not ips is None and not ips.tool is None:
            ips.tool = None
            ips.update = True
        ToolsManager.set(self)

        
    def mouse_down(self, ips, x, y, btn, **key): pass
    def mouse_up(self, ips, x, y, btn, **key): pass
    def mouse_move(self, ips, x, y, btn, **key): pass
    def mouse_wheel(self, ips, x, y, d, **key): pass
    # def dropmenue(self, ips, x, y, btn, list_items, **key): 
    #     # build listF
    #     if not self.list:
    #         list_title = 'test'
    #         self.list  = wx.ListCtrl( key['canvas'],pos=(x,y), size=(1, 10),style=wx.LC_REPORT)
    #         self.list.InsertColumn( 0, list_title )

            
    #     for i, x in enumerate(list_items): 
    #         self.list.InsertStringItem(0,x)
    #         self.list.EnsureVisible(i)

    #     ### 1. Register source's EVT_s to invoke launcher. ###
    #     EVT_LIST_ITEM_RIGHT_CLICK( self.list, -1, self.RightClickCb )
    #     # clear variables
    #     self.list_item_clicked = None

    #     # # show &amp; run
    #     key['canvas'].Show(1)

    def dropmenue(self, ips, x, y, btn, list_items, **key): 

        box = wx.BoxSizer(wx.VERTICAL)

        # Make and layout the controls
        fs = key['canvas'].GetFont().GetPointSize()
        bf = wx.Font(fs+4, wx.SWISS, wx.NORMAL, wx.BOLD)
        nf = wx.Font(fs+2, wx.SWISS, wx.NORMAL, wx.NORMAL)

        t = wx.StaticText(key['canvas'], -1, "PopupMenu")
        t.SetFont(bf)
        box.Add(t, 0, wx.CENTER|wx.ALL, 5)

        box.Add(wx.StaticLine(key['canvas'], -1), 0, wx.EXPAND)
        box.Add((10,20))

        text = 'PopUp Menu'
        t = wx.StaticText(key['canvas'], -1, text)
        t.SetFont(nf)
        box.Add(t, 0, wx.CENTER|wx.ALL, 5)
        t.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)

        self.SetSizer(box)

        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)    
        # return 1
    def RightClickCb( self, event ):
        # record what was clicked
        self.list_item_clicked = right_click_context = event.GetText()
        
        ### 2. Launcher creates wxMenu. ###
        menu = wx.Menu()
        for (id,title) in menu_title_by_id.items():
            ### 3. Launcher packs menu with Append. ###
            menu.Append( id, title )
            ### 4. Launcher registers menu handlers with EVT_MENU, on the menu. ###
            EVT_MENU( menu, id, self.MenuSelectionCb )

        ### 5. Launcher displays menu with call to PopupMenu, invoked on the source component, passing event's GetPoint. ###
        key['canvas'].PopupMenu( menu, event.GetPoint() )
        menu.Destroy() # destroy to avoid mem leak

    def MenuSelectionCb( self, event ):
        # do something
        operation = menu_title_by_id[ event.GetId() ]
        target    = self.list_item_clicked
        print( 'Perform "%(operation)s" on "%(target)s."' % vars())
    def OnContextMenu(self, event):
        self.log.WriteText("OnContextMenu\n")

        # only do this part the first time so the events are only bound once
        #
        # Yet another anternate way to do IDs. Some prefer them up top to
        # avoid clutter, some prefer them close to the object of interest
        # for clarity. 
        if not hasattr(key['canvas'], "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
            self.popupID5 = wx.NewId()
            self.popupID6 = wx.NewId()
            self.popupID7 = wx.NewId()
            self.popupID8 = wx.NewId()
            self.popupID9 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnPopupOne, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnPopupTwo, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)
            self.Bind(wx.EVT_MENU, self.OnPopupSix, id=self.popupID6)
            self.Bind(wx.EVT_MENU, self.OnPopupSeven, id=self.popupID7)
            self.Bind(wx.EVT_MENU, self.OnPopupEight, id=self.popupID8)
            self.Bind(wx.EVT_MENU, self.OnPopupNine, id=self.popupID9)

        # make a menu
        menu = wx.Menu()
        # Show how to put an icon in the menu
        item = wx.MenuItem(menu, self.popupID1,"One")
        bmp = images.Smiles.GetBitmap()
        item.SetBitmap(bmp)
        menu.AppendItem(item)
        # add some other items
        menu.Append(self.popupID2, "Two")
        menu.Append(self.popupID3, "Three")
        menu.Append(self.popupID4, "Four")
        menu.Append(self.popupID5, "Five")
        menu.Append(self.popupID6, "Six")
        # make a submenu
        sm = wx.Menu()
        sm.Append(self.popupID8, "sub item 1")
        sm.Append(self.popupID9, "sub item 1")
        menu.AppendMenu(self.popupID7, "Test Submenu", sm)


        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()

    def OnContextMenu(self, event):
        self.log.WriteText("OnContextMenu\n")
        # only do this part the first time so the events are only bound once
        #
        # Yet another anternate way to do IDs. Some prefer them up top to
        # avoid clutter, some prefer them close to the object of interest
        # for clarity. 
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
            self.popupID5 = wx.NewId()
            self.popupID6 = wx.NewId()
            self.popupID7 = wx.NewId()
            self.popupID8 = wx.NewId()
            self.popupID9 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnPopupOne, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnPopupTwo, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)
            self.Bind(wx.EVT_MENU, self.OnPopupSix, id=self.popupID6)
            self.Bind(wx.EVT_MENU, self.OnPopupSeven, id=self.popupID7)
            self.Bind(wx.EVT_MENU, self.OnPopupEight, id=self.popupID8)
            self.Bind(wx.EVT_MENU, self.OnPopupNine, id=self.popupID9)

        # make a menu
        menu = wx.Menu()
        # Show how to put an icon in the menu
        item = wx.MenuItem(menu, self.popupID1,"One")
        bmp = images.Smiles.GetBitmap()
        item.SetBitmap(bmp)
        menu.AppendItem(item)
        # add some other items
        menu.Append(self.popupID2, "Two")
        menu.Append(self.popupID3, "Three")
        menu.Append(self.popupID4, "Four")
        menu.Append(self.popupID5, "Five")
        menu.Append(self.popupID6, "Six")
        # make a submenu
        sm = wx.Menu()
        sm.Append(self.popupID8, "sub item 1")
        sm.Append(self.popupID9, "sub item 1")
        menu.AppendMenu(self.popupID7, "Test Submenu", sm)


        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()
    def OnPopupOne(self, event):
        self.log.WriteText("Popup one\n")

   
# dropmenue方法，传入一个[(title, function), ...]

        