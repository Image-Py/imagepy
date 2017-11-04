import wx, wx.html2 as webview
from markdown import markdown
from imagepy import IPy, root_dir
import os

def md2html(mdstr):
	exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite','markdown.extensions.tables','markdown.extensions.toc']

	html = '''
<html lang="zh-cn">
<head>
<meta content="text/html; charset=utf-8" http-equiv="content-type" />
</head>

<style>
h1,
h2,
h3,
h4,
h5,
h6,
p,
blockquote {
    margin: 0;
    padding: 0;
}
body {
    font-family: "Helvetica Neue", Helvetica, "Hiragino Sans GB", Arial, sans-serif;
    font-size: 13px;
    line-height: 18px;
    color: #737373;
    background-color: white;
    margin: 10px 13px 10px 13px;
}
table {
    margin: 10px 0 15px 0;
    border-collapse: collapse;
}
td,th { 
    border: 1px solid #ddd;
    padding: 3px 10px;
}
th {
    padding: 5px 10px;  
}

a {
    color: #0069d6;
}
a:hover {
    color: #0050a3;
    text-decoration: none;
}
a img {
    border: none;
}
p {
    margin-bottom: 9px;
}
p img {
    width:100%%;
}
h1,
h2,
h3,
h4,
h5,
h6 {
    color: #404040;
    line-height: 36px;
}
h1 {
    margin-bottom: 18px;
    font-size: 30px;
}
h2 {
    font-size: 24px;
}
h3 {
    font-size: 18px;
}
h4 {
    font-size: 16px;
}
h5 {
    font-size: 14px;
}
h6 {
    font-size: 13px;
}
hr {
    margin: 0 0 19px;
    border: 0;
    border-bottom: 1px solid #ccc;
}
blockquote {
    padding: 13px 13px 21px 15px;
    margin-bottom: 18px;
    font-family:georgia,serif;
    font-style: italic;
}
blockquote:before {
    content:"\201C";
    font-size:40px;
    margin-left:-10px;
    font-family:georgia,serif;
    color:#eee;
}
blockquote p {
    font-size: 14px;
    font-weight: 300;
    line-height: 18px;
    margin-bottom: 0;
    font-style: italic;
}
code, pre {
    font-family: Monaco, Andale Mono, Courier New, monospace;
}
code {
    background-color: #fee9cc;
    color: rgba(0, 0, 0, 0.75);
    padding: 1px 3px;
    font-size: 12px;
    -webkit-border-radius: 3px;
    -moz-border-radius: 3px;
    border-radius: 3px;
}
pre {
    display: block;
    padding: 14px;
    margin: 0 0 18px;
    line-height: 16px;
    font-size: 11px;
    border: 1px solid #d9d9d9;
    white-space: pre-wrap;
    word-wrap: break-word;
}
pre code {
    background-color: #fff;
    color:#737373;
    font-size: 11px;
    padding: 0;
}
sup {
    font-size: 0.83em;
    vertical-align: super;
    line-height: 0;
}
* {
    -webkit-print-color-adjust: exact;
}
@media screen and (min-width: 914px) {
    body {
        width: 854px;
        margin:10px auto;
    }
}
@media print {
    body,code,pre code,h1,h2,h3,h4,h5,h6 {
        color: black;
    }
    table, pre {
        page-break-inside: avoid;
    }
}
</style>

<body>

%s
</body>
</html>
	'''

	ret = markdown(mdstr,extensions=exts)
	f = open('yn.html', 'w', encoding='utf-8')
	f.write(html % ret);
	f.close()
	return html % ret

class HtmlPanel(wx.Panel):
	def __init__(self, parent, cont, url):
		wx.Panel.__init__(self, parent)
		self.frame = self.GetTopLevelParent()
		self.titleBase = self.frame.GetTitle()

		sizer = wx.BoxSizer(wx.VERTICAL)
		self.wv = webview.WebView.New(self)
		self.Bind(webview.EVT_WEBVIEW_TITLE_CHANGED, self.OnWebViewTitleChanged, self.wv)

		sizer.Add(self.wv, 1, wx.EXPAND)
		self.SetSizer(sizer)
		self.wv.SetPage(cont, url)

	def OnWebViewTitleChanged(self, evt):
		if evt.GetString() == 'about:blank': return
		if evt.GetString() == 'http:///': return
		self.frame.SetTitle("%s -- %s" % (self.titleBase, evt.GetString()))

class MkDownWindow(wx.Frame):
    def __init__(self, parent, title, cont, url):
        wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = title, size = wx.Size(500,500))
        logopath = os.path.join(root_dir, 'data/logo.ico')
        self.SetIcon(wx.Icon(logopath, wx.BITMAP_TYPE_ICO))
        HtmlPanel(self, md2html(cont), url)