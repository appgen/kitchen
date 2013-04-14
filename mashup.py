#!/usr/bin/env python2
'''
Mash up multiple datasets.
'''
from urlparse import urlparse
from copy import deepcopy

class AttributionTrie:
    def __init__(self, trie = [{}, set()]):
        self._trie = trie

    # Construction
    # ---------------------------------

    # The empty trie
    empty = [{}, set()]

    def build(self, path, viewid):
        self._trie = AttributionTrie._build_trie(self._trie, path, viewid)

    @staticmethod
    def _build_trie(trie, path, viewid):
        '''
        Build a trie by which we can search urls. Each subtrie is a tuple of a dict
        of urls and a set of 4x4 Socrata identifiers.
        '''
        # If we have stuff in the path that are not in the trie, add an empty branch.
        if path[0] not in trie[0]:
            trie[0][path[0]] = AttributionTrie.empty
        subtrie = deepcopy(trie[0][path[0]])

        # Recurse
        if len(path) == 1:
            # We have no more items in the path, so we're done.
            subtrie[1].add(viewid)
        else:
            # Add the next url part
            subtrie = AttributionTrie._build_trie(subtrie, path[1:], viewid)

        trie[0][path[0]] = subtrie
        return trie

    # Querying
    # ---------------------------------
    def __repr__(self):
        def shorten(param):
            if len(param) > 2:
                param = param[:2] + ['...']
            return ', '.join(param)
        params = map(shorten, [self._children().keys(), list(self.viewids())])
        return 'Children: %s  |  Viewids: %s' % tuple(params)

    def _children(self):
        return {k:AttributionTrie(v) for k,v in self._trie[0].items()}

    def descendant(self, path):
        'Find things with similar urls.'
        trie = deepcopy(self)
        for subdir in path.split('/'):
            trie = trie._children()[subdir]
        return trie

    def viewids(self):
        return self._trie[1]

def trie_affiliation_links(views):
    link_trie = AttributionTrie()
    for view in views:
        if 'attributionLink' in view:
            url = urlparse(view['attributionLink'])
            path = [url.netloc] + filter(None, url.path.split('/') + [url.query])
            link_trie.build(path, view['id'])
    return link_trie

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
