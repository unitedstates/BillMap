# FlatGov
Utilities and applications for the FlatGov project

## Data

### Bulk downloads
The core metadata that will be used for this project can be downloaded in bulk from ProPublica<sup>TM</sup> here: https://www.propublica.org/datastore/dataset/congressional-data-bulk-legislation-bills

Bulk historical metadata is available for one-year ranges. Data for the current Congress is updated twice daily.

### Scraping
#### Install congress repository and dependencies

The text of bills can be scraped with the Python project here: `https://github.com/unitedstates/congress`. Install the `congress` Python virtual environment, install the requirements (`pip install requirements.txt`). The scrapers were built with Python 2.7 and have not been upgraded; updates may be needed for a production environment, but the `@unitedstates/congress` scraper is sufficient to gather the baseline data to test the utilities in this repository.

On MacOS (Catalina), installing the `congress` requirements involved a few adjustments:

1. Install OpenSSL 1.02 with Homebrew. The latest OpenSSL (>1.1) causes problems with certain requirements; unfortunately, version 1.0.0 also failed. A script was set up by a Github user to install version 1.0.2.
`brew uninstall openssl --ignore-dependencies; brew uninstall openssl --ignore-dependencies; brew uninstall libressl --ignore-dependencies; https://raw.githubusercontent.com/Homebrew/homebrew-core/8b9d6d688f483a0f33fcfc93d433de501b9c3513/Formula/openssl.rb;`

2. Link the OpenSSL libraries
```
export LDFLAGS=-L/usr/local/opt/openssl/lib
export CPPFLAGS=-I/usr/local/opt/openssl/include
```

3. Install `` and `` directly
```
pip install pytz
pip install pep517
pip install cryptography
```

4. Install requirements
From the `congress` repository directory, `pip install -r requirements.txt`


### Run the scraper

```bash
./run govinfo --bulkdata=BILLSTATUS
./run bills
```

