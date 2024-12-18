// Resets the timer, displays question
const questions = JSON.parse(document.getElementById('questions').textContent);
const timer_seconds = JSON.parse(document.currentScript.dataset.timer_seconds);

let currentQuestionIndex = 0;

function displayQuestion() {
    console.log(document.getElementById('question-image'));
    const questionImageElement = document.getElementById('question-image');
    const answersElement = document.getElementById('answers');
    const currentQuestion = questions[currentQuestionIndex];

    // Set the question image based on the question number
    const questionNumber = parseInt(currentQuestion.question);
    questionImageElement.src = `/static/raven/v${questionNumber}.jpg`;
    console.log(questionImageElement.src);

    // Clear previous answers
    answersElement.innerHTML = '';

    // Reset the timer whenever a new question is displayed
    resetTimer();
}

displayQuestion();
