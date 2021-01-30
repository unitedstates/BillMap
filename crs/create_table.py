#!/usr/bin/python

import psycopg2
from config import config


def create_table():
    commands = (
        """ 
        CREATE TABLE bills (
            bill_id SERIAL PRIMARY KEY,
            number VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE crs (
            bill_id INTEGER NOT NULL,
            FOREIGN KEY (bill_id)
                    REFERENCES bills (bill_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
            report_name VARCHAR(255) NOT NULL, 
            report_date VARCHAR(255) NOT NULL, 
            report_link VARCHAR(255) NOT NULL
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

create_table()