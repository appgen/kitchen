import socrata, write
from helpers import cache
from combine import union

# viewdict = cache('viewdict', socrata.viewdict)
# columndict = cache('columndict', socrata.columndict)

print('Building union dict')
uniondict = cache('uniondict', socrata.uniondict)

print('Building copy generators')
generators = write.build_generators()

import json
for schema, viewids in uniondict.items():
    print('Appifying schema ' + json.dumps(schema))
    union(generators, viewids)
