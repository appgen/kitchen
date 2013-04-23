import os
import json
from group import group_columns

def views():
    view_dir = os.path.join('pantry', 'socrata', 'views')
    view_ids = os.listdir(view_dir)
    return [json.load(open(os.path.join(view_dir, view_id))) for view_id in view_ids]

def columns():
    pass # for k, v in group_columns(views()).items()

example = group_columns(views())[(u'text', u'neighborhood')]
