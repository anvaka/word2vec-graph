# word2vec graph

This visualization builds graphs of nearest neighbors from high-dimensional
word2vec embeddings.

![demo 1](https://i.imgur.com/dn0Egqo.gif)
![demo 2](https://i.imgur.com/Xtv1Haq.gif)
![demo words](https://i.imgur.com/zJKZEve.gif)

## Available Graphs

The dataset used for this visualization comes from [GloVe](https://nlp.stanford.edu/projects/glove/),
and has 6B tokens, 400K vocabulary, 300-dimensional vectors.

* [Distance < 0.9](https://anvaka.github.io/pm/#/galaxy/word2vec-wiki?cx=-4431&cy=3921&cz=-1124&lx=0.3701&ly=0.4218&lz=-0.0634&lw=0.8253&ml=300&s=1.75&l=1&v=d50_clean_small) -
In this visualization edge between words is formed when distance between corresponding
words' vectors is smaller than 0.9. All words with non-word characters and digits are removed.
The final visualization is sparse, yet meaningful.

* [Distance < 1.0](https://anvaka.github.io/pm/#/galaxy/word2vec-wiki?cx=88&cy=-10541&cz=1431&lx=0.1555&ly=0.6672&lz=-0.1453&lw=0.7139&ml=300&s=1.75&l=1&v=d50_clean) -
Similar to above, yet distance requirement is relaxed. Words with distance smaller than 1.0 are
given edges in the graph. All words with non-word characters and digits are removed. 
The visualization becomes more populated as more words are added. Still meaningful.

* [Raw; Distance < 0.9](https://anvaka.github.io/pm/#/galaxy/word2vec-wiki?cx=-7912&cy=-941&cz=-5655&lx=-0.3936&ly=-0.6815&lz=0.0636&lw=0.6137&ml=150&s=1.75&l=1&v=d50) (6.9 MB) -
Unlike visualizations above, this one was not filtered and includes all words from the
dataset. Majority of the clusters formed here have numerical nature. I didn't find this one
particularly interesting, yet I'm including it to show how word2vec finds numerical clusters.

### Common Crawl

I have also made a graph from Common Crawl dataset (840B tokens, 2.2M vocab, 300d vectors).
Words with non-word characters and numbers were removed.

Many clusters that remained represent words with spelling errors:

![spelling error](https://i.imgur.com/Ftj2Ce7.gif)

I had hard time deciphering meaning of many clusters here. Wikipedia embeddings were much more
meaningful. Nevertheless I want to keep this visualization to let you explore it as well:

* [Common Crawl visualization](https://anvaka.github.io/pm/#/galaxy/word2vec-crawl?cx=-2411&cy=6376&cz=-7215&lx=0.0797&ly=-0.8449&lz=-0.4924&lw=0.1930&ml=150&s=1.75&l=1&v=d300) - 28.4MB

# Intro and Details

[word2vec](https://en.wikipedia.org/wiki/Word2vec) is a family of algorithms
that allow you to find embeddings of words into high-dimensional vector spaces.

```
// For example
cat => [0.1, 0.0, 0.9]
dog => [0.9, 0.0, 0.0]
cow => [0.6, 1.0, 0.5]
```

Vectors with shorter distances between them usually share common contexts in the
corpus. This allows us to find distances between words:

```
|cat - dog| = 1.20
|cat - cow| = 1.48


"cat" is closer to "dog" than it is to the "cow".
```

## building a graph

We can simply iterate over every single word in the dictionary and add them into
a graph. But what would be an edge in this graph?

We draw an edge between two words if distance between embedding vectors is
shorter than a given threshold.

Once the graph is constructed, I'm using a method described here: [Your own graphs](https://github.com/anvaka/pm#your-own-graphs)
to construct visualizations.

*Note* From practical standpoint, searching all nearest neighbors in high dimensional
space is a very CPU intensive task. Building an index of vectors help. I didn't
know a good library for this task, so I [consulted Twitter](https://twitter.com/anvaka/status/971812468950487040).
Amazing recommendations by [@gumgumeo](https://twitter.com/gumgumeo) and [@AMZoellner](https://twitter.com/AMZoellner)
led to [spotify/annoy](https://github.com/spotify/annoy).


# Data

I'm using pre-trained word2vec models from the [GloVe](https://nlp.stanford.edu/projects/glove/)
project.


## Preprocessing

My original attempts to render `word2vec` graphs resulted in overwhelming presence
of numerical clusters. `word2vec` models really loved to put numerals together (and
I think it makes sense, intuitively). Alas - that made visualizations not very
interesting to explore. As I hoped from one cluster to another, just to find out
that one was dedicated to numbers `2017 - 2300`, while the other to `0.501 .. 0.403`

In Common Crawl word2vec encoding, I removed all words that had non-word characters
or numbers. In my opinion, this made visualization more interesting to explore, yet
still, I don't recognize a lot of clusters.

# Local setup

## Prerequisites

Make sure [`node.js`](https://nodejs.org/en/) is installed.

```
git clone https://github.com/anvaka/word2vec-graph.git
cd word2vec-graph
npm install
```

Install [spotify/annoy](https://github.com/spotify/annoy)

## Building graph file

1. Download the vectors, and extract them into graph-data
2. Modify `save_text_edges.py` to point to newly extracted vectors (see file
for more comments)
3. run `python save_text_edges.py` - depending on input vector file size
this make take a while. The output file `edges.txt` will be saved in the 
`graph-data` folder.
4. run `node edges2graph.js graph-data/edges.txt` - this will save graph in 
binary format into `graph-data` folder (graph-data/labels.json, graph-data/links.bin)
5. Now it's time to run layout. There are two options. One is slow, the other one is
much faster especially on the multi-threaded CPU.

### Running layout with node

You can use

```
node --max-old-space-size=12000 layout.js
```

To generate layout. This will take a while to converge (layout stops after 500 iterations).
Also note, that we need to increase maximum allowed RAM for node process
(`max-old-space-size` argument). I'm setting it to ~12GB - it was enough for my case

### Running layout with C++

Much faster version is to compile `layout++` module. You will need to manually
download and compile [`anvaka/ngraph.native`](https://github.com/anvaka/ngraph.native) package.

On ubuntu it was very straightforward: Just run `./compile-demo` and `layout++`
file will be created in the working folder. You can copy that file into this repository,
and run:

```
./layout++ ./graph-data/links.bin
```

The layout will converge much faster, but you will need to manually kill it (Ctrl + C)
after 500-700 iterations.

You will find many `.bin` files. Just pick the one with the highest number,
and copy it as `positions.bin` into `graph-data/` folder. E.g.:

```
cp 500.bin ./graph-data/positions.bin
```

That's it. Now you have both graph, and positions ready. You can use instructions from
[Your own graphs](https://github.com/anvaka/pm#your-own-graphs) to visualize your
new graph with `https://anvaka.github.io/pm/#/`

