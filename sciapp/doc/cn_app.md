# App

App是一个科研应用接口，里面有若干Manager，用于管理应用进行中的各种Object，同时App定义了show_img, active_img, close_img, get_img, img_names等方法，对于table等其他类型数据有类似支持。这里的App仅仅实现了容器管理功能，而对于各种交互功能，都只是print实现。因而需要在某个示例中，用UI框架重载这些方法。



### 方法列举：

* **alert(self, info, title='sciapp'):** 弹出一个提示框，需要用户确认

* **yes_no(self, info, title='sciapp'):** 要求用户输入True/False

* **show_txt(self, cont, title='sciapp'):** 对用户进行文字提示

* **show_md(self, cont, title='sciapp'):** 以MarkDown语法书写，向用户弹出格式化文档

* **show_para(self, title, para, view, on_handle=None, on_ok=None, on_cancel=None, on_help=None, preview=False, modal=True):** 展示交互对话框，para是参数字典，view指定了交互方式。而在这个命令行版的App对象中，只能通过打印完成交互，因而其他参数这里没有作用。但App是一个交互式应用接口，对于界面应用，其他参数分别是，参数变化回调，对话框确认，取消回调，是否自动添加预览选项，对话框是否以模态方式展示

  ---

  **以下功能通过app.img_manager管理器实现**

* **show_img(self, img, title=None):** 展示一个Image对象，并添加到app.img_manager。

* **get_img(self, title=None):** 根据title获取Image，如果缺省则返回manager的第一个Image

* **img_names(self):** 返回当前app持有的Image对象名称列表

* **active_img(self, title=None):** 将指定名称的Image对象置顶，以便于get_img可以优先获得

* **close_img(self, title=None):** 关闭指定图像，并从app.img_manager移除

  ---
  **以下功能通过app.table_manager管理器实现**

* **show_table(self, tab, title=None):** 展示一个Table对象，并添加到app.tab_manager。

* **get_table(self, title=None):** 根据title获取Table，如果缺省则返回manager的第一个Table

* **table_names(self):** 返回当前app持有的Table对象名称列表

* **active_table(self, title=None):** 将指定名称的Table对象置顶，以便于get_tab可以优先获得

* **close_table(self, title=None):** 关闭指定图像，并从app.tab_manager移除

  

### 用法举例

这个例子演示app的一些基础交互功能，由于命令行只有简单的打印功能，因而这几个功能这里本质都是print

```python
def basic_test():
    app = App()
    # alert a message
    app.alert('Hello!', title='SciApp')
    # show a text, here just print it
    app.show_txt('Hello', title='SciApp')
    # show a markdown text, here just print it
    app.show_md('Hello', title='SciApp')
    # yes or no
    rst = app.yes_no('Are you ok?', 'SciApp')
    print(rst)
```



这个例子演示app进行一组参数交互

```python
def para_test():
    app = App()
    para = {'name':'', 'age':5}
    view = [(str, 'name', 'your', 'name'),
            (int, 'age', (0,120), 0, 'your', 'age')]
    rst = app.show_para('Personal Information', para, view)
    # >>> your: ? name <str> yxdragon
    # >>> your: ? age <int> 32
    print(rst)
    # >>> {'name':'yxdragon', 'age':32}
```



这个例子用Image说明，通过app对象的show，get，close方法来展示图像

```python
def object_test():
    from sciapp.object import Image
    from skimage.data import camera

    app = App()
    image = Image([camera()], 'camera')
    app.show_img(image, 'camera')
    # >>> UINT8  512x512  S:1/1  C:0/1  0.25M
    print(app.get_img())
    # >>> <sciapp.object.image.Image object at 0x000002076A025780>
    print(app.img_names())
    # >>> ['camera']
    app.close_img('camera')
    # >>> close image: camera
    print(app.img_names())
    # >>> []
```
