#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os.path
import shutil

if __name__ == "__main__":
    cids = set([f.split('/')[-1] for f in glob.glob('./img/*')])
    for cid in cids:
        if 'tmp_' in cid:
            continue
        filenames = glob.glob('./img/%s/*.jpg' % cid)
        is_del = False
        for filename in filenames:
            if os.path.getsize(filename) == 2732:
                is_del = True
                break
        if is_del:
            shutil.rmtree('./img/%s' % cid)
            print 'removed:', cid
