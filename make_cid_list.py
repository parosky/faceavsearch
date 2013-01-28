#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import chardet
import urllib2
import time
import BeautifulSoup
import os

base_url = 'http://www.dmm.co.jp'
filename = 'data/cid.dat'
max_threads = 100
mutex = threading.Semaphore(1)
    
class MakerThread(threading.Thread):
    def __init__(self, url):
        self.url = url
        threading.Thread.__init__(self)

    def run(self):
        print self.url
        cids = []
        for i in range(1,1000):
            open_url = "%slimit=120/page=%d/" % (self.url, i)
            opened_url = urllib2.urlopen(open_url)
            if opened_url.url != open_url:
                break
            lines = opened_url.read()
            lines = unicode(lines, chardet.detect(lines)['encoding'])
            soup = BeautifulSoup.BeautifulSoup(lines)
            for s in soup(attrs={'class': 'tmb'}):
                video_url = "%s%s" % (base_url, s('a')[0]['href'])
                pos1 = video_url.index("cid=") + 4
                pos2 = video_url.index("/", pos1)
                cids.append(video_url[pos1:pos2])
    
        mutex.acquire()
        cids_saved = [line.strip() for line in open(filename)]
        cids_write = set(cids) - set(cids_saved)
        f = open(filename, 'a')
        for cid in cids_write:
            f.write('%s\n' % cid)
        f.close()
        mutex.release()    
        

class CharThread(threading.Thread):
    def __init__(self, consonant, vowel):
        # maker list page for specified HIRAGANA
        self.url = "%s/digital/videoa/-/maker/=/keyword=%s%s/" % (base_url, consonant, vowel)
        threading.Thread.__init__(self)

    def run(self):
        # get maker URL list
        lines = urllib2.urlopen(self.url).read()
        lines = unicode(lines, chardet.detect(lines)['encoding'])
        soup = BeautifulSoup.BeautifulSoup(lines)
        maker_url_list = ['%s%s' % (base_url, m('a')[0]['href']) for m in soup(attrs={'class': 'd-boxpicdata d-smalltmb'})]
        
        for maker_url in maker_url_list:    
            while True:
                time.sleep(10)
                if threading.activeCount() <= max_threads:
                    break
            t = MakerThread(maker_url)
            t.start()

if __name__ == "__main__":
    if not os.path.exists(filename):
        open(filename, 'a')

    # for each HIRAGANA
    for consonant in ['', 'k', 's', 't', 'n', 'h', 'm', 'y', 'r', 'w']:
        for vowel in ['a', 'i', 'u', 'e', 'o']:
            # get maker list and cids 
            t = CharThread(consonant, vowel)
            t.start()
            time.sleep(1)
