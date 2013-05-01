import os
import json

import pandas

SOCRATA = os.path.join('pantry', 'socrata')
VIEWS = os.path.join(SOCRATA, 'views')

def viewdict():
    'A hash from viewid to the metadata'
    return {view_id: json.load(open(os.path.join(VIEWS, view_id))) for view_id in os.listdir(VIEWS)}

def columndict():
    'A hash from column (type,name) to viewids'
    views = viewdict().values()
    everything = _group(views, lambda view: [(col['dataTypeName'], col['fieldName']) for col in view.get('columns', [])]).items()
    return {k:v for k,v in everything if k != (u'geospatial', u'shape')}

def _rows(viewid):
    'Get the rows for a viewid'
    return pandas.io.parsers.read_csv(os.path.join(SOCRATA, 'rows', viewid))

def _group(views, func):
    '''
    Produce a dictionary mapping column types to all of the datasets containing
    whatever property.
    '''
    items = {}
    for view in views:
        for item in func(view):
            if item not in items:
                items[item] = set()
            items[item].add(view['id'])
    return items

def join(column_name, dfs):
    'Join a bunch of dataframes on a column name'
    # Load
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
    v = viewdict()
    c = columndict()
