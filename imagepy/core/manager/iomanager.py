class ReaderManager:
    reader = {}
    
    @classmethod
    def add(cls, ext, read):cls.reader[ext.lower()] = read
        
    @classmethod
    def get(cls, ext):
    	if not ext.lower() in cls.reader:
    		return None
    	return cls.reader[ext.lower()]

    @classmethod
    def all(cls):return sorted(cls.reader.keys())

class WriterManager:
    writer = {}
    
    @classmethod
    def add(cls, ext, write):cls.writer[ext.lower()] = write
        
    @classmethod
    def get(cls, ext):
        if not ext.lower() in cls.writer:
            return None
        return cls.writer[ext.lower()]

    @classmethod
    def all(cls):return sorted(cls.writer.keys())

class ViewerManager:
    viewer = {}
    
    @classmethod
    def add(cls, ext, view):cls.viewer[ext.lower()] = view
        
    @classmethod
    def get(cls, ext):
        if not ext.lower() in cls.viewer:
            return None
        return cls.viewer[ext.lower()]

    @classmethod
    def all(cls):return sorted(cls.viewer.keys())