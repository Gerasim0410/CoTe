const mainData = document.currentScript.dataset
function submitAnswers() {
    // Send answers to the server via AJAX
    fetch(mainData.test_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': mainData.csrfToken,
        },
        body: JSON.stringify({ 
            answers: answers,
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        } else {
            alert(data.message);  
        }
    });
}
