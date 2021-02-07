# FlatGov bills scraper

# About

This is the Django based scraper for the CRS reports.

## Installation

```shell
pip3.9 install requirements.txt
```

## Collecting the data

SQLite database is attached and pre-filled with bills records.

Two tables defined in the models: `Bills` and `CrsReport`. Table `Bills` is pre-populated from JSON, and it happens during applying first migration `0001_initial.py`. 

If you want start from scratch you need to:

Download a JSON file:

```shell
cd FlatGov
wget https://github.com/aih/FlatGov/files/5878874/billsMeta.json.gz
gunzip billsMeta.json.gz
```

Apply only first migration on a clean database:

```shell
python3.9 manage.py migrate 0001_initial
```

The migration command will trigger importing values from `billsMeta.json` to `Bills`.

To scrape the data to CRS table enter a Django console and do:

```shell
python3.9 manage.py shell
```

```python
from FlatGov.populate_crs_table import CrsFromApi
crs = CrsFromApi()
crs.populate()
```
