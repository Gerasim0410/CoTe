let timer; 
const progressBar = document.getElementById('progress-bar');
const totalTime = parseFloat(progressBar.textContent); 
let questionStart = null;
let timeLeft = totalTime; // видимое значение, которое будет пересчитываться каждый тик

function resetTimer() {
    console.log('⏱ resetTimer');
    clearInterval(timer);
    questionStart = Date.now();

    timer = setInterval(function () {
        // пересчитываем оставшееся время на лету
        const elapsed = (Date.now() - questionStart) / 1000;
        timeLeft = Math.max(0, totalTime - elapsed); // чтобы значение не ушло в минус

        // обновляем прогрессбар
        const progressPercent = (timeLeft / totalTime) * 100;
        progressBar.style.width = progressPercent + '%';

        // если закончилось время
        if (timeLeft <= 0) {
            clearInterval(timer);
            timeLeft = 0; // фиксируем

            if (!selected) {
                selectAnswer(null); 
            }
            document.getElementById('answer-catched').textContent = "";

            const buttons = document.getElementsByTagName('button');
            if (buttons) {
                Array.from(buttons).forEach((button) => {
                    button.disabled = false;
                });
            }

            const image = document.getElementById('question-image');
            if (image) {
                image.onclick = null;
            }

            selected = false;
            displayQuestion();
        }
    }, 50); // 50 мс достаточно часто, без перегрузки
}

resetTimer();
