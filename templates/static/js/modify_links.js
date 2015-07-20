(function() {
  "use strict";
  var newLink = function newLink() {
    var linksPara = document.getElementById('links-paragraph');
    var linkSpan = libVoting.template('links-template');

    var lastSpan = linksPara.children[linksPara.children.length - 1];
    linksPara.insertBefore(linkSpan, lastSpan);
  };

  var deleteLink = function deleteLink(elem) {
    "use strict";
    elem.parentNode.removeChild(elem);
  }

  window.newLink = newLink;
  window.deleteLink = deleteLink;
})()
