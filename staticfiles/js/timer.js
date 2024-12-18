let timer; 
const progressBar = document.getElementById('progress-bar');
const totalTime = parseFloat(progressBar.textContent); 
let timeLeft = totalTime;
function resetTimer() {
    timeLeft = totalTime; 
    // progressBar.textContent = timeLeft.toFixed(1);
    clearInterval(timer);
    timer = setInterval(function () {
        timeLeft -= 0.01;
        // progressBar.textContent = timeLeft.toFixed(1);

        // Update the progress bar width
        const progressPercent = (timeLeft / totalTime) * 100;
        progressBar.style.width = progressPercent + '%';

        if (timeLeft <= 0) {
            console.log('in if');
            timeLeft = 0;
            clearInterval(timer);
            if (!selected) {
                selectAnswer(null); 
            }
            document.getElementById('answer-catched')
            .textContent = "";
            if (document.getElementsByTagName('button')) {
                Array.from(document.getElementsByTagName('button'))
                .forEach((button) => {
                    button.disabled = false;
                });
            }
            if (document.getElementById('question-image')) {
                Array.from(document.getElementById('question-image'))
                .forEach((button) => {
                    button.onclick = null;
                });
            }
            selected = false;
            displayQuestion();
        }
    }, 10);
}

resetTimer();
