class DocumentManager:
    docs = {}
        
    @classmethod
    def add(cls, name, cont):cls.docs[name] = cont
        
    @classmethod
    def get(cls, name=None):
        if not name in cls.docs: 
            return '# Sorry, No Document yet.'
        return cls.docs[name]