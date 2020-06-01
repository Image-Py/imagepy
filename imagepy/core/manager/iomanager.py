'''
class ReaderManager:
    reader = []

    @classmethod
    def add(cls, ext, read, tag='img', note=''):
        if isinstance(ext, str): ext = [ext]
        for i in ext:
            obj = (i, read, tag, note)
            if not obj in cls.reader: cls.reader.append(obj)
        
    @classmethod
    def get(cls, ext=None, tag=None, note=None):
        msk = [True for i in cls.reader]
        if not ext is None: 
            for i in range(len(msk)): msk[i] &= cls.reader[i][0]==ext
        if not tag is None:
            for i in range(len(msk)): msk[i] &= cls.reader[i][2]==tag
        if not note is None:
            for i in range(len(msk)): msk[i] &= cls.reader[i][3]==note
        return [cls.reader[i] for i in range(len(msk)) if msk[i]]

class WriterManager:
    writer = []
    
    @classmethod
    def add(cls, ext, read, tag='img', note=''):
        if isinstance(ext, str): ext = [ext]
        for i in ext:
            obj = (i, read, tag, note)
            if not obj in cls.writer: cls.writer.append(obj)
    
    @classmethod
    def get(cls, ext=None, tag=None, note=None):
        msk = [True for i in cls.writer]
        if not ext is None: 
            for i in range(len(msk)): msk[i] &= cls.writer[i][0]==ext
        if not tag is None:
            for i in range(len(msk)): msk[i] &= cls.writer[i][2]==tag
        if not note is None:
            for i in range(len(msk)): msk[i] &= cls.writer[i][3]==note
        return [cls.writer[i] for i in range(len(msk)) if msk[i]]
'''

from sciapp import Manager

ReaderManager = Manager()
WriterManager = Manager()