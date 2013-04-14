#!/usr/bin/env python2
'''
Mash up multiple datasets.
'''
from copy import deepcopy
from urlparse import urlparse

empty_tree = [{}, set()]
def _build_tree(tree, path, viewid):
    '''
    Build a tree by which we can search urls. Each subtree is a tuple of a dict
    of urls and a set of 4x4 Socrata identifiers.
    '''
    # If we have stuff in the path that are not in the tree, add an empty branch.
    if path[0] not in tree[0]:
        tree[0][path[0]] = deepcopy(empty_tree)

    # Recurse
    if len(path) == 1:
        # We have no more items in the path, so we're done.
        tree[0][path[0]][1].add(viewid)
    else:
        # Add the next url part
        tree[0][path[0]] = _build_tree(tree[0][path[0]], path[1:], viewid)
    return tree


def tree_affiliation_links(views):
    link_tree = deepcopy(empty_tree)
    for view in views:
        if 'attributionLink' in view:
            url = urlparse(view['attributionLink'])
            path = [url.netloc] + filter(None, url.path.split('/') + [url.query])
            link_tree = _build_tree(link_tree, path, view['id'])
    return link_tree

def group_tags(views):
    return group(views, lambda view: view.get('tags', []))

def group_columns(views):
    return group(views, lambda view: [(col['dataTypeName'], col['fieldName']) for col in view.get('columns', [])])

def group_owner(views):
    return group(views, lambda view: [view.get('owner', {}).get('displayName', None)])

def group(niews, func):
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

if __name__ == '__main__':
    import os
    import json
    view_dir = os.path.join('pantry', 'socrata', 'views')
    view_ids = os.listdir(view_dir)
    views = [json.load(open(os.path.join(view_dir, view_id))) for view_id in view_ids]
    for k, v in group_columns(views).items():
        if len(v) > 30:
            print k
    for k, v in group_owner(views).items():
        if len(v) > 2:
            print k
