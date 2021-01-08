#
# * S-Name:		cyberdrop-downloader
# * Author:		Sflashy#7643 - sflashy@mail.com
# * Date:		01/08/2021
#

import re, sys, os
from datetime import datetime
from multiprocessing.pool import ThreadPool
from uuid import uuid4
try:
    import requests
except:
    os.system('pip install requests')
    sys.exit(f'{str(datetime.now())[:-7]} INFO Please run the it again!')



class CyberDrop:
    THREADS = 10
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}

    def __init__(self):
        self.session = requests.session()
        self.imageList = []

    def fetchImages(self):
        url = sys.argv[1]
        if 'http' not in sys.argv[1]:
            url = 'https://cyberdrop.me/a/' + sys.argv[1]
        htmlResponse = self.session.get(url, headers=self.HEADERS)
        if htmlResponse.status_code == 200:
            for image in re.findall(r'<a class="image" href="(.*?)" target="_blank"', htmlResponse.text):
                self.imageList.append(image)
        else:
            print(f'{str(datetime.now())[:-7]} ERROR Cannot connect to the server [{htmlResponse.status_code}]')

    def checkdir(self):
        if not os.path.exists('./downloads'):
            os.mkdir('./downloads')

    def downloadImages(self, url):
        fileExt = re.search(r'(\.mp4|\.gif|\.jpg|\.png|\.webm|\.jpeg)', url).group(1)
        fileName = uuid4().hex
        print(f'{str(datetime.now())[:-7]} INFO Downloading: {fileName}{fileExt}', end='\r')
        with open('./downloads/' + fileName + fileExt, 'wb') as f:
            f.write(self.session.get(url).content)

print(f'{str(datetime.now())[:-7]} INFO Initializing...')
cyberdrop = CyberDrop()
cyberdrop.checkdir()
print(f'{str(datetime.now())[:-7]} INFO Fetching images...')
cyberdrop.fetchImages()
_ = [_ for _ in ThreadPool(cyberdrop.THREADS).imap_unordered(cyberdrop.downloadImages, cyberdrop.imageList)]
