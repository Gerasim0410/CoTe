const socket = new WebSocket(`ws://${window.location.host}/ws/quiz/`);
const questions = JSON.parse(document.getElementById('questions').textContent);
const timer_seconds = JSON.parse(document.currentScript.dataset.timer_seconds);
const test = document.currentScript.dataset.test_name;

let after_test_link;
let select_url;
let submit_url;
let group;
let answers;
let currentQuestionIndex = 0;
let selected = false;

// on opening send request to web socket to understand who we are
// (mobile device or big screen)
socket.onopen = function() {
    socket.send(JSON.stringify({ 
        type: "test_async", 
        test: test 
    }));
    console.log('Message sent');
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Data parsed');
    // depending on who we are we will receive different links
    // but will still need to use them almost in the same context
    if (data.test_url) {
        console.log('Got test_url');
        after_test_link = data.test_url;
        select_url = data.select_url;
        submit_url = data.submit_url;
        group = data.group;
        answers = {};
        [select_url, submit_url].forEach((elt) => {
            const scriptElement = document.createElement('script');
            scriptElement.src = elt;
            scriptElement.async = true;
            scriptElement.onload = () => 
                console.log('Script loaded successfully');
            document.body.appendChild(scriptElement);
        });
    } 
    if (data.redirect_url) {
        window.location.href = data.redirect_url;
    } else if (data.message) {
        alert(data.message);
    }
};

function displayQuestion() {
    const questionElement = document.getElementById('question');
    
    if (currentQuestionIndex < questions.length) {
    const currentQuestion = questions[currentQuestionIndex];
    questionElement.textContent = currentQuestion.question;
    }
    
    resetTimer();
}

displayQuestion();
