import wx, os, time, wx.html2 as webview
from markdown import markdown
from imagepy import IPy, root_dir

def md2html(mdstr):
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite',
        'markdown.extensions.tables','markdown.extensions.toc', 'mdx_math']

    html = '''
        <html lang="zh-cn">
            <head>
                <meta content="text/html; charset=utf-8" http-equiv="content-type" />
            </head>

            <script type="text/x-mathjax-config">
                MathJax.Hub.Config({
                  config: ["MMLorHTML.js"],
                  jax: ["input/TeX", "output/HTML-CSS", "output/NativeMML"],
                  extensions: ["MathMenu.js", "MathZoom.js"]
                });
            </script>

            <script type="text/javascript" 
                src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js">
            </script>

            <style>
                @import url("%s");
            </style>

            <body>
                %s
            </body>
        </html>
    '''

    ret = markdown(mdstr,extensions=exts)

    return html % (IPy.root_dir+'/data/markdown.css', ret)

class HtmlPanel(wx.Panel):
    def __init__(self, parent, cont='', url=''):
        wx.Panel.__init__(self, parent)
        self.frame = self.GetTopLevelParent()
        self.titleBase = self.frame.GetTitle()

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.wv = webview.WebView.New(self)
        self.Bind(webview.EVT_WEBVIEW_TITLE_CHANGED, self.OnWebViewTitleChanged, self.wv)

        sizer.Add(self.wv, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        if url != '': self.wv.LoadURL(url)
        else: self.wv.SetPage(cont, url)

    def SetValue(self, value):
        self.wv.SetPage(*value)

    def OnWebViewTitleChanged(self, evt):
        if evt.GetString() == 'about:blank': return
        if evt.GetString() == 'http:///': return
        self.frame.SetTitle("%s -- %s" % (self.titleBase, evt.GetString()))
        if os.path.exists(IPy.root_dir+'/data/index.htm'):
            os.remove(IPy.root_dir+'/data/index.htm')

class MkDownWindow(wx.Frame):
    def __init__(self, parent, title, cont, url):
        wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = title, size = wx.Size(500,500))
        logopath = os.path.join(root_dir, 'data/logo.ico')
        self.SetIcon(wx.Icon(logopath, wx.BITMAP_TYPE_ICO))
        cont = '\n'.join([i.strip() for i in cont.split('\n')])

        with open(IPy.root_dir+'/data/index.htm', 'w', encoding='utf-8') as f:
            f.write(md2html(cont))
        HtmlPanel(self, url = IPy.root_dir+'/data/index.htm')
        