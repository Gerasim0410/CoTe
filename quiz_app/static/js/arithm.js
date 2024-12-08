// Resets timer, displays (next) question
const questions = JSON.parse(document.getElementById('questions').textContent);
const timer_seconds = JSON.parse(document.currentScript.dataset.timer_seconds);
    
let currentQuestionIndex = 0;

function displayQuestion() {
    const questionElement = document.getElementById('question');
    const currentQuestion = questions[currentQuestionIndex];

    questionElement.textContent = currentQuestion.question;
    resetTimer();
}

displayQuestion();
