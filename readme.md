# Preface

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
## Example
```bash
python3 rsdh-rss.py -c rsdh-ssl.cfg
```
## Configuration files
|Config file|Show Title|
|------|----|
|rsdh-disco.cfg|Den Haag Disco Dance Department|
|rsdh-doucheco.cfg|DoucheCo|
|rsdh-iventi.cfg| I Venti d'Azzurro|
|rsdh-ssl.cfg|Radio Stad Den Haag Sundaynight Live|