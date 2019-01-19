import os

def get_docs(path):
    docs = []
    for dirpath,dirnames,filenames in os.walk(path):
        for filename in filenames:
            docs.append(os.path.join(dirpath,filename))
    return [i for i in docs if i[-3:] == '.md']

print(get_docs('./'))
