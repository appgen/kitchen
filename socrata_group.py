#!/usr/bin/env python2
'''
Mash up multiple datasets.
'''
from urlparse import urlparse
from copy import deepcopy

class Attributiontree:
    def __init__(self, tree = [{}, set()]):
        self._tree = tree

    # Construction
    # ---------------------------------

    # The empty tree
    empty = [{}, set()]

    def build(self, path, viewid):
        self._tree = Attributiontree._build_tree(self._tree, path, viewid)

    @staticmethod
    def _build_tree(tree, path, viewid):
        '''
        Build a tree by which we can search urls. Each subtree is a tuple of a dict
        of urls and a set of 4x4 Socrata identifiers.
        '''
        # If we have stuff in the path that are not in the tree, add an empty branch.
        if path[0] not in tree[0]:
            tree[0][path[0]] = Attributiontree.empty
        subtree = deepcopy(tree[0][path[0]])

        # Recurse
        if len(path) == 1:
            # We have no more items in the path, so we're done.
            subtree[1].add(viewid)
        else:
            # Add the next url part
            subtree = Attributiontree._build_tree(subtree, path[1:], viewid)

        tree[0][path[0]] = subtree
        return tree

    # Querying
    # ---------------------------------
    def __repr__(self):
        def shorten(param):
            if len(param) > 2:
                param = param[:2] + ['...']
            return ', '.join(param)
        params = map(shorten, [self.children().keys(), list(self.current_viewids())])
        return 'Children: %s  |  Viewids: %s' % tuple(params)

    def children(self):
        return {k:Attributiontree(v) for k,v in self._tree[0].items()}

    def descendant(self, path):
        'Find things with similar urls.'
        tree = deepcopy(self)
        for subdir in filter(None, path.split('/')):
            tree = tree.children()[subdir]
        return tree

    def child_paths(self):
        return set(self._tree[0].keys())

    def descendant_paths(self):
        todo = [([], self)]
        while len(todo) > 0:
            path, tree = todo.pop()
            for filename, child in tree.children().items():
                if len(child.current_viewids()) > 0:
                    yield '/'.join(path + [filename])
            todo.extend([(path + [subdir], v) for subdir, v in tree.children().items()])

    def current_viewids(self):
        return self._tree[1]

    def descendant_viewids(self):
        todo = [self]
        while len(todo) > 0:
            current = todo.pop()
            for viewid in current.current_viewids():
                yield viewid
            todo.extend(current.children().values())

def attribution_links(views):
    link_tree = Attributiontree()
    for view in views:
        if 'attributionLink' in view:
            url = urlparse(view['attributionLink'])
            path = [url.netloc] + filter(None, url.path.split('/') + [url.query])
            link_tree.build(path, view['id'])
    return link_tree

def group_tags(views):
    return group(views, lambda view: view.get('tags', []))

def distinct_columns(views):
    return filter(lambda a: a != (u'geospatial', u'shape'), group(views, lambda view: [(col['dataTypeName'], col['fieldName']) for col in view.get('columns', [])]))

def group_owner(views):
    return group(views, lambda view: [view.get('owner', {}).get('displayName', None)])

def group(views, func):
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
    for k, v in distinct_columns(views).items():
        if len(v) > 50:
            print k
#   for k, v in group_owner(views).items():
#       if len(v) > 2:
#           print k

#   t = attribution_links(views)
#   print set(t.descendant('schools.nyc.gov/NR/rdonlyres/66E8CC55-51E7-4DE5-8C5C-08C588701A1E').descendant_viewids())
#   print set(t.descendant('www.nyc.gov/html/dcp/html').descendant_paths())
