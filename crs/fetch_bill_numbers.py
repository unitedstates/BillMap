#!/usr/bin/python

import psycopg2
from config import config


def fetch_bill_numbers():
    conn = None
    bill_numbers = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT bill_id, number FROM bills")
        bill_numbers = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return bill_numbers