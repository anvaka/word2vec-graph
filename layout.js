var createLayout = require('ngraph.offline.layout');
var loadGraph = require('./loadBinGraph.js');

loadGraph('./graph-data/labels.json', './graph-data/links.bin')
  .then(graph => {
    console.log(graph.getLinksCount() + ' edges');
    var layout = createLayout(graph, {
      outDir: './graph-layout',
    });
    layout.run();
  });
