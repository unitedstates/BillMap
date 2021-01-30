#!/usr/bin/python

import psycopg2
from config import config


def insert_crs(report_name, report_date, report_link):
    sql = """INSERT INTO crs(report_name, report_date, report_link)
             VALUES(%s, %s, %s) RETURNING crs_id;"""
    conn = None
    crs_id = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (report_name, report_date, report_link))
        crs_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return crs_id