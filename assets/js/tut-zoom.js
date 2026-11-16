/* Tutorials: a click on a screenshot opens it larger in a dialog, with its rings; a click anywhere or Esc closes it.
   Without JS the link opens the picture file itself. */
(function () {
  "use strict";
  var links = document.querySelectorAll(".tut-fig-zoom");
  var dialog = document.createElement("dialog");
  if (!links.length || typeof dialog.showModal !== "function") { return; }
  dialog.className = "tut-zoom";
  document.body.appendChild(dialog);
  dialog.addEventListener("click", function () { dialog.close(); });

  function open(link, event) {
    var pic = link.querySelector(".tut-fig-pic").cloneNode(true);
    event.preventDefault();
    pic.querySelector("img").removeAttribute("loading");
    dialog.replaceChildren(pic);
    dialog.showModal();
  }

  Array.prototype.forEach.call(links, function (link) {
    link.addEventListener("click", function (event) { open(link, event); });
  });
})();
