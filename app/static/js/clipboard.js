function copy() {
    var markdownDiv = document.getElementById("markdown");

    var text = markdownDiv.innerText;
    navigator.clipboard.writeText(text).then(function () {
        console.log('Async: Copying to clipboard was successful!');
    }, function (err) {
        console.error('Async: Could not copy text: ', err);
    });

