import socrata
from helpers import cache
from combine import union

# viewdict = cache('viewdict', socrata.viewdict)
# columndict = cache('columndict', socrata.columndict)
# generators = cache('generators', write.build_generators)

uniondict = cache('uniondict', socrata.uniondict)
for schema, viewids in uniondict.items():
    union(viewids)
