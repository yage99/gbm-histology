
import shutil
import os

f = open('TCGAMaxim/clinical.csv')
for line in f:
    id, time = line.split(',')
    if os.path.exists(os.path.join("/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/svs-selected", id)):
        shutil.copytree(os.path.join("/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/svs-selected", id), os.path.join("/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/svs-hasclinical/", id))
    else:
        print "warn: %s not exist" % id
