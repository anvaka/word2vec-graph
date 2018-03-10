# word2vec graph

* [Wikipedia visualization](https://anvaka.github.io/pm/#/galaxy/word2vec-wiki?cx=-7912&cy=-941&cz=-5655&lx=-0.3936&ly=-0.6815&lz=0.0636&lw=0.6137&ml=150&s=1.75&l=1&v=d50) - 6.9 MB
* [Common Crawl visualization](https://anvaka.github.io/pm/#/galaxy/word2vec-crawl?cx=-2411&cy=6376&cz=-7215&lx=0.0797&ly=-0.8449&lz=-0.4924&lw=0.1930&ml=150&s=1.75&l=1&v=d300) - 28.4MB

word2vec is a family of algorithms that allow you to find embeddings of words
into high-dimensional vector spaces.

```
// For example
cat => [0.1, 0.0, 0.9]
dog => [0.9, 0.0, 0.0]
cow => [0.6, 1.0, 0.5]
```

Vectors with shorter distances between them usually share comon contexts in the
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

*Note* From parcical standpoint, searching all nearest neghbours in high dimensional
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
much faster especially on the multithreaded CPU.

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

