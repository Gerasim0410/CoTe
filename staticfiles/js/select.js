// Selects and submit answers
let answers = [];
let selected = false;

function selectAnswer(answer) {
    // Capture the user's selected answer
    answers.push({
        selectedAnswer: answer, 
        time_taken: Math.round(
          (timer_seconds - timeLeft + Number.EPSILON) * 1000) / 1000,
    });

    // Block other answers or submit
    currentQuestionIndex++;
    if (currentQuestionIndex < questions.length) {
        selected = true;
        document.getElementById('answer-catched')
        .textContent = "Ответ сохранен";
        Array.from(document.getElementsByTagName('button'))
        .forEach((button) => {button.disabled = true;})
    } else {
        submitAnswers();
    }
}
