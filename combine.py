import pandas
VIEWS = os.path.join('pantry', 'socrata', 'views')
ROWS = os.path.join('pantry', 'socrata', 'rows')

def _union(viewids):
    data = [pandas.read_csv(os.path.join(ROWS, viewid)) for viewid in viewids]
    return pandas.concat(data)

def _combiner(func):
    'Create a combiner function'
    def g(viewids):
        seed = str(func) + ','.join(viewids)

        # Save CSV data
        df = func(viewids)
        df.to_csv(os.path.join('comestibles', '%d.csv' % seed))

        # Save JSON metadata
        metadata = {
            'seed': seed,
            'sources': [json.load(open(os.path.join(VIEWS, viewid))) for viewid in viewids],
        }
        json.dump(metadata, os.path.join('comestibles', '%d.json' % seed))

    return g

# Exposed functions
union = _combiner(_union)
