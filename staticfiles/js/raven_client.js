// Resets the timer, displays question
const questions = JSON.parse(document.getElementById('questions').textContent);
const timer_seconds = JSON.parse(document.currentScript.dataset.timer_seconds);

let currentQuestionIndex = 0;

function displayQuestion() {

    // Reset the timer whenever a new question is displayed
    resetTimer();
}

displayQuestion();
