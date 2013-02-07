#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import shutil
import threading
import os
import urllib
import urllib2
import chardet
import BeautifulSoup
import time

base_url = 'http://www.dmm.co.jp'
max_threads = 50

class DownloadThread(threading.Thread):
    def __init__(self, cid):
        self.cid = cid
        self.url = "http://www.dmm.co.jp/digital/videoa/-/detail/=/cid=%s/" % cid
        threading.Thread.__init__(self)

    def run(self):
        directory = "./img/%s" % cid
        directory_temp = "./img/tmp_%s" % cid
      
        os.mkdir(directory_temp)

        # get image filename
        while True:
            try:
                lines = urllib2.urlopen(self.url).read()
                lines = unicode(lines, chardet.detect(lines)['encoding'], 'ignore')
                break
            except urllib2.URLError as e:
                if e.code == 404:
                    print "404:", self.url
                    os.rename(directory_temp, directory)
                    return
                else:
                    print "download error"
                    time.sleep(10)

        # no sample
        if u"拡大表示されません" in lines:
            print "no image", self.url
            os.rename(directory_temp, directory)
            return
         
        soup = BeautifulSoup.BeautifulSoup(lines)
        img_urls = []

        # package
        try:
            img_urls.append(soup(attrs={'name': 'package-image'})[0]['href'])
        except:
            print "package errpr:", self.url

        # sample
        s4 = soup(attrs={'id': 'sample-image-block'})
        if len(s4) != 0:
            img_urls += [s3['src'].replace('-', 'jp-') for s3 in s4[0]('img')]
            
        for img_url in img_urls:
            filename = img_url[img_url.rindex("/")+1:]
            print img_url
            
            while True:
                try:
                    urllib.urlretrieve( img_url, "%s/%s" % (directory_temp, filename))
                    break
                except:
                    print "download error:", img_url
                    time.sleep(10)

        os.rename(directory_temp, directory)


if __name__ == '__main__':
    print "remove temp directories"
    for directory in glob.glob('./img/tmp_*'):
        shutil.rmtree(directory)

    for line in open('data/cid.dat'):
        cid = line.strip()

        # check exists
        if os.path.exists("./img/%s" % cid) or os.path.exists("./img/tmp_%s" % cid):
            continue
       
        while True:
            if threading.activeCount() <= max_threads:
                t = DownloadThread(cid)
                t.start()
                time.sleep(1)
                break
            time.sleep(1)
