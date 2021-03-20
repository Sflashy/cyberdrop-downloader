#
# * S-Name:		cyberdrop-downloader
# * Author:		Sflashy#7643 - sflashy@mail.com
# * Date:		01/08/2021
#

import re, sys, os
from datetime import datetime
from multiprocessing.pool import ThreadPool
from uuid import uuid4
import argparse
try:
    import requests
except:
    os.system('pip install requests')
    sys.exit(f'{str(datetime.now())[:-7]} INFO Please run the it again!')

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description='CyberDrop Downloader')
parser.add_argument('-u', '--url', default=None)
parser.add_argument('-d', '--directory', default=None)
parser.add_argument('-f', '--folder', default=None)

class CyberDrop:
    THREADS = 100
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}
    ARGS = parser.parse_args()

    def __init__(self):
        print(f'{str(datetime.now())[:-7]} INFO Initializing...')
        self.session = requests.session()
        self.imageList = []
        self.directory = './downloads'
        self.checkdir()
        self.fetchImages()

    def fetchImages(self):
        print(f'{str(datetime.now())[:-7]} INFO Fetching images...')
        url = self.ARGS.url
        if 'http' not in url:
            url = 'https://cyberdrop.me/a/' + url
        htmlResponse = self.session.get(url, headers=self.HEADERS)
        if htmlResponse.status_code == 200:
            for image in re.findall(r'<a class="image" href="(.*?)" target="_blank"', htmlResponse.text):
                self.imageList.append(image)
        else:
            print(f'{str(datetime.now())[:-7]} ERROR Album not found or server is unreachable [{htmlResponse.status_code}]')

    def checkdir(self):
        if self.ARGS.directory:
            self.directory = self.ARGS.directory
            if not os.path.exists(self.directory): os.mkdir(self.directory)

        if self.ARGS.folder:
            if not self.ARGS.directory:
                if not os.path.exists(self.directory): os.mkdir(self.directory)
            self.directory = self.directory + '/' + self.ARGS.folder
            if not os.path.exists(self.directory): os.mkdir(self.directory)

        if not self.ARGS.directory and not self.ARGS.folder:
            if not os.path.exists(self.directory): os.mkdir(self.directory)
            
    def downloadImages(self, url):
        fileExt = re.search(r'(\.mp4|.mov|\.m4v|\.ts|\.mkv|\.avi|\.wmv|\.webm|\.vob|\.gifv|\.mpg|\.mpeg|\.mp3|\.flac|\.wav|\.png|\.jpeg|\.jpg|\.gif|\.bmp|\.webp|\.heif|\.tiff|\.svf|\.svg|\.ico|\.psd|\.ai|\.pdf|\.txt|\.log|\.csv|\.xml|\.cbr|\.zip|\.rar|\.7z|\.tar|\.gz|\.iso|\.torrent|\.kdbx)', url).group(1)
        fileName = uuid4().hex
        while True:
            try:
                print(f'{str(datetime.now())[:-7]} INFO Downloading: {fileName}{fileExt}            ', end='\r')
                with open(f'{self.directory}/{fileName}{fileExt}', 'wb') as f:
                    f.write(self.session.get(url).content)
                    break
            except:
                print(f'{str(datetime.now())[:-7]} INFO RETRY: {fileName}{fileExt}  ', end='\r')

cyberdrop = CyberDrop()
_ = [_ for _ in ThreadPool(cyberdrop.THREADS).imap_unordered(cyberdrop.downloadImages, cyberdrop.imageList)]
