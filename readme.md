Kitchen: Convert raw data into a JSON file per app
====

Run `startuppidy.py` to build one JSON file per app in the `comestibles`
directory. This file runs everything else in the directory.

## Architecture
Data from Socrata comes as views and rows.
We group datasets from Socrata based on their unionability, joinabality, &c.
We combine each group into *enriched datasets*.

We use other data sources to generate copy for each dataset. Specifically,
we currently use Collabfinder submissions. This is incorporated into the
enriched datasets.

Enriched datasets are saved as two files, each with the same base name.
The base name is a number that is used as a random seed. The two extensions
are `csv`, for the table, and `json` for associated metadata. These files
go into the `comestibles` directory.

## Copy-writing approach
For the copy-writing, I had envisioned parsing the text into a grammatical
tree, formulating the various trees into a grammar and generating text that
matched that structure, weighting the random text generation towards the
app name and the app topic for appropriate parts of speech. These pages might
help.

* http://nltk.googlecode.com/svn/trunk/doc/book/ch09.html
* http://stackoverflow.com/questions/15009656/how-to-use-nltk-to-generate-sentences-from-an-induced-grammar

A simpler approach might be an n-gram model on the part-of-speech-tagged
sentences, randomly switching appropriate words for the app name and topic.
I'd build one model for the first sentences and a separate model for the
full dataset, and I'd use the output of the first model as a context for
the second.

## Joining datasets
To do: Allow for fuzzier column name matches. For example, "Building Address"
should match "building_address", "NEIGHBORHOOD" should match "Neighborhood" and
"Building Tax Expenses" should match "Bldg tax expenses".

## Other notes
The metadata field in the view json is crazy.
