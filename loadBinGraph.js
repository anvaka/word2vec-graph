var fs = require('fs');
var createGraph = require('ngraph.graph');

module.exports = loadGraph;

function loadGraph(labelsFile, linksFile) {
  var graph = createGraph();
  return new Promise((resolve, reject) => {
    var labels = require(labelsFile);
    labels.forEach(label => graph.addNode(label));

    var links = fs.readFileSync(linksFile);
    var from;
    for (var i = 0; i < links.length; i += 4) {
      var id = links.readInt32LE(i);
      if (id < 0) from = labels[-(id + 1)];
      else {
        if (!id) throw new Error('missing edge id?');
        graph.addLink(from, labels[id - 1]);
      }
    }
    resolve(graph);
  });
}

