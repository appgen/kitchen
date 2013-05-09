import os
import json
import re

import pandas

SOCRATA = os.path.join('pantry', 'socrata')
VIEWS = os.path.join(SOCRATA, 'views')

def viewdict():
    'A hash from viewid to the metadata'
    return {view_id: json.load(open(os.path.join(VIEWS, view_id))) for view_id in os.listdir(VIEWS)}

def columndict(minmatches = 2):
    'A hash from column (type,name) to viewids'
    views = viewdict().values()
    everything = _group(views, lambda view: [(col['dataTypeName'], col['fieldName']) for col in view.get('columns', [])]).items()
    return {k:v for k,v in everything if k != (u'geospatial', u'shape') and len(v) >= minmatches}

def _is_map(view):
    'Is this view a map?'
    return (u'geospatial', u'shape') in set([(col['dataTypeName'], col['fieldName']) for col in view.get('columns', [])])

def parse_shape(df):
    'Parse a shape into longitude and latitude.'
    def unshape(group = 1):
        return lambda shape: float(re.match(r'\(([0-9.]*), (-[0-9.]*)\)', shape).group(group))

    df['Longitude'] = df['Shape'].map(unshape(group = 2))
    df['Latitude'] = df['Shape'].map(unshape(group = 1))
    del(df['Shape'])

    return df

def uniondict():
    'A hash from partial title to a bunch of datasets that can be unioned'
    views = filter(_is_map, viewdict().values())
    everything = _group(views, lambda view: [tuple([(col['dataTypeName'], col['fieldName']) for col in view.get('columns', [])])]).items()
    return {k:v for k,v in everything if len(v) > 1}

def uniondict_broad():
    'A hash from partial title to a bunch of datasets that can be unioned'
    views = viewdict().values()
    everything = _group(views, lambda view: [tuple([col['fieldName'] for col in view.get('columns', [])])]).items()
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
        df = df.groupby(column_type_name).last()
        dfs.append(df)

    # Join
    left = dfs[0]
    for right in dfs[1:]:
        left = pandas.merge(left, right, on = column_type_name[1])
        if df.empty:
            left = right

    if not df.empty:
        return left

def union(column_type_names, id_set):
    ids = list(id_set)
    df = _rows(ids[0])
    for viewid in ids[1:]:
        df = df.append(_rows(viewid))
    return df

from Levenshtein import median
def combine_titles(views):
    'Produce a title for a unioned dataset.'
    titles = [view['name'] for view in views]
    for title in titles:
        # Remove borough
        title = re.sub(r' ?((the ?)?bronx|manhattan|queens|staten island|brooklyn)', '', title)
        # Remove year
        title = re.sub(r' ?(199|200)[0-9]', '', title)
    return median(titles)

def fix_types(view, df):
    set([u'calendar_date',
             u'text',
                  u'percent',
                       u'number',
                            u'url',
                                 u'location',
                                      u'money',
                                           u'date'])


if __name__ == '__main__':
    v = viewdict()
    c = columndict()
    u = uniondict()
