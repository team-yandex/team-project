const questionId = JSON.parse(document.getElementById('question-id').textContent)

const questionSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/session/'
    + questionId // TODO: session id
    + '/'
);

questionSocket.onopen = function(e) {
    questionSocket.send(JSON.stringify({'questionId': questionId}))   
}

questionSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.hasOwnProperty('end') && data.end) {
        const form = document.querySelector('#form-id');
        form.parentNode.removeChild(form);
        const video = document.querySelector('#question-video');
        video.src = data.url;
        video.play();
    } else if (data.hasOwnProperty('url')) {
        const video = document.querySelector('#question-video');
        video.src = data.url;
        video.play();
    }
};

questionSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};
