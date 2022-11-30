# Preface

Mirrors a show from RSDH from their Stackstorage.com site and creates a rss feed for the downloaded episodes.
Does not do any housekeeping at the moment and the amount of episodes it does track is hardcoded as well.

Working again since January 2020.

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
- bs4

Includes custom module "stack", to list and download from Transip's Stackstorage.com anonymously.

## Example

```bash
python3 rsdh-rss.py -c rsdh-ssl.cfg
```

## Configuration files

|Config file|Show Title|
|------|----|
|rsdh-doucheco.cfg|DoucheCo|
|rsdh-iventi.cfg|I Venti d'Azzurro|
|rsdh-ssl.cfg|Radio Stad Den Haag Sundaynight Live|
