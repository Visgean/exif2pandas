# Extract EXIF to pandas / SQL / Excel / Feather

Extracts:

- file size 
- gps
- Exif data 

Allows export to: 

- Excel
- SQLite
- Feather

and anything else that [Pandas supports](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html).


## Installation

```
    $ pip install exif2pandas --user
```

To export the dataframe you will need one of these modules:

 - SQLite: ``pip install --user SQLAlchemy`` 
 - Feather: ``pip install --user pyarrow`` 
 - Excel: ``pip install --user xlsxwriter``

# Usage

```
usage: exif2pandas [-h] [-s SQLITE] [-f FEATHER] [-e EXCEL] [-p PROCESSES]
                   picture_folders [picture_folders ...]

Generate sql database with exif data.

positional arguments:
  picture_folders       Folders with the images

optional arguments:
  -h, --help            show this help message and exit
  -s SQLITE, --sqlite SQLITE
                        Output the data frame to SQLite file (this will
                        override existing file!)
  -f FEATHER, --feather FEATHER
                        Output the data frame to feather file (this will
                        override existing file!)
  -e EXCEL, --excel EXCEL
                        Output the data frame to excel (this will override
                        existing file!)
  -p PROCESSES, --processes PROCESSES
                        number of processes to use for collecting exif data,
                        defaults to 5
```

# Example:

```
    $ exif2pandas ~/Dropbox/Photos/ -s ~/photo_metadata.sqlite
```


# Speed

While this is not a benchmark at all, it takes me about 10 seconds to process 123 GB of photos. 
This was taken at my Dell XPS 9570 with Intel® Core™ i7-8750H CPU @ 2.20GHz × 12 CPU using 5 processes.

The resulting file is about 13 MB large.

# Structure

The following is an example of columns that are generated - some cameras might include different fields.

## Custom fields:

- all the columns ending with ``-float`` are evaluated fractions 
- ``cleaned_date`` - this is original date - ignores date set by editors..
- ``cleaned_latitude`` - converted latitude to GPS style, the algorithm is not very precise as far as I know
- ``cleaned_longitude``- longitude
- ``size_megabytes `` - image size in megabytes
- ``filename`` - original filename

## Exif fields:
```
exif-aperturevalue exif-aperturevalue-float exif-bodyserialnumber exif-brightnessvalue 
exif-brightnessvalue-float exif-colorspace exif-componentsconfiguration exif-compressedbitsperpixel 
exif-compressedbitsperpixel-float exif-customrendered exif-datetimedigitized exif-datetimeoriginal 
exif-digitalzoomratio exif-digitalzoomratio-float exif-exifimagelength exif-exifimagewidth 
exif-exifversion exif-exposurebiasvalue exif-exposurebiasvalue-float exif-exposuremode 
exif-exposureprogram exif-exposuretime exif-exposuretime-float exif-filesource exif-flash 
exif-flashpixversion exif-fnumber exif-fnumber-float exif-focallength exif-focallength-float 
exif-focallengthin35mmfilm exif-focalplaneresolutionunit exif-focalplanexresolution 
exif-focalplanexresolution-float exif-focalplaneyresolution exif-focalplaneyresolution-float 
exif-interoperabilityoffset exif-isospeedratings exif-lensmake exif-lensmodel exif-lensserialnumber 
exif-lensspecification exif-lightsource exif-maxaperturevalue exif-maxaperturevalue-float 
exif-meteringmode exif-scenecapturetype exif-scenetype exif-sensingmethod exif-sensitivitytype 
exif-sharpness exif-shutterspeedvalue exif-shutterspeedvalue-float exif-subjectarea 
exif-subjectdistancerange exif-subsectime exif-subsectimedigitized exif-subsectimeoriginal 
exif-usercomment exif-whitebalance
```

## GPS fields

```
gps-gpsaltitude gps-gpsaltitude-float gps-gpsaltituderef gps-gpsdate gps-gpsdestbearing 
gps-gpsdestbearing-float gps-gpsdestbearingref gps-gpsdop gps-gpsdop-float gps-gpsimgdirection 
gps-gpsimgdirection-float gps-gpsimgdirectionref gps-gpslatitude gps-gpslatituderef 
gps-gpslongitude gps-gpslongituderef gps-gpsmapdatum gps-gpsspeed gps-gpsspeed-float 
gps-gpsspeedref gps-gpstimestamp gps-gpsversionid
```

## Image Fields:

```
image-artist image-cfapattern image-cfarepeatpatterndim image-copyright image-datetime 
image-datetimeoriginal image-documentname image-exifoffset image-exposuretime 
image-exposuretime-float image-fnumber image-fnumber-float image-focallength 
image-focallength-float image-gpsinfo image-imagelength image-imagewidth 
image-isospeedratings image-make image-model image-orientation image-rating 
image-resolutionunit image-sampleformat image-software image-subfiletype 
image-xresolution image-xresolution-float image-ycbcrpositioning 
image-yresolution-float image-yresolution
```

# Other fields

```
interoperability-interoperabilityindex interoperability-interoperabilityversion
makernote-afpointset makernote-blurwarning makernote-colortemperature makernote-exposurecount
makernote-exposurewarning makernote-flashmode makernote-flashstrength 
makernote-flashstrength-float makernote-focusmode makernote-focuspixel 
makernote-focuswarning makernote-hdrimagetype makernote-motororbracket 
makernote-noteversion makernote-picturemode makernote-quality makernote-saturation 
makernote-sharpness makernote-slowsync makernote-whitebalance makernote-whitebalancefinetune 
```