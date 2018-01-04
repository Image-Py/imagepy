# -*- coding: utf-8 -*
# load and build the toolbar 
import wx  
import os
import numpy as np
from imagepy.ui.widgets import HistCanvas, CurvePanel
from ..core.loader import loader

def build_widget(parent, datas):
    for i in datas[1]:
        parent.AddPage(i(parent), i.title, False )


def build_widgets_panel(parent, datas):
    wpanel = wx.ScrolledWindow( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
    wpanel.SetScrollRate( 5, 5 ) 
    sizer = wx.BoxSizer( wx.VERTICAL )
    for i in datas[1]:
        choicebook = wx.Choicebook( wpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.CHB_DEFAULT )
        build_widget(choicebook, i)
        sizer.Add( choicebook, 0, wx.EXPAND |wx.ALL, 0 )
    wpanel.SetSizer( sizer )
    wpanel.Layout()
    sizer.Fit( wpanel )
    return wpanel

def build_widgets(parent, toolspath):
    datas = loader.build_widgets(toolspath)
    return build_widgets_panel(parent, datas)
    
    '''
    bSizer1 = wx.BoxSizer( wx.VERTICAL )
    #m_notebook1 = wx.Notebook( wpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
    m_notebook1 = wx.Choicebook( wpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.CHB_DEFAULT )
    m_panel2 = wx.Panel( m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
    bSizer2 = wx.BoxSizer( wx.VERTICAL )
    
    m_button1 = wx.Button( m_panel2, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
    bSizer2.Add( m_button1, 0, wx.ALL, 5 )
    
    m_button2 = wx.Button( m_panel2, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
    bSizer2.Add( m_button2, 0, wx.ALL, 5 )
    
    m_button3 = wx.Button( m_panel2, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
    bSizer2.Add(m_button3, 0, wx.ALL, 5 )
    
    
    m_panel2.SetSizer( bSizer2 )
    m_panel2.Layout()
    bSizer2.Fit( m_panel2 )
    m_notebook1.AddPage( m_panel2, u"histogram", True )
    #m_panel3 = wx.Panel( m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
    m_panel3 = CurvePanel(m_notebook1)
    m_panel3.set_hist(np.random.rand(256)+2)
    m_notebook1.AddPage( m_panel3, u"a page", False )
    
    bSizer1.Add( m_notebook1, 0, wx.EXPAND |wx.ALL, 0 )

    m_notebook1 = wx.Notebook( wpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
    
    m_panel2 = wx.Panel( m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
    bSizer2 = wx.BoxSizer( wx.VERTICAL )
    
    m_button1 = wx.Button( m_panel2, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
    bSizer2.Add( m_button1, 0, wx.ALL, 5 )
    
    m_button2 = wx.Button( m_panel2, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
    bSizer2.Add( m_button2, 0, wx.ALL, 5 )
    
    m_button3 = wx.Button( m_panel2, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
    bSizer2.Add(m_button3, 0, wx.ALL, 5 )
    
    
    m_panel2.SetSizer( bSizer2 )
    m_panel2.Layout()
    bSizer2.Fit( m_panel2 )
    m_notebook1.AddPage( m_panel2, u"histogram", True )
    m_panel3 = wx.Panel( m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
    m_notebook1.AddPage( m_panel3, u"a page", False )
    
    bSizer1.Add( m_notebook1, 0, wx.EXPAND |wx.ALL, 0 )

    wpanel.SetSizer( bSizer1 )
    wpanel.Layout()
    bSizer1.Fit( wpanel )

    return wpanel
    '''
