import psycopg2
import pandas as pd
import sys
import os
from django.conf import settings


def pg_load_table(file_path):
    '''
    This function upload csv to a target table
    '''
    try:
        conn = psycopg2.connect(dbname="energy", host='db', port=5432,
         user="postgres", password="rucha")
        cur = conn.cursor()
        table_name = 'downloadcsv_metadata' #'downloadcsv_yearlyresult'
        with open(file_path, "r") as f:
            next(f)
            cur.copy_from(f, table_name, sep=',')
        conn.commit()
    except Exception as e:
        print("Error: {}".format(str(e)))
        sys.exit(1)

file_path = os.path.join("historical_data/Metadata.csv") #'YearlyResult.csv' # Change the file path.
pg_load_table(file_path)