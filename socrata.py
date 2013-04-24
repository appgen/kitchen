import os
import json

import pandas

from socrata_group import group_columns

SOCRATA = os.path.join('pantry', 'socrata')
VIEWS = os.path.join(SOCRATA, 'views')

def rows(viewid):
    return pandas.io.parsers.read_csv(os.path.join(SOCRATA, 'rows', viewid))

def viewids():
    return os.listdir(VIEWS)

def views():
    return {view_id: json.load(open(os.path.join(VIEWS, view_id))) for view_id in viewids()}

def columns():
    return group_columns(views().values())

def join(column_name, view_ids):
    # Load
    dfs = map(rows, view_ids)

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
    example = join(u'building_address', group_columns(views())[(u'text', u'building_address')])
