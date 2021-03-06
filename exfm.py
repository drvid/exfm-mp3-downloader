try:
    import simplejson as json
except ImportError:
    import json
import re, sys, time, urllib, urllib2

class ExfmError(Exception):
    pass

class ExfmDownloader(object):
    def _request(self, route, data):
        url = "http://ex.fm/api/v3%s" % route
        data = urllib.urlencode(data, True)
        headers = {'User-Agent': 'exfm API Python Client'}
        try:
            url += '?' + data
            req = urllib2.Request(url, headers=headers)
            response_data = urllib2.urlopen(req).read()
            data = json.loads(response_data)
            if data['status_code'] != 200:
                raise ExfmError(data['status_text'])
            return self.downloader(data)
        except urllib2.HTTPError, e:
            return e.read()
        except urllib2.URLError, e:
            return str(e)

    def reporthook(self, count, blockSize, totalSize):
        if count == 0:
            self.startTime= time.time()      #use self instead of declaring a global variable inside classes
            return
        duration = time.time() - self.startTime
        progressSize = int(count*blockSize)
        speed = int(progressSize / (1024 * duration ))
        percent = int(count*blockSize*100/totalSize)
        sys.stdout.write("----------------------------")
        sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" % (percent,progressSize/(1024*1024),speed, duration ))
        sys.stdout.flush()

    def downloader(self, data):
        songs = data['songs']
        for song in songs:
            if 'api.soundcloud.com' in  song['url']:
                song['url'] +=  '?consumer_key=leL50hzZ1H8tAdKCLSCnw'
            print "\r--------------------------------------------------------------------"
            print "\r"+song['title']
            urllib.urlretrieve(song['url'], song['title']+'.mp3', self.reporthook)
        print ''                     # Prevents Download completed!' line from merging to the download bar
        print 'Download completed!'

    def get_user_loved(self, username='solancer', start=0, results=1000):
        return self._request("/user/%s/loved" % username, 
                              data={'start': start, 'results': results})
