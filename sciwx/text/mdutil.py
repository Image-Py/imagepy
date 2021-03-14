from markdown import markdown
import os.path as osp

def md2html(mdstr, css=None):
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite',
        'markdown.extensions.tables','markdown.extensions.toc']#, 'mdx_math']
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
    css = css or osp.join(osp.split(osp.abspath(__file__))[0], 'markdown.css')
    return html % (css, markdown(mdstr, extensions=exts))

if __name__ == '__main__':
    print(md2html('#abc'))
