## Updates

#### Added Bill, Sponsor model to bills app.
1. At the moment, we have 2 models - Bill & Sponsor. We will need to add more models and fields in the future.


#### Update environment variables
1. Add 2 env vars.
`DJANGO_SETTINGS_MODULE=flatgov.dev`
`SECRET_KEY=setAKeyInPrduction`


#### Download tmp files
1. Download tmp files in fetch_bill app. `~Flatgov/server_py/flatgov/fetch_bill$ ./download_bills.sh`
2. You can find `congress` directory in here - `~FlatGov/server_py/flatgov/congress`


#### Create billsMeta.json file via Django command.
1. Given that we are using django orm for database, we can store bill, sponsor data via django command.
2. `~FlatGov/server_py/flatgov/common` directory contains all the django commands.
3. Run `billdata.py` - `$python manage.py bill_data`
4. While running `billdata.py` file, it creates bill, sponsor objects and add proper relations.
