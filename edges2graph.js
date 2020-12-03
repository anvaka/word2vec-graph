let edgesFileName = process.argv[2] || './graph-data/edges.txt';
let forEachLine = require('for-each-line');
var graph = require('ngraph.graph')();
var saveGraph = require('ngraph.tobinary');

forEachLine(edgesFileName, (line) => {
  var parts = line.split('\t');
  if (parts.length !== 2) {
    console.log('Something is wrong here: ', line);
    return;
  }
  var destinations = parts[1].split(' ');
  for (var i = 0; i < destinations.length; ++i) {
    graph.addLink(parts[0], destinations[i]);
  }
}).then(() => {
    console.log('Done!')

    saveGraph(graph, {
      outDir: './graph-data',
      labels: 'labels.json', 
      meta: 'meta.json',
      links: 'links.bin'
    });
});
