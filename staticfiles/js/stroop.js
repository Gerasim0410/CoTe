// displays question and answers
// resets the timer
const questions = JSON.parse(document.getElementById('questions').textContent);
const timer_seconds = JSON.parse(document.currentScript.dataset.timer_seconds);

let currentQuestionIndex = 0;

function displayQuestion() {
    const questionElement = document.getElementById('question');
    const answersElement = document.getElementById('answers');
    const currentQuestion = questions[currentQuestionIndex];

    // Display the word in the mismatched color
    questionElement.textContent = currentQuestion.question;
    questionElement.style.color = currentQuestion.word_color;

    // Clear previous answers
    answersElement.innerHTML = '';

    // Display multiple-choice buttons with Russian labels and values
    currentQuestion.answers.forEach((answer) => {
        const btn = document.createElement('button');
        btn.className = 'answer-btn';
        btn.style.backgroundColor = answer[0];
        btn.onclick = function() {
            selectAnswer(answer[1]);  
        };
        answersElement.appendChild(btn);
    });

    // Reset the timer whenever a new question is displayed
    resetTimer();
}

// Start by displaying the first question and resetting the timer
displayQuestion();
