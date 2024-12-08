function submitAnswers() {
    const data = { 
      type: "test_submit_async", 
      group: group,
      test: test,
      answers: answers };
    socket.send(JSON.stringify(data));
}
