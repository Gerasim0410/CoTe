const test = document.getElementsByTagName('script')[1].dataset.test_name;
if (test.includes("stroop")) {
const socket = new WebSocket(`ws://${window.location.host}/ws/quiz/`);
socket.onopen = function() {
    socket.send(JSON.stringify({
        type: "instr",
        test: window.document.baseURI
    }))
}
socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const button = document.getElementsByClassName('btn-primary mt-2')[0];
    button.firstChild.href = data.url;
}
}
