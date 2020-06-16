function copy() {
    let markdownDiv = document.getElementById("markdown");

    let text = markdownDiv.innerText;
    navigator.clipboard.writeText(text).then(function () {
        console.log('Async: Copying to clipboard was successful!');
    }, function (err) {
        console.error('Async: Could not copy text: ', err);
    });
}

