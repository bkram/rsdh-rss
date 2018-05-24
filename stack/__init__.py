import urllib
from io import BytesIO

import requests
from mutagen.id3 import ID3


class Stack:
    directory = ''
    path = ''

    def __init__(self, stacksite, token):
        self.stacksite = stacksite
        self.token = token
        self.params = {
            'public': 'true',
            'token': self.token,
            'type': 'folder',
            'offset': '0',
            'limit': '5000',
            'sortBy': 'mtime',
            'order': 'desc',
            'query': ''
        }

    def list(self, directory):
        self.directory = directory
        self.params['dir'] = self.directory
        dirlist = ['httpd/unix-directory']
        url = 'https://{}.stackstorage.com/public-share/{}/list/{}'.format(
            self.stacksite, self.token, self.directory)
        r = requests.get(url, params=self.params)
        resp = requests.get(r.url)
        listing = []
        if resp.status_code == 200:
            directory = resp.json()
            for item in directory['nodes']:
                if item['mimetype'] in dirlist:
                    listing.append(
                        dict(Type='Dir', Name=item['path'])
                    )
                else:
                    listing.append(
                        dict(Mimetype='File', Path=item['path'][1:], Type=item['mimetype'],
                             Size=item['fileSize'], Mediatype=item['mediaType']))
        return listing

    def downloadurl(self, path):
        preview = 'https://{}.stackstorage.com/public-share/{}/preview'.format(
            self.stacksite, self.token)
        previewparams = {'path': path, 'mode': 'full'}
        url = preview + '?' + urllib.parse.urlencode(previewparams)
        return url

    def getid3tag(self, path, tag):
        headers = {"Range": "bytes=0-2048"}
        r = requests.get(self.downloadurl(path), headers=headers)
        try:
            idinfo = ID3(BytesIO(r.content))[tag].text[0]
        except Exception as e:
            print('Cannot parse id3: {}'.format(e))
            idinfo = False
        return idinfo
