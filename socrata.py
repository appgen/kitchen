import os
import json

import pandas

from socrata_group import distinct_columns

SOCRATA = os.path.join('pantry', 'socrata')
VIEWS = os.path.join(SOCRATA, 'views')

def rows(viewid):
    return pandas.io.parsers.read_csv(os.path.join(SOCRATA, 'rows', viewid))

def viewids():
    return os.listdir(VIEWS)

def viewdict():
    return {view_id: json.load(open(os.path.join(VIEWS, view_id))) for view_id in viewids()}

def join(column_name, viewids):
    # Load
    dfs = map(row, viewids)

    for df in dfs:
        # Lowercase names
        df.columns = [name.lower() for name in df.columns]
        # Distinct
        df = df.groupby(column_name).last()

    # Join
    left = dfs[0]
    for right in dfs[1:]:
        try:
            left = pandas.merge(left, right, on = column_name)
        except:
            break
    return left

if __name__ == '__main__':
    # example = join(u'building_address', distinct_columns(viewdict().values())[(u'text', u'building_address')])
    v = viewdict()
    c = distinct_columns(v.values()))
    join(u'building_address',
