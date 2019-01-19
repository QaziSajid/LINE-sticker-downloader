import webbrowser
import sticker_dl as sd
import os
import subprocess as sp

def proper(s):
    p = ''.join(c for c in s if (c.isalnum() or c==' '))
    return p

source=open("numbers.txt", 'r')
ids=[]
#dest=open("links.txt", 'w')
for line in source:
    pid = line.strip()
    if pid not in ids:
        ids.append(pid)
source.close()

print("Downloading static stickers")
i=1
for pid in ids:
    print(i, "/", len(ids))
    i+=1
    sd.dwnl(pid, 0)
dirs = os.listdir()
if "_static" not in dirs:
    sp.call(["mkdir", "_static"])
for d in dirs:
    if (d[0]!='.' and '.py' not in d and d!='_animated' and d!='_static' and d!='__pycache__' and '.txt' not in d and '.sh' not in d):
        sp.call(['mv', d, '_static'])

print("Downloading animated stickers")
i=1
for pid in ids:
    print(i, "/", len(ids))
    i+=1
    sd.dwnl(pid, 1)
dirs = os.listdir()
if "_animated" not in dirs:
    sp.call(["mkdir", "_animated"])
for d in dirs:
    if (d[0]!='.' and '.py' not in d and d!='_animated' and d!='_static' and d!='__pycache__' and '.txt' not in d and '.sh' not in d):
        sp.call(['mv', d, '_animated'])

print("Converting animated stickers from apng to gif")
dirs = os.listdir('_animated')
for d in dirs:
    if d[0]!='.':
        files = os.listdir('_animated/'+d)
        for f in files:
            if "apng" in f:
                sp.call(["apng2gif", '_animated/'+d+"/"+f, '_animated/'+d+"/"+f[:-4]+"gif"])  
                sp.call(["mogrify", "-loop", "0", '_animated/'+d+"/"+f[:-4]+"gif"])
                sp.call(["rm", '_animated/'+d+"/"+f])
            
print("Do you want to split static packs at 30 limit? [y/n]")
c = input()
if(c=='y' or c=='Y'):
    dirs = os.listdir('_static')
    nf = 0
    for d in dirs:
        if d[0]!='.':
            files = os.listdir('_static/'+d)
            nf = len(files)
            if (nf>30):
                sd = proper(d)+"extra"
                print("extras exist in ", d)
                sp.call(["mkdir", '_static/'+d+"/"+sd])
                #print("directory made")
                for i in range (30, nf):
                    f = files[i]
                    sp.call(["mv", '_static/'+d+'/'+f, '_static/'+d+'/'+sd])
            #print ("moved")
