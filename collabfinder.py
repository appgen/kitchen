#!/usr/bin/env python2
import os
from lxml.html import fromstring

DOWNLOAD_DIRECTORY = os.path.join('pantry', 'collabfinder', 'current', 'project', 'projects')

def _backgrounds(html):
    'This project needs...'
    return map(unicode, html.xpath('id("seeking")/descendant::b/text()'))

def _description(html):
    '''
    What are you making?
    Why are you making it?
    What do you need help with?
    '''
    questions =['what', 'why', 'need']
    answers = map(unicode, html.xpath('//div[@class="column span-18 append-1 border_t_g first last"]/h2[@class="plain"]/text()'))
    if len(answers) == 3:
        return dict(zip(questions, answers))

def _goals(html):
    'Project Goals'
    return map(unicode, html.xpath('id("project_goals")/li/text()'))

def _tags(html):
    'Tags'
    return map(unicode, html.xpath('//ul[@class="bottomend-1 attributes tags"]/li/a/text()'))

def _github(html):
    'Project Github'
    results = html.xpath('//h2[@class="toppend-1 border_t_g"]/a/text()')
    if len(results) == 1:
        return unicode(results[0])

def _answers(projectId, html):
    return {
        'projectId': projectId,
        'backgrounds': _backgrounds(html),
        'description': _description(html),
        'goals': _goals(html),
        'tags': _tags(html),
        'github': _github(html),
    }

def answers():
    'Get the answers to all the questions for all the projects.'
    # Loop through file names
    for filename in os.listdir(DOWNLOAD_DIRECTORY):
        raw = open(os.path.join(DOWNLOAD_DIRECTORY, filename)).read()
        if raw == '':
            continue
        yield _answers(int(filename), fromstring(raw))

if __name__ == '__main__':
    import sys
    import json
    json.dump(list(main()), open(os.path.join('output', 'projects.json'), 'w'))
