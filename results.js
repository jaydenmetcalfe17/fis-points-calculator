window.onload = function() {
    var output = localStorage.getItem('output');
    console.log('Retrieved output from local storage:', output);
    document.getElementById('outputContainer').innerText = output;
  };