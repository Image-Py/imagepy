class Macros:
    def __init__(self, title, cmds):
        self.title = title
        self.cmds = cmds
        
    def __call__(self): return self
        
    def start(self, app, para=None, callafter=None):
        app.run_macros(self.cmds, callafter)