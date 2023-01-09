#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import argparse
import configparser
import datetime
import glob
import hashlib
import os
import sys
from pathlib import Path

import rfeed

from stack import Stack


def getargs():
    parser = argparse.ArgumentParser(description="RSDH RSS feed generator.")
    parser.add_argument(
        "-c", "--config", help="Configuration file", dest="config", required=True
    )
    args = parser.parse_args()
    return args


def getconfig(args):
    config = configparser.ConfigParser()
    try:
        config.read(args.config)
        stacksite = config.get("site", "stacksite")
        token = config.get("site", "token")
        showdir = config.get("show", "showdir")
        title = config.get("show", "title")
        link = config.get("show", "link")
        description = config.get("show", "description")
        language = config.get("show", "language")
        image = config.get("show", "image")
        latestmatch = config.get("show", "latestmatch")
        output = config.get("file", "output")
        localdir = config.get("local", "location")
        download = config.get("download", "location")
        return (
            stacksite,
            token,
            showdir,
            title,
            link,
            description,
            language,
            image,
            latestmatch,
            output,
            localdir,
            download,
        )
    except Exception as e:
        print("Configuration {}\n please check config file".format(e))
        sys.exit(1)


def createitem(filename, title, pubdate, url, size, mediatype, permalink):
    guid = hashlib.md5(filename.encode("utf-8")).hexdigest().upper()
    item = rfeed.Item(
        title=title,
        pubDate=pubdate,
        description=title,
        enclosure=rfeed.Enclosure(url=url, length=size, type=mediatype),
        guid=rfeed.Guid(guid, isPermaLink=permalink),
    )
    return item


def createfeed(rss, title, description, language, image, link):
    feed = rfeed.Feed(
        link=link,
        title=title,
        description=description,
        language=language,
        lastBuildDate=datetime.datetime.now(),
        items=rss,
        image=rfeed.Image(url=image, link=link, title=title),
    )
    return feed.rss()


def downloadurl(showdir, path, download):
    url = "{}{}/{}".format(download, showdir.replace(" ", "%20"), path.split("/")[-1])
    return url


def downloadfile(rsdh, localdir, path):
    filename = "{}/{}".format(localdir, path.split("/")[-1])
    if not Path(localdir).is_dir():
        Path(localdir).mkdir()
    if not Path(filename).is_file():
        print('Downloading to disk from "{}" to "{}'.format(path, filename))
        f = open(filename, mode="wb")
        f.write(rsdh.download(path))
        f.close()
    else:
        print('File already on disk "{}"'.format(path))


def detectdate(description):
    airdate = None
    for item in description.replace("_", " ").replace("+", " ").split(" "):
        if len(item) == 8 and item.startswith("20"):
            try:
                airdate = datetime.datetime.strptime(item, "%Y%m%d")
            except Exception as e:
                print(
                    "Error: {} : cannot convert {} \
                     into datetime object [{}]".format(
                        description, item, e
                    )
                )
    return airdate


def getshows(rsdh, showdir, localdir, download, permalink, **kwargs):
    rss = []
    dirlist = ['/{}/'.format(showdir)]
    match = ""
    maxcount = 10000
    scount = 0

    if "match" in kwargs:
        match = kwargs["match"]
    for i in rsdh.list(directory=showdir):
        if i["Type"] == "Dir":
            dirlist.append(i["Name"])
    if not len(dirlist):
        dirlist.append(showdir)

    for shows in dirlist:
        for show in rsdh.list(directory=shows):

            if (
                    scount < maxcount
                    and show["Type"] == "audio/mpeg"
                    and match.lower() in show["Path"].lower()
            ):
                downloadfile(rsdh, localdir, show["Path"])

    files = glob.glob('{}/*'.format(localdir))

    for file in files:
        filename = file.split("/")[-1]
        description = filename.split(".")[0].replace("-", " ")
        showdate = detectdate(description)
        filesize = os.path.getsize(file)
        fileurl = downloadurl(localdir, filename, download)
        filetype = 'audio'
        if filesize > 1024*1024*1024:
            rss.append(
                createitem(
                    filename,
                    description,
                    showdate,
                    fileurl,
                    filesize,
                    filetype,
                    permalink=permalink,
                )
            )
            print("Adding item {}".format(filename))
        else:
            print('File with a too small size {}'.format(filename))
            sys.exit(1)
    return rss


def main():
    args = getargs()
    (
        stacksite,
        token,
        showdir,
        title,
        link,
        description,
        language,
        image,
        latestmatch,
        output,
        localdir,
        download,
    ) = getconfig(args)
    rsdh = Stack(stacksite=stacksite, token=token)
    rssallshows = getshows(
        rsdh, showdir, localdir, download, permalink=True, match=latestmatch
    )
    f = open(output, "w")
    f.write(createfeed(rssallshows, title, description, language, image, link))
    f.close()


if __name__ == "__main__":
    main()
