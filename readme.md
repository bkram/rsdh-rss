# Preface

Mirrors a show from RSDH from their Stackstorage.com site and creates a rss feed for the downloaded episodes.
Does not do any housekeeping at the moment and the amount of episodes it does track is hardcoded as well.


> **Warning**
> Due to changes in the stack handling of the csrf-token, which was moved to javascript code, the stack module is currently not working.


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

See the config files in config/ for more details.
