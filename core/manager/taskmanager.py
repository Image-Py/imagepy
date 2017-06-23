class TaskManager:
    tasks = {}
    
    @classmethod
    def add(cls, key):
        cls.tasks[key] = 1
        
    @classmethod
    def remove(cls, key):
        cls.tasks.pop(key)

    @classmethod
    def get(cls, key=None):
        if key==None:return cls.tasks
        return cls.tasks[key]