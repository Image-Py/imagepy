# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 23:45:59 2017

@author: yxl
"""
import os, sys
from ..engine import Macros, MkDown, Widget, WorkFlow, Report
from ..manager import ToolsManager, PluginsManager, WidgetsManager, DocumentManager
from ... import IPy, root_dir
from codecs import open

def getpath(root, path):
    for i in range(10,0,-1):
        if not '../'*i in path: continue
        s = root
        for j in range(i):s=os.path.dirname(s)
        path = path.replace('../'*i, s+'/')
    return path.replace('\\\\','\\').replace('\\','/')

def extend_plugins(path, lst, err):
    rst = []
    for i in lst:
        if isinstance(i, tuple) or i=='-': 
            rst.append(i)
        elif i[-3:] == 'rpt':
            pt = os.path.join(root_dir,path)
            print(pt+'/'+i)
            rst.append(Report(i[:-4], pt+'/'+i))
            PluginsManager.add(rst[-1])
        elif i[-3:] == '.mc':
            pt = os.path.join(root_dir, path)
            f = open(pt+'/'+i, 'r', 'utf-8')
            cmds = f.readlines()
            f.close()
            rst.append(Macros(i[:-3], [getpath(pt, i) for i in cmds]))
            PluginsManager.add(rst[-1])
        elif i[-3:] == '.wf':
            pt = os.path.join(root_dir,path)
            f = open(pt+'/'+i, 'r', 'utf-8')
            cmds = f.read()
            f.close()
            rst.append(WorkFlow(i[:-3], cmds))
            PluginsManager.add(rst[-1])
        elif i[-3:] == '.md':
            f = open(os.path.join(root_dir,path)+'/'+i, 'r', 'utf-8')
            cont = f.read()
            f.close()
            rst.append(MkDown(i[:-3], cont))
            PluginsManager.add(rst[-1])
        elif i[-6:] in ['wgt.py', 'gts.py']:
            try:
                rpath = path.replace('/', '.').replace('\\','.')
                #rpath = rpath[rpath.index('imagepy.'):]
                plg = __import__('imagepy.'+ rpath+'.'+i[:-3],'','',[''])
                if hasattr(plg, 'wgts'):
                    rst.extend([j if j=='-' else Widget(j) for j in plg.wgts])
                    for p in plg.wgts:
                        if not isinstance(p, str):WidgetsManager.add(p)
                else: 
                    rst.append(Widget(plg.Plugin))
                    WidgetsManager.add(plg.Plugin)
            except Exception as  e:
                err.append((path, i, sys.exc_info()[1]))
        else:
            try:
                rpath = path.replace('/', '.').replace('\\','.')
                #rpath = rpath[rpath.index('imagepy.'):]
                plg = __import__('imagepy.'+ rpath+'.'+i[:-3],'','',[''])
                if hasattr(plg, 'plgs'):
                    rst.extend([j for j in plg.plgs])
                    for p in plg.plgs:
                        if not isinstance(p, str):PluginsManager.add(p)
                else: 
                    rst.append(plg.Plugin)
                    PluginsManager.add(plg.Plugin)
            except Exception as  e:
                err.append((path, i, sys.exc_info()[1]))

    return rst
            
def sort_plugins(catlog, lst):
    rst = []
    for i in catlog:
        if i=='-':rst.append('-')
        for j in lst:
            if j[:-3]==i or j[:-4]==i or j[0].title==i:
                lst.remove(j)
                rst.append(j)
    rst.extend(lst)
    return rst
        
def build_plugins(path, err=False):
    root = err in (True, False)
    if root: sta, err = err, []
    subtree = []
    cont = os.listdir(os.path.join(root_dir, path))
    for i in cont:
        subp = os.path.join(path,i)
        if os.path.isdir(os.path.join(root_dir, subp)):
            sub = build_plugins(subp, err)
            if len(sub)!=0:subtree.append(sub)
        elif i[-6:] in ('plg.py', 'lgs.py', 'wgt.py', 'gts.py'):
            subtree.append(i)
        elif i[-3:] in ('.mc', '.md', '.wf', 'rpt'):
            subtree.append(i)
    if len(subtree)==0:return []
    
    rpath = path.replace('/', '.').replace('\\','.')
    #rpath = rpath[rpath.index('imagepy.'):]
    pg = __import__('imagepy.'+rpath,'','',[''])
    pg.title = os.path.basename(path)
    if hasattr(pg, 'catlog'):
        if 'Personal Information' in pg.catlog:
            print(subtree)
        subtree = sort_plugins(pg.catlog, subtree)
    subtree = extend_plugins(path, subtree, err)
    
    if root and sta and len(err)>0:
        IPy.write('Some plugin may be not loaded, but not affect others!')
        for i in err: IPy.write('>>> %-50s%-20s%s'%i)
    return (pg, subtree)  
    
def extend_tools(path, lst, err):
    rst = []
    for i in lst:
        if i[-3:] in ('.mc', '.md', '.wf', 'rpt'):
            pt = os.path.join(root_dir, path)
            # if i[-3:] == '.md':print(pt)
            f = open(pt+'/'+i)
            cmds = f.readlines()
            f.close()
            rst.append((Macros(i[:-3], [getpath(pt, i) for i in cmds]),  
                os.path.join(root_dir, path)+'/'+i[:-3]+'.gif'))
        else:
            try:
                rpath = path.replace('/', '.').replace('\\','.')
                #rpath = rpath[rpath.index('imagepy.'):]
                
                plg = __import__('imagepy.'+rpath+'.'+i,'','',[''])
                if hasattr(plg, 'plgs'): 
                    for i,j in plg.plgs: rst.append((i, path+'/'+j))
                else: rst.append((plg.Plugin, 
                    os.path.join(root_dir, path)+'/'+i.split('_')[0]+'.gif'))
            except Exception as e:
                err.append((path, i, sys.exc_info()[1]))
    for i in rst:ToolsManager.add(i[0])
    return rst
            
def sort_tools(catlog, lst):
    rst = []
    for i in catlog:
        if i=='-':rst.append('-')
        for j in lst:
            if j==i or j[0].title==i or j[:-3]==i:
                lst.remove(j)
                rst.append(j)
    rst.extend(lst)
    return rst
    
def build_tools(path, err=False):
    root = err in (True, False)
    if root: sta, err = err, []
    subtree = []
    cont = os.listdir(os.path.join(root_dir, path))

    for i in cont:
        subp = os.path.join(path,i)
        if root and os.path.isdir(os.path.join(root_dir, subp)):
            sub = build_tools(subp, err)
            if len(sub)!=0:subtree.append(sub)
        elif not root:
            if i[len(i)-7:] in ('_tol.py', 'tols.py'):
                subtree.append(i[:-3])
            elif i[-3:] in ('.mc', '.md', '.wf', 'rpt'):
                subtree.append(i)
    if len(subtree)==0:return []
    rpath = path.replace('/', '.').replace('\\','.')
    #rpath = rpath[rpath.index('imagepy.'):]
    pg = __import__('imagepy.' + rpath,'','',[''])
    pg.title = os.path.basename(path)
    if hasattr(pg, 'catlog'):
        subtree = sort_tools(pg.catlog, subtree)
    if not root:subtree = extend_tools(path, subtree, err)    
    elif sta and len(err)>0: 
        IPy.write('tools not loaded:')
        for i in err: IPy.write('>>> %-50s%-20s%s'%i)
    return (pg, subtree)
    
def extend_widgets(path, lst, err):
    rst = []
    for i in lst:
        try:
            rpath = path.replace('/', '.').replace('\\','.')
            #rpath = rpath[rpath.index('imagepy.'):]
            plg = __import__('imagepy.'+rpath+'.'+i,'','',[''])
            rst.append(plg.Plugin)
        except Exception as e:
            err.append((path, i, sys.exc_info()[1]))
    for i in rst:WidgetsManager.add(i)
    return rst
            
def sort_widgets(catlog, lst):
    rst = []
    for i in catlog:
        if i=='-':rst.append('-')
        for j in lst:
            if j==i or j[:-3]==i or j[0].title==i:
                lst.remove(j)
                rst.append(j)
    rst.extend(lst)
    return rst
    
def build_widgets(path, err=False):
    root = err in (True, False)
    if root: sta, err = err, []
    subtree = []
    cont = os.listdir(os.path.join(root_dir, path))
    for i in cont:
        subp = os.path.join(path,i)
        if root and os.path.isdir(os.path.join(root_dir, subp)):
            sub = build_widgets(subp, err)
            if len(sub)!=0:subtree.append(sub)
        elif not root:
            if i[len(i)-7:] in ('_wgt.py', 'wgts.py'):
                subtree.append(i[:-3])
                #print('====', subtree)
    if len(subtree)==0:return []
    rpath = path.replace('/', '.').replace('\\','.')
    #rpath = rpath[rpath.index('imagepy.'):]
    pg = __import__('imagepy.' + rpath,'','',[''])
    pg.title = os.path.basename(path)
    if hasattr(pg, 'catlog'):
        subtree = sort_widgets(pg.catlog, subtree)
    if not root:
        subtree = extend_widgets(path, subtree, err)  
    elif sta and len(err)>0: 
        IPy.write('widgets not loaded:')
        for i in err: IPy.write('>>> %-50s%-20s%s'%i)
    return (pg, subtree)

def build_document(path):
    docs = []
    for dirpath,dirnames,filenames in os.walk(path):
        for filename in filenames:
            if filename[-3:] != '.md': continue
            docs.append(os.path.join(dirpath, filename))
            f = open(docs[-1], encoding='utf-8')
            cont = f.read()
            f.close()
            DocumentManager.add(filename[:-3], cont)
    return docs

if __name__ == "__main__":
    print (os.getcwd())
    os.chdir('../../')
    data = build_tools('tools')
