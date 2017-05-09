# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 23:45:59 2017
@author: yxl
"""
import IPy
import IPyGL
import os,sys
from core.engines import Macros
from core.managers import ToolsManager,PluginsManager

first = [0,0]
def _preprocess_path(currpath):
    """
    currpath,rpath = _preprocess_path(currpath)
    """
    rootpath = IPyGL.root_dir
    currpath = currpath.replace(".",os.path.sep)
    if not os.path.exists(currpath):
        currpath = os.path.join(IPyGL.root_dir,currpath)    

    rpath = currpath[len(rootpath):] if currpath.startswith(rootpath) else currpath 
    # Replace path.sep("/","\\") with "."
    rpath = rpath.replace('/', '.').replace('\\','.')   
    # To successcful call __import__() function, remove the first "." 
    rpath = rpath[1:] if rpath[0]=="." else rpath         

    return currpath, rpath


def build_plugins(currpath, err=None,level = 1):
    #TODO: what is the error?
    root = err==None
    if err==None: err = []
    subtree = []

    currpath,rpath = _preprocess_path(currpath)
    paths = os.listdir(currpath)
    for ipath in paths:
        subp = os.path.join(currpath,ipath)
        if os.path.isdir(subp):
            sub = build_plugins(subp, err,level+1)
            if len(sub)!=0:
                subtree.append(sub)
        elif ipath[-6:] in ('plg.py', 'lgs.py') or ipath[-3:]==".mc":
            subtree.append(ipath)

    # return subtree
    if len(subtree)==0:
        return []

    #print("subtree=\n{}".format(subtree)   )
    pg = __import__(rpath,'','',[''])
    pg.title = os.path.basename(currpath)
    if hasattr(pg, 'catlog'):
        subtree = sort_plugins(pg.catlog, subtree)
    subtree = extend_plugins(currpath, subtree, err)

    if first[0]==0 and root and len(err)>0:
        IPy.write('some plugin may be not loaded, but not affect otheres!')
        for e in err: IPy.write('>>> %-50s%-20s%s'%e)
    if root : first[0]=1
    return (pg, subtree)


def extend_plugins(currpath, lst, err):
    rst = []
    currpath,rpath = _preprocess_path(currpath)

    # ======================================================
    for item in lst:
        if isinstance(item, tuple) or item=='-':
            rst.append(item)
        elif item[-3:]=='.mc':
            with open(os.path.join(currpath,item)) as f:
                cmds = f.readlines()
                #print(cmds)
                rst.append(Macros(item[:-3], cmds))
        else:
            try:
                #!TODO:Fixme!
                # importlib.import_module()
                plg = __import__(rpath+'.'+item[:-3],'','',[''])
                if hasattr(plg, 'plgs'):
                    rst.extend([x for x in plg.plgs])
                    for x in plg.plgs:
                        if not isinstance(x, str):
                            PluginsManager.add(x)
                else:
                    rst.append(plg.Plugin)
                    PluginsManager.add(plg.Plugin)
            except Exception as e:
                err.append((currpath, item, sys.exc_info()[1]))

    return rst

def sort_plugins(catlogs, lst):
    rst = []
    for catlog in catlogs:
        if catlog=='-':
            rst.append('-')
        for item in lst:
            if item[:-3] == catlog or item[0].title == catlog:
                lst.remove(item)
                rst.append(item)
    rst.extend(lst)
    return rst

def build_tools(currpath, err=None,level=1):
    root = err==None
    if err==None:err=[]
    subtree = []
    
    currpath,rpath = _preprocess_path(currpath)
    
    #!Todo: Get all the "*plg.py","*lgs.py","*.mc" and the path into the subtree!
    paths = os.listdir(currpath)
    for ipath in paths:
        subp = os.path.join(currpath,ipath)
        if root and os.path.isdir(subp):
            sub = build_tools(subp, err,level+1)
            if len(sub)!=0:
                subtree.append(sub)
        elif not root:
            if ipath[-7:] in ('_tol.py', 'tols.py'):
                subtree.append(ipath[:-3])
            elif ipath[-3:]==".mc":
                subtree.append(ipath)

    # return subtree
    if len(subtree)==0:
        return []

    pg = __import__(rpath,'','',[''])
    pg.title = os.path.basename(currpath)
    if hasattr(pg, 'catlog'):
        subtree = sort_tools(pg.catlog, subtree)
    if not root:
        subtree = extend_tools(currpath, subtree, err)
    elif first[1]==0 and len(err)>0:
        IPy.write('tools not loaded:')
        for e in err: IPy.write('>>> %-50s%-20s%s'%e)
    if root :
        first[1]=1
    return (pg, subtree)

def extend_tools(currpath, lst, err):
    currpath,rpath = _preprocess_path(currpath)

    rst = []
    for item in lst:
        if item[-3:]=='.mc':
            with open(os.path.join(currpath,item)) as f:
                cmds = f.readlines()
                rst.append((Macros(item[:-3], cmds),  os.path.join(currpath,item[:-3]+'.gif')))
        else:
            try:
                plg = __import__(rpath+'.'+item,'','',[''])
                if hasattr(plg, 'plgs'):
                    for k,v in plg.plgs:
                        rst.append((k,  os.path.join(currpath,v)))
                else:
                    rst.append((plg.Plugin,os.path.join(currpath,item.split('_')[0]+'.gif')) )
            except Exception as e:
                err.append((currpath, item, sys.exc_info()[1]))
    #! Todo: Fixme!
    for item in rst:
        ToolsManager.add(item[0])
    return rst

def sort_tools(catlogs, lst):
    rst = []
    for catlog in catlogs:
        if catlog=='-':rst.append('-')
        for item in lst:
            if item==catlog or item[0].title==catlog or item[:-3]==catlog:
                lst.remove(item)
                rst.append(item)
    rst.extend(lst)
    return rst


if __name__ == "__main__":
    print(os.getcwd())
    # os.chdir('../../')
    os.chdir("/home/auss/Programs/Python/ImagePy/imagepy3/")
    data = build_tools('tools')
    print(data)
