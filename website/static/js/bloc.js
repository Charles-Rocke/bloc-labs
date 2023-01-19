var svg = document.getElementsByTagName("svg")[0];
var bbox = svg.getBBox();

var viewBox;

if (bbox.width > bbox.height) {
  viewBox = [bbox.x, bbox.y - (bbox.width - bbox.height) / 2, bbox.width, bbox.width].join(" ")
} else if (bbox.width < bbox.height) {
  viewBox = [bbox.x - (bbox.height - bbox.width) / 2, bbox.y, bbox.height, bbox.height].join(" ")
} else {
  viewBox - [bbox.x, bbox.y, bbox.width, bbox.height].join(" ");
}
svg.setAttribute("viewBox", viewBox);
prompt("Copy to clipboard: Ctrl+C, Enter", svg.outerHTML);