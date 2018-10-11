import urllib

import requests
from bs4 import BeautifulSoup


class Stack:
    """
    Interface with TransIP's Stack storage
    Requires
        - stacksite (subdomain before stackstorage.com)
        - token (token as shown in url, after /s/)
    """
    directory = ''
    path = ''
    csrf = ''
    s = requests.session()

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

        url = 'https://{}.stackstorage.com/s/{}'.format(self.stacksite, self.token)
        mainpage = self.s.get(url)
        soup = BeautifulSoup(mainpage.content, "lxml")
        for meta in soup.findAll("meta"):
            mstring = str(meta)
            if "csrf-token" in (str(meta)):
                self.csrf = mstring.split('"')[1]

    def list(self, directory):
        self.directory = directory
        self.params['dir'] = self.directory
        session = self.s
        dirlist = ['httpd/unix-directory']
        url = 'https://{}.stackstorage.com/public-share/{}/list/{}'.format(
            self.stacksite, self.token, self.directory)
        r = session.get(url, params=self.params)
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

    def download(self, path):
        session = self.s
        preview = 'https://{}.stackstorage.com/public-share/{}/download?'.format(
            self.stacksite, self.token)
        previewparams = {'download-path': path, 'CSRF-Token': self.csrf}
        url = preview + urllib.parse.urlencode(previewparams)
        resp = session.get(url)

        if resp.status_code == 200:
            return resp.content
        else:
            print(resp.status_code)
