// Creates and displays word matrix
// Submits and displays words
// Selects and submits answers
const questions = JSON.parse(document.getElementById('questions').textContent);
const timer_seconds = JSON.parse(document.currentScript.dataset.timer_seconds);

const matrix = questions[0]['matrix'];
const wordsToFind = questions[0]['correct_answer'];

let submittedWords = [];
let answers;
let selected = false;

function displayQuestion() {};

// Populate matrix on the screen
function createMatrix() {
    const matrixContainer = document.getElementById('matrix');
    matrix.forEach(row => {
        row.forEach(letter => {
            const letterElement = document.createElement('div');
            letterElement.className = 'letter';
            letterElement.textContent = letter;
            matrixContainer.appendChild(letterElement);
        });
    });
}

function submitWord() {
    const input = document.getElementById('word-input');
    const word = input.value.trim().toLowerCase();
        
    if (word && wordsToFind.includes(word) && 
        !submittedWords.includes(word)) {
        submittedWords.push(word);
        updateSubmittedWords();
    }
    input.value = '';  // Clear input after submission
}

// Display the submitted words on the screen
function updateSubmittedWords() {
    const listElement = document.getElementById('submitted-words-list');
    listElement.innerHTML = '';  // Clear previous words
    submittedWords.forEach(word => {
        const wordElement = document.createElement('li');
        wordElement.textContent = word;
        listElement.appendChild(wordElement);
    });
}

function selectAnswer(args) {
    const timeElapsed = timer_seconds - timeLeft;  
    answers = {
        selectedAnswer: submittedWords,
        time_taken: timeElapsed
    };
    submitAnswers();
}

createMatrix();
