(function() {
  "use strict";
  var newAnswer = function newAnswer() {
    var ansPara = document.getElementById('answers-block');
    var ansSpan = window.libVoting.template('answers-template');
    var currentID;
    if (ansPara.children.length <= 1) {
      currentID = 'new0'
    } else {
      var lastAns = ansPara.children[ansPara.children.length - 2];
      currentID = 'new' +
        (parseInt(lastAns.getAttribute('data-id').substring(3)) + 1);
    }

    ansSpan.setAttribute('data-id', currentID);
    ansSpan.children[0].name = ansSpan.children[0].name.replace('new0', currentID);
    for (var i = 2; i < ansSpan.children.length; i++) {
      var systemDiv = ansSpan.children[i];
      systemDiv.children[0].id = systemDiv.children[0].id.replace('new0', currentID);
      systemDiv.children[0].name = systemDiv.children[0].name.replace('new0', currentID);
      systemDiv.children[1].setAttribute('for',
        systemDiv.children[1].getAttribute('for').replace('new0', currentID));
    };

    var lastElement = ansPara.children[ansPara.children.length - 1];
    ansPara.insertBefore(ansSpan, lastElement);
  };

  var deleteAnswer = function deleteAnswer(elem) {
    "use strict";
    elem.parentNode.removeChild(elem);
  }

  window.newAnswer = newAnswer;
  window.deleteAnswer = deleteAnswer;
})();
