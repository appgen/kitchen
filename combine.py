import json, os, re, random
import pandas
import write, socrata
from keywords import get_keywords

VIEWS = os.path.join('pantry', 'socrata', 'views')
ROWS = os.path.join('pantry', 'socrata', 'rows')

PREFIXES = [u"responsive", u"game", u"beta", u"tech", u"digital", u"social", u"my", u"our", u"the", u"all", u"in", u"on"]
SUFFIXES = [u"box", u"grid", u"share", u"wise", u"hop", u"works", u"bit", u"book", u"list", u"square", u"rock", u"ly", u"sy", u"er", u"it", u"ie", u"io", u"am", u"ia", u"ora", u"ero", u"ist", u"ism", u"ium", u"ble", u"ify", u"ous", u"ing"]

def _not_nyc_department(tag):
    'Check whether a tag is a word.'
    return tag not in {u'dob'}

def _app_name(tags):
    if len(tags) == 0:
        raise ValueError

    good_tags = filter(_not_nyc_department, tags)
    tag = random.sample(good_tags, 1)[0]
    construction_scheme = random.randint(1,3)

    if construction_scheme == 1:
        # Add prefix
        name = random.sample(PREFIXES, 1)[0] + tag.split(' ')[0]

    elif construction_scheme == 2:
        # Add suffix
        name = random.sample(tag.split(' ')[-1] + random.sample(SUFFIXES, 1)[0], 1)[0]

    elif construction_scheme == 3:
        # Remove last vowel
        _reversed_name = ''.join(reversed(list(tag.split(' ')[-1])))
        name = ''.join(reversed(re.sub(r'[aoeui]', '', _reversed_name, count = 1)))

    if len(name) > 3:
        return name
    else:
        return _app_name(tags)

def _seed_text(keywords):
    return ' '.join(random.sample(keywords, 3))

def _add_viewid_column(viewid, df):
    df['source_dataset_viewid'] = viewid
    return df

def _union(viewids):
    data = [_add_viewid_column(viewid, pandas.read_csv(os.path.join(ROWS, viewid))) for viewid in viewids]
    return pandas.concat(data)

def _combiner(func, funcname):
    'Create a combiner function'
    def g(generators, viewids):
        'Turn the viewids into a single dataset, with metadata in a json and data in a csv. The base name of the resulting files is returned.'
        seed = hash(funcname + ','.join(sorted(viewids)))
        print seed

        geojson_file = os.path.join('comestibles', '%d.geojson' % seed)
        json_file = os.path.join('comestibles', '%d.json' % seed)
        csv_file = os.path.join('comestibles', '%d.csv' % seed)

        print 'Combining the data'
        df = func(viewids)

        print 'Extracting geospatial coordinates'
        df = socrata.parse_shape(df)

        # Save CSV data
        if not os.path.exists(csv_file):
            df.to_csv(csv_file)

        # Save geoJSON if the dataset is a small map.
        if {'Longitude', 'Latitude'}.issubset(set(df.columns)) and df.shape[0] < 10000 and not os.path.exists(geojson_file):
            feature_collection = { "type": "FeatureCollection",
                                   "features": [] }
            for i in df.index:
                properties = df.ix[i].to_dict()
                feature = { "type": "Feature",
                            "geometry": {"type": "Point", "coordinates": [properties.pop('Longitude'), properties.pop('Latitude')]},
                          }
                feature["properties"] = properties
                feature_collection['features'].append(feature)
            json.dump(feature_collection, open(geojson_file, 'w'))

        if not os.path.exists(json_file):
            # Source JSON metadata
            metadata = {
                'seed': seed,
                'sources': [json.load(open(os.path.join(VIEWS, viewid))) for viewid in viewids],
            }

            # Create more metadata
            keywords = list(get_keywords(*metadata['sources']))
            name = _app_name(keywords)

            metadata.update({
                'name': name,
                'keywords': keywords,
                'combined_title': socrata.combine_titles(metadata['sources']),
                'logo': None,
                'collabfinder_what': write.generate(generators, _seed_text(keywords), 'what'),
                'collabfinder_why': write.generate(generators, _seed_text(keywords), 'why'),
                'collabfinder_need': write.generate(generators, _seed_text(keywords), 'need'),
            })

            json.dump(metadata, open(json_file, 'w'))

    return g

# Exposed functions
union = _combiner(_union, 'union')
