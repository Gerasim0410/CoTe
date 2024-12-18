function selectAnswer(arg) {
    console.log(arg)
    currentQuestionIndex++;
    if (currentQuestionIndex >= questions.length) {submitAnswers();}
};
