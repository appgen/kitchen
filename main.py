#!/usr/bin/env python2
import socrata, write
from helpers import cache
from combine import union

# Load source data
# viewdict = cache('viewdict', socrata.viewdict)
# columndict = cache('columndict', socrata.columndict)

print('Building union dict')
uniondict = cache('uniondict', socrata.uniondict)

print('Building copy generators')
generators = write.build_generators()

# Limit memory usage
# http://stackoverflow.com/questions/2308091/how-to-limit-python-heap-size
MEM_GB = 10
import resource
rsrc = resource.RLIMIT_DATA
soft, hard = resource.getrlimit(rsrc)
resource.setrlimit(rsrc, (MEM_GB * (2 ** 30), hard))

# Generate the files.
import json
for schema, viewids in uniondict.items():
    print('Appifying schema ' + json.dumps(schema))
    try:
        union(generators, viewids)
    except:
        print 'The offending function call:'
        print 'union(generators, ' + unicode(viewids) + ')'
        raise
