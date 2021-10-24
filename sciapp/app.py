from .manager import Manager
from .object import Image, Table, Scene

class App():
    def __init__(self, asyn=True):
        self.asyn = asyn
        self.managers = {}
        self.img_manager = self.manager('img')
        #self.wimg_manager = self.manager('wimg')
        self.tab_manager = self.manager('tab')
        #self.wtab_manager = self.manager('wtab')
        self.mesh_manager = self.manager('mesh')
        self.wmesh_manager = self.manager('wmesh')
        self.task_manager = self.manager('task')
        
        self.plugin_manager = self.manager('plugin')

    def manager(self, name, value=None):
        if not name in self.managers: 
            self.managers[name] = Manager()
        return self.managers[name]

    # ========== Plugin ==========
    def add_plugin(self, name, plg, tag=None):
        self.plugin_manager.add(name, plg, tag)
        for i in ' _.-': name = name.replace(i,'_')
        self.__dict__['_%s_'%name] = plg

    def get_plugin(self, name=None):
        return self.plugin_manager.get(name)

    def plugin_names(self, tag=None):
        return self.plugin_manager.names(tag)

    # ========== Image ==========
    def show_img(self, img, name): 
        if not isinstance(img, Image): 
            img = Image(img, name)
        img.name = self.img_manager.name(name)
        self.img_manager.add(img.name, img)
        print(img.info)

    #def add_img_win(self, win, name):
    #    self.wimg_manager.add(name, win)

    def close_img(self, name): 
        self.img_manager.remove(name)
        print('close image:', name)

    def active_img(self, name): 
        self.img_manager.active(name)
        print('active image:', name)

    def get_img(self, name=None):
        return self.img_manager.get(name)

    def img_names(self):
        return self.img_manager.names()

    # ========== Table ==========
    def show_table(self, tab, name): 
        if not isinstance(tab, Table): 
            tab = Table(tab, name)
        tab.name = self.tab_manager.name(name)
        self.tab_manager.add(tab.name, tab)
        print(tab.info)

    def close_table(self, name): 
        self.tab_manager.remove(name)
        print('close table:', name)

    def active_table(self, name): 
        self.tab_manager.active(name)
        print('active image:', name)

    def get_table(self, name=None):
        return self.tab_manager.get(name)

    def table_names(self):
        return self.tab_manager.names()

    # ========== Others ==========
    def show_plot(self): pass

    def show_mesh(self, mesh, name):
        mesh.name = self.mesh_manager.name(name)
        self.mesh_manager.add(mesh.name, mesh)

    def active_mesh(self, name): 
        self.mesh_manager.active(name)
        print('active mesh:', name)

    def close_mesh(self, name):
        self.mesh_manager.remove(name)

    #def add_mesh_win(self, win):
    #    self.wmesh_manager.add(win.name, win)

    #def remove_mesh_win(self, win):
    #    self.wmesh_manager.remove(obj=win)

    def get_mesh(self, name=None):
        return self.mesh_manager.get(name)
    
    def get_mesh_name(self):
        return self.mesh_manager.names()
    
    #def get_mesh_win(self, name=None):
    #    return self.wmesh_manager.get(name)

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

    def get_path(self, title='sciapp', filt='', io='save', name=''):
        print('input file path:')
        return input()
    
    def show_para(self, title, para, view, on_handle=None, on_ok=None, 
        on_cancel=None, on_help=None, preview=False, modal=True):
        for i in view:
            if i[0]==str: para[i[1]] = input(i[2]+': ? '+i[3]+' <str> ')
            if i[0]==int: para[i[1]] = int(input(i[4]+': ? '+i[5]+' <int> '))
            if i[0]==float: para[i[1]] = float(input(i[4]+': ? '+i[5]+' <float> '))
            if i[0]=='slide': para[i[1]] = float(input(i[4]+': ? <float> '))
            if i[0]==bool: para[i[1]] = bool(input(i[2]+': <True/False> '))
            if i[0]==list: para[i[1]] = i[3](input('%s %s: %s'%(i[4],i[5],i[2])+' <single choice> '))
            if i[0]=='chos':para[i[1]] = input('%s:%s <multi choices> '%(i[3],i[2])).split(',')
            if i[0]=='color': para[i[1]] = eval(input(i[2]+': ? '+i[3]+' <rgb> '))
        return para

    def run_macros(self, cmd, callafter=None):
        cmds = [i for i in cmd]
        def one(cmds, after): 
            cmd = cmds.pop(0)
            if not isinstance(cmd, str): title, para = cmd
            else: title, para = eval('"'+cmd.replace('>', '",'))
            plg = self.plugin_manager.get(name=title)()
            after = lambda cmds=cmds: one(cmds, one)
            if len(cmds)==0: after = callafter
            plg.start(self, para, after)
        one(cmds, None)

    def show(self, tag, cont, title):
        tag = tag or 'img'
        if tag=='img':
            self.show_img([cont], title)
        elif tag=='imgs':
            self.show_img(cont, title)
        elif tag=='tab':
            self.show_table(cont, title)
        elif tag=='mc':
            self.run_macros(cont)
        elif tag=='md':
            self.show_md(cont, title)
        elif tag=='wf':
            self.show_workflow(cont, title)
        else: self.alert('no view for %s!'%tag)

    def record_macros(self, cmd):
        print('>>>', cmd)