class OpenerManager:
    opener = {}
    
    @classmethod
    def add(cls, ext, read, show=None):cls.opener[ext] = read, show
        
    @classmethod
    def get(cls, ext):
    	if not ext in cls.opener:
    		return None
    	return cls.opener[ext]

    @classmethod
    def all(cls):return sorted(cls.opener.keys())