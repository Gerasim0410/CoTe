const questions = JSON.parse(document.getElementById('questions').textContent)[0];
const timer_seconds = JSON.parse(document.currentScript.dataset.timer_seconds);

let currentQuestionIndex = 0;
let answers = [];
let selected = false;
const buttons = document.querySelectorAll('button.col');

function displayQuestion() {
    const shapesContainer = document.getElementById('shapes-container');
    const shapes = questions['shapes_seq'];
    const colors = questions['colors_seq'];
    const spatials = questions['spatials_seq'];

    shapesContainer.innerHTML = '';
    const shapeElement = document.createElement('div');
    shapeElement.className = 'shape ' + shapes[currentQuestionIndex]; 
    if (spatials[currentQuestionIndex] == "up") {shapeElement.className += ' higher'}
    else if (spatials[currentQuestionIndex] == "down") {shapeElement.className += ' lower'};
    shapeElement.style.color = colors[currentQuestionIndex]; 
    if (!shapeElement.className.includes('triangle')) {
        shapeElement.style.backgroundColor = colors[currentQuestionIndex];
    };
    shapesContainer.appendChild(shapeElement);
    shapeElement.hidden = false;
    shapesContainer.hidden = false;
    console.log(shapeElement.hidden);
    console.log(shapesContainer.hidden);
    show_figure = setTimeout(() => {
        shapeElement.hidden = true;
        shapesContainer.hidden = true;
        console.log(shapeElement.hidden);
        console.log(shapesContainer.hidden);
    }, 1000);

    buttons.forEach((button) => {
        if (currentQuestionIndex === 0) {
            button.style.display = 'none'; // Скрытие кнопок
        } else {
            button.style.display = 'block'; // Отображение кнопок
        }
    });

    resetTimer();
}

function selectAnswer(answer) {
    answers.push({
        selectedAnswer: answer,
        time_taken: Math.round(
          (timer_seconds - timeLeft + Number.EPSILON) * 1000) / 1000,
    });

    currentQuestionIndex++;
    if (currentQuestionIndex < questions['shapes_seq'].length) {
        selected = true;
        document.getElementById('answer-catched')
        .textContent = "Ответ сохранен";
        Array.from(document.getElementsByTagName('button'))
        .forEach((button) => {button.disabled = true;})
    } else {
        submitAnswers();
    }
}

displayQuestion();
