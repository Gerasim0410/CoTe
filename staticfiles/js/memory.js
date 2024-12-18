// Controls memorization phase, sets timer for it
// Displays new question (word)
// Selects and submits answers
const questions = JSON.parse(document.getElementById('questions').textContent);
const timer_seconds = JSON.parse(document.currentScript.dataset.timer_seconds);

let currentQuestionIndex = 0;
let currentWordIndex = 0;
let answers = [];
let selected = false;
let timeLeftRemember;
 
function startMemorizationPhase() {
    timeLeft = 15;
    const questionElement = document.getElementById('question');
    questionElement.textContent = 
    ` Запомните эти слова:\n ${questions[0].words_to_remember.join(', ')}`;
    document.getElementById('answers').style.display = 'none';
    timeLeftRemember = 15;
    const buttons = document.querySelectorAll('button.col');
    buttons.forEach(button => {
        button.style.display = 'none';
    });
    timer_rem = setInterval(function () {
        timeLeftRemember -= 0.01;
        timeLeftRemember = 
        Math.round((timeLeftRemember + Number.EPSILON) * 1000) / 1000
        console.log(timeLeftRemember);
        if (timeLeftRemember <= 0) {
            clearInterval(timer_rem);
            startWordSequencePhase();
            buttons.forEach(button => {
                button.style.display = 'block';
            });
        }
    }, 10);
}

function startWordSequencePhase() {
    document.getElementById('answers').style.display = 'block';
    const question = document.getElementById('question');
    question.textContent = `Это слово надо было запомнить?`;


    displayQuestion();
}

function displayQuestion() {
    const questionElement = document.getElementById('answer');
    const currentQuestion = questions[0];
    questionElement.textContent = 
    currentQuestion.words_seq[currentWordIndex];
    resetTimer();
}

function selectAnswer(arg) {
    const currentQuestion = questions[0];

    if (arg==0) {
        answers.push({
            selectedAnswer: -1,
            time_taken: Math.round(
                (timer_seconds - timeLeft + Number.EPSILON) * 100) / 100,
        });
    } else if (arg==1) {
        answers.push({
            selectedAnswer: currentWordIndex,
            time_taken: Math.round(
                (timer_seconds - timeLeft + Number.EPSILON) * 100) / 100,
        });
    } else {
        answers.push({
            selectedAnswer: null,
            time_taken: Math.round(
                (timer_seconds - timeLeft + Number.EPSILON) * 100) / 100,
        });
    };
        
    currentWordIndex++;
    if (currentWordIndex < currentQuestion.words_seq.length) {
        selected = true;
        document.getElementById('answer-catched')
        .textContent = "Ответ сохранен";
        Array.from(document.getElementsByTagName('button'))
        .forEach((button) => {button.disabled = true;})
    } else {
        submitAnswers();
    }
}

// Start the test with the memorization phase
startMemorizationPhase();
