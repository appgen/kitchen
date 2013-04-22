#!/usr/bin/env python2
import os
from lxml.html import fromstring, HTMLParser

DOWNLOAD_DIRECTORY = os.path.join('pantry', 'collabfinder', 'current', 'projects')

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

HTML_PARSER = HTMLParser(encoding = 'utf-8')
def answers():
    'Get the answers to all the questions for all the projects.'
    # Loop through file names
    for filename in os.listdir(DOWNLOAD_DIRECTORY):
        raw = open(os.path.join(DOWNLOAD_DIRECTORY, filename)).read().decode('utf-8')
        if raw == '':
            continue
        yield _answers(int(filename), fromstring(raw, parser = HTML_PARSER))

if __name__ == '__main__':
    import sys
    import json
    print json.dumps(list(answers()))
