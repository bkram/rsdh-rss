# Preface
Currently no longer working.

It seems Stack now requires a valid *cookie* to do a direct download, since we create static url's for the RSS feed this no longer works :( .
So the feed gets created but it is no longer possible to download the file in the podcast app.

At some point I will update this project to download an x amount of shows while crawling to be able to serve them locally.

Since Radio Stad Den Haag does not provide RSS links by themselves, but I like to listen to their shows on the go I have created this feed generator, it crawls their stackstorage download section and creates the RSS feed.

## Requirements

- python3

### Python modules (via pip3 install)

- argpar
- configparser
- datetime
- hashlib
- urllib
- requests
- rfeed
- mutagen

## Example

```bash
python3 rsdh-rss.py -c rsdh-ssl.cfg
```
## Configuration files

|Config file|Show Title|
|------|----|
|rsdh-disco.cfg|Disco Dance Department|
|rsdh-doucheco.cfg|DoucheCo|
|rsdh-iventi.cfg|I Venti d'Azzurro|
|rsdh-ssl.cfg|Radio Stad Den Haag Sundaynight Live|