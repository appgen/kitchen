import os
import json

import pandas

from group import group_columns

SOCRATA = os.path.join('pantry', 'socrata')
VIEWS = os.path.join(SOCRATA, 'views')

def rows(viewid):
    return pandas.io.parsers.read_csv(os.path.join(SOCRATA, 'rows', viewid))

def viewids():
    view_ids = os.listdir(VIEWS)
    return [json.load(open(os.path.join(VIEWS, view_id))) for view_id in view_ids]

def columns():
    pass # for k, v in group_columns(views()).items()

example = group_columns(viewids())[(u'text', u'neighborhood')]
