# Bulk rename PDFs


Renames all whacky PDF named files to a bit better form. Extracts new name either from metadata or text on the first slide. 


### Install: 

```
$ sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python-dev
$ pip3 install pdfs-rename --user
```

### Usage:

```
usage: pdfs-rename [-h] [--rename] [--extract] pdfs [pdfs ...]

positional arguments:
  pdfs        list of filenames to rename

optional arguments:
  -h, --help  show this help message and exit
  --rename    rename the files, on default we only print extracted filenames
  --extract   extract new name from text
```
