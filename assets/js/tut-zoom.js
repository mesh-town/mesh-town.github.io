/* Tutorials: a click on a screenshot opens it larger in a dialog; a click anywhere or Esc closes it.
   Without JS the link opens the picture file itself. */
(function () {
  "use strict";
  var links = document.querySelectorAll(".tut-fig-zoom");
  var dialog = document.createElement("dialog");
  if (!links.length || typeof dialog.showModal !== "function") { return; }
  var img = document.createElement("img");
  dialog.className = "tut-zoom";
  dialog.appendChild(img);
  document.body.appendChild(dialog);
  dialog.addEventListener("click", function () { dialog.close(); });

  function open(link, event) {
    var small = link.querySelector("img");
    event.preventDefault();
    img.src = small.currentSrc || small.src;
    img.alt = small.alt;
    dialog.showModal();
  }

  Array.prototype.forEach.call(links, function (link) {
    link.addEventListener("click", function (event) { open(link, event); });
  });
})();
