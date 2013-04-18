#!/usr/bin/env python2
'''
Mash up multiple datasets.
'''
from urlparse import urlparse
from copy import deepcopy
from lxml.etree import Element, XML

def attribution_links(views):
    link_tree = Element('a')
    for view in views:
        if 'attributionLink' in view:
            url = urlparse(view['attributionLink'])
            path = [url.netloc] + filter(None, url.path.split('/') + [url.query])

            xpath = ''
            for part in path:
                xpath += '/' + part
                if link_tree.xpath(xpath) == []:
                    link_tree.append(Element('a'))

            link_tree.xpath(xpath)[0].append(XML('<viewid>%s</viewid>' % view['attributionLink']))

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

    t = attribution_links(views)
