#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import urllib2
import chardet
import BeautifulSoup
import codecs

if __name__ == '__main__':
    filename = "./data/title.dat"
    cids = [line.strip() for line in open('./data/cid.dat')]
    if os.path.exists(filename):
        cids_saved = [line.strip()[:line.index(',')] for line in open(filename)]
    else:
        cids_saved = []
    print cids_saved
    for cid in set(cids)-set(cids_saved):
        url = "http://www.dmm.co.jp/digital/videoa/-/detail/=/cid=%s/" % cid
        try:
            lines = urllib2.urlopen(url).read()
            lines = unicode(lines, chardet.detect(lines)['encoding'], 'ignore')
            soup = BeautifulSoup.BeautifulSoup(lines)
            title = soup(attrs={'class': 'tdmm'})[0]['alt']
        except urllib2.URLError as e:
            if e.code == 404:
                print "404:", url
                title = ""
        codecs.open(filename, 'a', 'utf-8').write('%s,%s\n' % (cid, title))
