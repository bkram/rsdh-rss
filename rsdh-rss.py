#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import argparse
import configparser
import datetime
import hashlib
import urllib
import requests
import rfeed


def getargs():
    parser = argparse.ArgumentParser(description='RSDH RSS feed generator.')
    parser.add_argument(
        '-c',
        '--config',
        help='Configuration file',
        dest='config',
        required=True)
    args = parser.parse_args()
    return args


def getconfig(args):
    config = configparser.ConfigParser()
    try:
        config.read(args.config)
        stacksite = config.get('site', 'stacksite')
        token = config.get('site', 'token')
        showdir = config.get('show', 'showdir')
        title = config.get('show', 'title')
        link = config.get('show', 'link')
        description = config.get('show', 'description')
        language = config.get('show', 'language')
        image = config.get('show', 'image')
        latestmatch = config.get('show', 'latestmatch')
        output = config.get('file', 'output')
        return stacksite, token, showdir, title, link, description, language, image, latestmatch, output
    except Exception as e:
        exit('Configuration {}\n please check config file'.format(e))


def createitem(filename, title, pubdate, url, size, mediatype, permalink):
    guid = hashlib.md5(filename.encode('utf-8')).hexdigest().upper()
    item = rfeed.Item(
        title=title,
        pubDate=pubdate,
        description=title,
        enclosure=rfeed.Enclosure(
            url=url, length=size, type=mediatype),
        guid=rfeed.Guid(
            guid, isPermaLink=permalink))
    return item


def createfeed(rss, title, description, language, image, link):
    feed = rfeed.Feed(
        link=link,
        title=title,
        description=description,
        language=language,
        lastBuildDate=datetime.datetime.now(),
        items=rss,
        image=rfeed.Image(
            url=image, link=link, title=title))
    return feed.rss()


def detectdate(description):
    for item in description.replace('_', ' ').split(' '):
        if len(item) == 8 and item.startswith('20'):
            try:
                airdate = datetime.datetime.strptime(item, '%Y%m%d')
            except Exception as e:
                print('Error: {} : cannot convert {} into datetime object [{}]'.
                      format(description, item, e))
                airdate = None
    return airdate


def downloadurl(path, stacksite, showsparams):
    preview = 'https://{}.stackstorage.com/public-share/{}/preview'.format(
        stacksite, showsparams['token'])
    previewparams = {'path': path, 'mode': 'full'}
    url = preview + '?' + urllib.parse.urlencode(previewparams)
    return url


def getshows(showsurl, showsparams, showdir, stacksite):
    rss = []
    for year in range(datetime.datetime.now().year, 2007, -1):
        showsparams['dir'] = '/{}/'.format(showdir) + str(year)
        r = requests.get(showsurl, params=showsparams)
        resp = requests.get(r.url)
        if resp.status_code == 200:
            shows = resp.json()
            for show in shows['nodes']:
                if show['mimetype'] == 'audio/mpeg':
                    path = show['path']
                    filename = path.split('/')[-1]
                    filesize = show['fileSize']
                    filetype = show['mediaType']
                    description = filename.split('.')[0].replace('-', ' ')
                    showdate = detectdate(description)
                    fileurl = downloadurl(path, stacksite, showsparams)
                    rss.append(
                        createitem(
                            filename,
                            description,
                            showdate,
                            fileurl,
                            filesize,
                            filetype,
                            permalink=True))
    return rss


def getlatest(showsurl, showsparams, stacksite, latestmatch):
    rss = []
    showsparams['dir'] = '/- LATEST RECORDINGS/'
    r = requests.get(showsurl, params=showsparams)
    resp = requests.get(r.url)
    if resp.status_code == 200:
        shows = resp.json()
        for show in shows['nodes']:
            if show['mimetype'] == 'audio/mpeg' and latestmatch in show['path']:
                path = show['path']
                filename = path.split('/')[-1]
                filesize = show['fileSize']
                filetype = show['mediaType']
                description = filename.split('.')[0].replace('-', ' ')
                showdate = detectdate(description)
                fileurl = downloadurl(path, stacksite, showsparams)
                rss.append(
                    createitem(
                        filename,
                        description,
                        showdate,
                        fileurl,
                        filesize,
                        filetype,
                        permalink=False))
        return rss


def main():
    args = getargs()
    stacksite, token, showdir, title, link, description, language, image, latestmatch, output = getconfig(
        args)
    showsurl = 'https://{}.stackstorage.com/public-share/{}/list'.format(
        stacksite, token)
    showsparams = {
        'public': 'true',
        'token': token,
        'type': 'folder',
        'offset': '0',
        'limit': '5000',
        'sortBy': 'mtime',
        'order': 'desc',
        'query': ''
    }

    rssfeed = getlatest(showsurl, showsparams, stacksite, latestmatch) \
              + getshows(showsurl, showsparams, showdir, stacksite)
    f = open(output, 'w')
    f.write(createfeed(rssfeed, title, description, language, image, link))
    f.close()


if __name__ == "__main__":
    main()
