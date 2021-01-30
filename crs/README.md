To run these script:
    1. Copy billsMeta.json to the root of the project.
    2. Rename database.ini.template to database.ini and set the config of your local postgres DB.
    3. Run the following scripts:
        - python bulk_download.py (to download report metadata json and pdf files) It should take long time.
        - python create_table.py (to create bills and crs table in crs database)
        - python insert_mock_billdata.py (to insert bill numbers from billsMeta.json to bills table)
        - python main.py (This is the main script)