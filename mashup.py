#!/usr/bin/env python2
'''
Mash up multiple datasets.
'''

def group_columns(views):
    '''
    Produce a dictionary mapping column types to all of the datasets containing
    such a column.
    '''
    column_types = {}
    for view in views:
        for col in view['columns']:
            key = (col['dataTypeName'], col['fieldName'])
            if key not in column_types:
                column_types[key] = set()
            column_types[key].add(view['id'])
    return column_types

def _group_tags(views):
    tags = {}
    for view in views:
        for tag in view.get('tags', []):
            if tag not in tags:
                tags[tag] = set()
            tags[tag].add(view['id'])
    return tags

def group_tags(views):
    return group(lambda view: view.get('tags', []))

def group(func):
    items = {}
    for view in views:
        for item in func(view):
            if item not in items:
                items[item] = set()
            items[item].add(view['id'])
    return items

if __name__ == '__main__':
    import os
    import json
    view_dir = os.path.join('pantry', 'socrata', 'views')
    view_ids = os.listdir(view_dir)
    views = [json.load(open(os.path.join(view_dir, view_id))) for view_id in view_ids]
    for k, v in group_columns(views).items():
        if len(v) > 30:
            print k
    print group_tags(views)
