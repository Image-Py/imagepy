import json, os.path as osp

class Manager:
    def __init__(self, unique=True, path=None):
        self.objs, self.unique, self.path = [], unique, path
        if not path is None: self.read(path)

    def add(self, name, obj, tag=None):
        if self.unique: self.remove(name, tag)
        self.objs.insert(0, (name, obj, tag))

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