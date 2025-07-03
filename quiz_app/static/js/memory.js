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
    console.log("🔁 Вызов startMemorizationPhase");

    // Скрываем прогресс-бар
    document.querySelector('.progress-container').style.visibility = 'hidden';

    const duration = 15;
    const questionElement = document.getElementById('question');
    questionElement.textContent = 
        `Запомните эти слова:\n ${questions[0].words_to_remember.join(', ')}`;

    document.getElementById('answers').style.display = 'none';

    const buttons = document.querySelectorAll('button.col');
    buttons.forEach(button => {
        button.style.display = 'none';
    });

    const startTime = Date.now();
    console.log("⏳ Устанавливаем setInterval на memorization phase");

    timer_rem = setInterval(function () {
        const elapsed = (Date.now() - startTime) / 1000;
        timeLeftRemember = Math.max(0, duration - elapsed);
        console.log('⏳ timeLeftRemember:', timeLeftRemember);

        if (timeLeftRemember <= 0) {
            console.log("💥 Завершение фазы запоминания");
            clearInterval(timer_rem);

            // Показываем прогресс-бар обратно
            document.querySelector('.progress-container').style.visibility = 'visible';

            startWordSequencePhase();
            buttons.forEach(button => {
                button.style.display = 'block';
            });
        }
    }, 50);
}


function startWordSequencePhase() {
    console.log('➡️ startWordSequencePhase');
    document.getElementById('answers').style.display = 'block';
    const question = document.getElementById('question');
    question.textContent = `Было ли слово?`;

    displayQuestion();
}

function displayQuestion() {
    console.log('📋 displayQuestion', currentWordIndex);
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
