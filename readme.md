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
