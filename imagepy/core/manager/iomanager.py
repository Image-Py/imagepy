class ReaderManager:
    reader = {}
    
    @classmethod
    def add(cls, ext, read, tag='img'):
        if not tag in cls.reader: cls.reader[tag] = {}
        if isinstance(ext, str):
            cls.reader[tag][ext.lower()] = read
            return
        for i in ext:
            cls.reader[tag][i.lower()] = read
        
    @classmethod
    def get(cls, ext=None, tag='img'):
        if ext is None and tag is None:
            ls = [cls.reader[i].keys() for i in cls.reader.keys()]
            return sorted([x for j in ls for x in j])
        elif ext is None and not tag is None:
            return sorted(cls.reader[tag].keys())
        elif not ext is None and tag is None:
            for i in cls.reader.values():
                if ext.lower() in i: return i[ext.lower()]
        elif not tag is None and not ext is None:
            if ext.lower() in cls.reader[tag]:
                return cls.reader[tag][ext.lower()]

class WriterManager:
    writer = {}
    
    @classmethod
    def add(cls, ext, write, tag='img'):
        if not tag in cls.writer: cls.writer[tag] = {}
        if isinstance(ext, str):
            cls.writer[tag][ext.lower()] = write
            return
        for i in ext:
            cls.writer[tag][i.lower()] = write
        
    @classmethod
    def get(cls, ext=None, tag='img'):
        if ext is None and tag is None:
            ls = [cls.writer[i].keys() for i in cls.writer.keys()]
            return sorted([x for j in ls for x in j])
        elif ext is None and not tag is None:
            return sorted(cls.writer[tag].keys())
        elif not ext is None and tag is None:
            for i in cls.writer.values():
                if ext.lower() in i: return i[ext.lower()]
        elif not tag is None and not ext is None:
            if ext.lower() in cls.writer[tag]:
                return cls.writer[tag][ext.lower()]

class ViewerManager:
    viewer = {}
    
    @classmethod
    def add(cls, ext, view):cls.viewer[ext.lower()] = view
        
    @classmethod
    def get(cls, ext='img'):
        for i in ReaderManager.reader:
            if ext.lower() in ReaderManager.reader[i]:
                return cls.viewer[i]