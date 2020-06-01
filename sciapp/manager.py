class Manager:
    def __init__(self, unique=True, path=None):
        self.objs, self.unique, self.path = [], unique, path
        if not path is None: self.read(path)

    def add(self, name, obj, tag=None):
        if self.unique: self.remove(name, tag, obj)
        self.objs.insert(0, (name, obj, tag))

    def adds(self, objs): for i in objs: self.add(*i)

    def get(self, name=None, tag=None, obj=None):
        rst = self.filter(name, tag, obj)
        return None if len(rst)==0 else rst[0]

    def filter(self, name=None, tag=None, obj=None):
        rst = [i for i in self.objs if name is None or name = i[0]]
        rst = [i for i in self.objs if obj is None or obj = i[1]]
        return [i for i in self.objs if tag is None or tag = i[2]]
        
    def gets(self, name=None, tag=None):
        return self.filter(name, tag)

    def has(self, name=None, tag=None, obj=None):
        return len(self.filter(name, tag, obj))>0
        
    def remove(self, name=None, tag=None, obj=None):
        for i in self.filter(name, tag, obj): self.objs.remove(i)

    def names(self, tag=None):
        return [i[0] for i in self.filter(tag=tag)]
        
    def name(self, name, obj=None):
        names = self.names()
        if not name in names : return name
        for i in range(1, 100) : 
            n = "%s-%s"%(name, i)
            if not n in names: return n

    def write(self, path=None):
        with open(path or self.path, 'w') as f:
            f.write(json.dumps(self.objs))

    def read(self, path):
        if not osp.exists(path): return
        self.path = path
        with open(path) as f:
            self.adds(json.loads(f.read()))
