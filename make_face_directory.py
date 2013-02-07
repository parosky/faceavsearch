#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import shutil
import glob

# init of face detection variables
hc = cv2.cv.Load("./haarcascades/haarcascade_frontalface_alt.xml")
storage = cv2.cv.CreateMemStorage()

# remove temporary directories
print "remove temporary directories"
for directory in glob.glob('./face/tmp_*'):
    shutil.rmtree(directory)

# make save directory
if not os.path.exists('./face'):
    os.mkdir('face')

# make cid list for detection 
src_cids = set([f.split('/')[-1] for f in glob.glob('./img/*')])
face_cids = set([f.split('/')[-1] for f in glob.glob('./face/*')])
cids = src_cids - face_cids

# each cid
for cid in cids:
    # make temporary directory
    dir_temp = "./face/tmp_%s" % cid
    dir_save = "./face/%s" % cid
    os.mkdir(dir_temp)

    # get imagefile list
    filelist = glob.glob("./img/%s/*.jpg" % cid)

    # each imagefile
    for filename in filelist:
        print "detecting:", filename
        fn = filename.split('/')[-1]
        try:
            i = int(fn[fn.rindex('-')+1:fn.rindex('.')])
        except:
            i = 0

        # load and detect
        img = cv2.cv.LoadImage(filename)
        faces = cv2.cv.HaarDetectObjects(img, hc, storage, min_size=(50,50))
        
        # each face
        for j, face in enumerate(faces):
            # clip and save
            rect, n = face
            cv2.cv.SetImageROI(img, rect)
            cv2.cv.SaveImage("%s/%d-%d.jpg" % (dir_temp, i, j+1), img)
    
    # rename temporary directory
    os.rename(dir_temp, dir_save)


