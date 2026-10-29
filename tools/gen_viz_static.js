/* Generator: writes assets/viz/static.svg and static-narrow.svg (the step-5 state, no packets).

Usage: node tools/gen_viz_static.js .   (from the repository root, Node stdlib only)
*/
'use strict';
var fs = require('fs');
var path = require('path');
var scene = require(path.resolve(__dirname, '../assets/viz/scene.js'));

var root = path.resolve(process.argv[2] || '.');
var dir = path.join(root, 'assets', 'viz');
var css = fs.readFileSync(path.join(dir, 'viz-scene.css'), 'utf8')
  .replace(/\/\*[\s\S]*?\*\//g, '')
  .replace(/\s*\n\s*/g, '')
  .replace(/\s*([{};,:])\s*/g, '$1');
var style = scene.staticStyle() + css;

[['h', 'static.svg'], ['v', 'static-narrow.svg']].forEach(function (pair) {
  var svg = scene.build(pair[0], { cls: 'net links name static', style: '--p:1', css: style });
  fs.writeFileSync(path.join(dir, pair[1]), svg + '\n');
  console.log('wrote ' + path.join('assets', 'viz', pair[1]) + ' (' + Buffer.byteLength(svg) + ' bytes)');
});
