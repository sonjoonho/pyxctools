# Python xeno-canto Tools

[![Build Status](https://travis-ci.org/sonjoonho/pyxctools.svg?branch=master)](https://travis-ci.org/sonjoonho/pyxctools)

This is a project that wraps the [https://www.xeno-canto.org/](xeno-canto) API for easy use in Python notebooks and scripts.

This project requires Python 3.6 and above.

## Features

Performs API calls, supporting [https://www.xeno-canto.org/help/search](advanced search parameters), returning data in a Python dictionary. 

Example of value returned by `query`
```
{'numRecordings': '3', 
'numSpecies': '1', 
'page': 1, 
'numPages': 1, 
'recordings': [
            {'id': '228435', 'gen': 'Chordeiles', 'sp': 'nacunda', 'ssp': '', 'en': 'Nacunda Nighthawk',
             'rec': 'Peter Boesman', 'cnt': 'Brazil', 'loc': 'Pantanal, Pixaim area, Mato Grosso',
             'lat': '-16.6666666667',
             'lng': '-56.8333333333', 'type': 'song', 'file': '//www.xeno-canto.org/228435/download',
             'lic': '//creativecommons.org/licenses/by-nc-nd/4.0/', 'url': 'https://www.xeno-canto.org/228435',
             'q': 'B', 'time': '05:45', 'date': '2005-07-31'},
            {'id': '228434', 'gen': 'Chordeiles', 'sp': 'nacunda', 'ssp': '', 'en': 'Nacunda Nighthawk',
             'rec': 'Peter Boesman', 'cnt': 'Brazil', 'loc': 'Pantanal, Pixaim area, Mato Grosso',
             'lat': '-16.6666666667',
             'lng': '-56.8333333333', 'type': 'song', 'file': '//www.xeno-canto.org/228434/download',
             'lic': '//creativecommons.org/licenses/by-nc-nd/4.0/', 'url': 'https://www.xeno-canto.org/228434',
             'q': 'B', 'time': '05:45', 'date': '2005-07-30'},
            {'id': '228433', 'gen': 'Chordeiles', 'sp': 'nacunda', 'ssp': '', 'en': 'Nacunda Nighthawk',
             'rec': 'Peter Boesman', 'cnt': 'Brazil', 'loc': 'Pantanal, Pixaim area, Mato Grosso',
             'lat': '-16.6666666667',
             'lng': '-56.8333333333', 'type': 'song', 'file': '//www.xeno-canto.org/228433/download',
             'lic': '//creativecommons.org/licenses/by-nc-nd/4.0/', 'url': 'https://www.xeno-canto.org/228433',
             'q': 'C', 'time': '05:45', 'date': '2005-07-30'}]}
```

Recordings returned by queries can be downloaded, along with a number of metadata fields:

```
id: the catalogue number of the recording on xeno-canto
gen: the generic name of the species
sp: the specific name of the species
ssp: the subspecies name
en: the English name of the species
rec: the name of the recordist
cnt: the country where the recording was made
loc: the name of the locality
lat: the latitude of the recording in decimal coordinates
lng: the longitude of the recording in decimal coordinates
type: the sound type of the recording (e.g. 'call', 'song', etc). This is generally a comma-separated list of sound types.
file: the URL to the audio file
lic: the URL describing the license of this recording
url: the URL specifying the details of this recording
q: the current quality rating for the recording
time: the time of day that the recording was made
date: the date that the recording was made
```

## About xeno-canto

>xeno-canto is a website dedicated to sharing bird sounds from all over the world. Whether you are a research scientist, a birder, or simply curious about a sound that you heard out your kitchen window, we invite you to listen, download, and explore the bird sound recordings in the collection.
>The service provides a database of bird song and sound recordings contributed and maintained by enthusiasts worldwide. It provides access to search the connection and play or download recordings and to submit new recordings. Discussion forums encourage interactions among members of the birding community to exchange information about bird song and related topics.

from https://www.xeno-canto.org/.
