#!/usr/bin/env python2
import json
from dumptruck import DumpTruck

dt = DumpTruck(dbname = '/tmp/appgen.db')

def query(filename, sql):
    'Query the database and save to a file.'
    f = open(filename, 'w')
    d = json.dump(dt.execute(sql), f, indent = 2)
    f.close()
    return d

def unionability():
    '''
    please give me the unionability data sorted by #of datasets per superset
    https://www.facebook.com/perluette/posts/2411449970353
    '''

    query('/tmp/unionability.json', '''
    SELECT "attribution", "schema", count(*) AS 'n'
    FROM "dataset"
    GROUP BY "attribution", "schema"
    ORDER BY "n";
    ''')

if __name__ == '__main__':
    unionability()
