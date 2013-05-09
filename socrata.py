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
    return {k:v for k,v in everything if k != (u'geospatial', u'shape') and len(v) > 1}

def uniondict():
    'A hash from partial title to a bunch of datasets that can be unioned'
    views = viewdict().values()
    everything = _group(views, lambda view: [tuple([(col['dataTypeName'], col['fieldName']) for col in view.get('columns', [])])]).items()
    return {k:v for k,v in everything if len(v) > 1}

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

def join(column_type_name, ids):
    'Join a bunch of dataframes on a column name'
    # Load
    dfs = []
    for viewid in ids:
        # Load it
        df = _rows(viewid)
        # Lowercase names
        df.columns = [name.lower() if name.lower() == column_type_name[1] else viewid + u'-' + name.lower() for name in df.columns]
        # Distinct
#       df = df.groupby(column_type_name).last()
        dfs.append(df)

    # Join
    left = dfs[0]
    for right in dfs[1:]:
        left = pandas.merge(left, right, on = column_type_name[1])
        if df.empty:
            left = right

    if not df.empty:
        return left

def union(column_type_names, ids):
    df = None
    for viewid in ids:
        if df == None:
            df = _rows(viewid)
        else:
            df.append(_rows(viewid))
    return df

from Levenshtein import median
def union_title(views):
    'Produce a title for a unioned dataset.'
    titles = [view['name'] for view in views]
    for title in titles:
        # Remove borough
        title = re.sub(r' ?((the ?)?bronx|manhattan|queens|staten island|brooklyn)', '', title)
        # Remove year
        title = re.sub(r' ?(199|200)[0-9]', '', title)
    return median(titles)

if not __name__ == '__main__':
    v = viewdict()
#   c = columndict()
    u = uniondict()
