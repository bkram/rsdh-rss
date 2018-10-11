# Stackstorage python module

## Usage example of the included stackstorage module.

### Ipython session

Listing a directory and downloading a file.

```python
import stack
rsdh = stack.Stack(stacksite='ewagro-2', token='suzB3bQvfQu7ihZ')

rsdh.list('/Top 100/2009')

[{'Mimetype': 'File',
  'Path': 'Top 100/2009/Top100-2009.mp3',
  'Type': 'audio/mpeg',
  'Size': 616759296,
  'Mediatype': 'audio'}]

download = rsdh.download('Top 100/2009/Top100-2009.mp3')

f = open('download.mp3', mode='wb')
f.write(download)
f.close()
```
