from __future__ import print_function

import re
# Install from https://github.com/spotify/annoy
from annoy import AnnoyIndex

# Ignore all vectors with distance larger than this:
threshold = 0.9

# unpack your data from https://nlp.stanford.edu/projects/glove/
# Make sure to update `dimensions` according to embedded vector dimension
input_vectors = "graph-data/glove.840B.300d.txt"

# This file will contain nearest neighbors, one per line:
# node [tab char] neighbor_1 neighbor_2 ...

out_file = "graph-data/edges.txt"

# How many dimension in the vector space
dimensions = 300

# How many trees do want to use for `AnnoyIndex`
max_trees = 50

with open(input_vectors) as input_file:
    content = input_file.readlines()

word_id = 0
words = []
word_index = AnnoyIndex(dimensions)

for line in content:
    line_items = line.split(' ')
    word = line_items[0]
    # There are a lot of words with numbers (dates, years) - and they are not very intersting to me.
    # There are also ~140K instances of words with non-word characters, so we are going to ignore them
    # as well
    if re.search('[0-9\W]', word):
        continue

    words.append(word)
    vectors = [float(x) for x in line_items[1:]]
    word_index.add_item(word_id, vectors)
    word_id += 1

word_index.build(max_trees)

# If you want to save index:
# word_index.save('crawl_50_clean.ann')

# If you want to load index:
# u1 = AnnoyIndex(dimensions)
# u1.load('crawl_50_clean.ann')

# naive test:
# result = word_index.get_nns_by_item(words.index('dog'), 42, include_distances=True)
# result = zip(result[0], result[1])
# print([(words[x], dist) for x, dist in result]) # will find the 1000 nearest neighbors

out = open(out_file,'w')

for idx in range(len(words)):
    word = words[idx]
    result = word_index.get_nns_by_item(idx, 42, include_distances=True)
    pairs = zip(result[0], result[1])
    edges = [words[pair[0]] for pair in pairs if (words[pair[0]] != word) and (pair[1] < threshold)]
    if len(edges) > 0:
        out.write(word + '\t' + " ".join(edges) + '\n')

    if idx % 10000 == 0:
        print(idx)

out.close()

print("All done")
