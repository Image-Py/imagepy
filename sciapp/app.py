import json, os.path as osp

class Manager:
    def __init__(self, unique=True, path=None):
        self.objs, self.unique, self.path = [], unique, path
        if not path is None: self.read(path)

    def add(self, name, obj, tag=None):
        if self.unique: self.remove(name, tag)
        self.objs.insert(0, (name, obj, tag))

    def active(self, name=None, tag=None, obj=None):
        objs = self.gets(name, tag, obj)
        for i in objs: self.objs.remove(i)
        for i in objs: self.objs.insert(0, i)

    def set(self, name, obj, tag=None):
        self.remove(name, tag)
        self.objs.insert(0, (name, obj, tag))

    def adds(self, objs): 
        for i in objs: self.add(*i)

    def get(self, name=None, tag=None, obj=None):
        rst = self.gets(name, tag, obj)
        return None if len(rst)==0 else rst[0][1]

    def gets(self, name=None, tag=None, obj=None):
        rst = [i for i in self.objs if name is None or name == i[0]]
        rst = [i for i in rst if obj is None or obj is i[1]]
        return [i for i in rst if tag is None or tag == i[2]]
        
    def has(self, name=None, tag=None, obj=None):
        return len(self.gets(name, tag, obj))>0
        
    def remove(self, name=None, tag=None, obj=None):
        for i in self.gets(name, tag, obj): self.objs.remove(i)

    def names(self, tag=None):
        return [i[0] for i in self.gets(tag=tag)]
        
    def name(self, name):
        names = self.names()
        if not name in names : return name
        for i in range(1, 100) : 
            n = "%s-%s"%(name, i)
            if not n in names: return n

    def write(self, path=None):
        with open(path or self.path, 'w') as f:
            f.write(json.dumps(self.objs))

    def read(self, path):
        self.path = path
        if not osp.exists(path): return
        with open(path) as f:
            self.adds(json.loads(f.read()))

class Source:
    managers = {}

    @classmethod
    def manager(cls, name):
        if not name in cls.managers: 
            cls.managers[name] = Manager()
        return cls.managers[name]

class App():
    def __init__(self):
        self.managers = {}
        self.img_manager = self.manager('img')
        self.wimg_manager = self.manager('wimg')
        self.tab_manager = self.manager('tab')
        self.wtab_manager = self.manager('wtab')
        self.mesh_manager = self.manager('mesh')
        self.wmesh_manager = self.manager('wmesh')
        self.task_manager = self.manager('task')
        self.plugin_manager = self.manager('plugin')

    def add_plugin(self, name, plg, tag=None):
        self.plugin_manager.add(name, plg, tag)

    def get_plugin(self, name=None):
        return self.plugin_manager.get(name)

    def plugin_names(self, tag=None):
        return self.plugin_manager.names(tag)

    def manager(self, name, value=None):
        if not name in self.managers: 
            self.managers[name] = Manager()
        return self.managers[name]

    def show_img(self, img): pass
    def show_table(self, img): pass
    def show_md(self, img, title=''): pass
    def show_txt(self, img, title=''): pass
    def show_plot(self): pass
    def show_mesh(self): pass

    def add_img(self, img):
        if not self.img_manager.has(img.name, obj=img):
            img.name = self.img_manager.name(img.name)
        self.img_manager.add(img.name, img)

    def remove_img(self, img):
        print('remove', img.name)
        self.img_manager.remove(obj=img)
        print(self.img_manager.objs, 'close')

    def add_img_win(self, win):
        self.wimg_manager.add(win.name, win)

    def remove_img_win(self, win):
        self.wimg_manager.remove(obj=win)
        
    def get_img(self, name=None):
        return self.img_manager.get(name)
    
    def get_img_name(self):
        return self.img_manager.names()
    
    def get_img_win(self, name=None):
        return self.wimg_manager.get(name)

    def add_tab(self, tab):
        if not self.tab_manager.has(tab.name, obj=tab):
            tab.name = self.tab_manager.name(tab.name)
        self.tab_manager.add(tab.name, tab)

    def remove_tab(self, tab):
        self.tab_manager.remove(obj=tab)

    def add_tab_win(self, win):
        self.wtab_manager.add(win.name, win)

    def remove_tab_win(self, win):
        self.wtab_manager.remove(obj=win)

    def get_tab(self, name=None):
        return self.tab_manager.get(name)
    
    def get_tab_name(self):
        return self.tab_manager.names()
    
    def get_tab_win(self, name=None):
        return self.wtab_manager.get(name)

    def add_mesh(self, mesh):
        if not self.mesh_manager.has(mesh.name, obj=mesh):
            mesh.name = self.mesh_manager.name(mesh.name)
        self.mesh_manager.add(mesh.name, mesh)

    def remove_mesh(self, mesh):
        self.mesh_manager.remove(obj=mesh)

    def add_mesh_win(self, win):
        self.wmesh_manager.add(win.name, win)

    def remove_mesh_win(self, win):
        self.wmesh_manager.remove(obj=win)

    def get_mesh(self, name=None):
        return self.mesh_manager.get(name)
    
    def get_mesh_name(self):
        return self.mesh_manager.names()
    
    def get_mesh_win(self, name=None):
        return self.wmesh_manager.get(name)

    def add_task(self, task):
        self.task_manager.add(task.title, task)

    def remove_task(self, task):
        self.task_manager.remove(obj=task)

    def info(self, value): 
        print('Information:', value)

    def show_md(self, cont, title='ImagePy'):
        print(title, '\n', cont)

    def show_txt(self, cont, title='ImagePy'):
        print(title, '\n', cont)

    def alert(self, cont, title='ImagePy'):
        print(title, '\n', cont, 'enter to continue!')
        input()

    def yes_no(self, cont, title='ImagePy'):
        print(title, '\n', cont, 'Y/N?')
        return input() in 'yY'

    def getpath(self, title, filt, io, name=''):
        print('input file path:')
        return input()
    
    def show_para(self, title, view, para, on_handle=None, on_ok=None, 
        on_cancel=None, on_help=None, preview=False, modal=True):
        print(title+':')
        for i in view:
            if i[0]==str: para[i[1]] = input(i[2]+': ? '+i[3]+' <str> ')
            if i[0]==int: para[i[1]] = int(input(i[4]+': ? '+i[5]+' <int> '))
            if i[0]==float: para[i[1]] = float(input(i[4]+': ? '+i[5]+' <float> '))
            if i[0]=='slide': para[i[1]] = float(input(i[4]+': ? '+i[5]+' <float> '))
            if i[0]==bool: para[i[1]] = bool(input(i[2]+': <True/False> '))
            if i[0]==list: para[i[1]] = i[3](input('%s %s: %s'%(i[4],i[5],i[2])+' <single choice> '))
            if i[0]=='chos':para[i[1]] = input('%s:%s <multi choices> '%(i[3],i[2])).split(',')
            if i[0]=='color': para[i[1]] = eval(input(i[2]+': ? '+i[3]+' <rgb> '))
        return para

    def run_macros(self, cmd, callafter=None):
        cmds = [i for i in cmd]
        def one(cmds, after): 
            cmd = cmds.pop(0)
            title, para = cmd.split('>')
            plg = self.manager('plugin').get(name=title)()
            after = lambda cmds=cmds: one(cmds, one)
            if len(cmds)==0: after = callafter
            plg.start(self, eval(para), after)
        one(cmds, None)

if __name__ == '__main__':
    app = App()
    app.alert('Hello, SciApp!')

    para = {'name':'yxdragon', 'age':10, 'h':1.72, 'w':70, 'sport':True, 'sys':'Mac', 'lan':['C/C++', 'Python'], 'c':(255,0,0)} 

    view = [('lab', 'lab', 'This is a questionnaire'),
            (str, 'name', 'name', 'please'), 
            (int, 'age', (0,150), 0, 'age', 'years old'),
            (float, 'h', (0.3, 2.5), 2, 'height', 'm'),
            ('slide', 'w', (1, 150), 0, 'weight','kg'),
            (bool, 'sport', 'do you like sport'),
            (list, 'sys', ['Windows','Mac','Linux'], str, 'favourite', 'system'),
            ('chos', 'lan', ['C/C++','Java','Python'], 'lanuage you like(multi)'),
            ('color', 'c', 'which', 'you like')]

    app.show_para('parameter', view, para)
