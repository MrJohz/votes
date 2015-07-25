(function() {
  "use strict";

  window.libVoting = {
    toElement: function(string) {
      var containerElem = document.createElement('div');
      containerElem.innerHTML = string;
      if (containerElem.children.length == 1) {
        return containerElem.children[0];
      } else {
        return containerElem.children;
      }
    },
    template: function(id) {
      return this.toElement(document.getElementById(id).innerHTML);
    }
  }
})();
