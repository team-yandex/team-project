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
        const form = document.querySelector('#card-body-id');
        document.querySelector('#timer').remove()
        const button = document.createElement('a');
        button.className += 'btn btn-trd';
        button.innerText = 'Заново';
        button.href = location.protocol + '//' + location.host + '/game/single/';
        form.parentNode.appendChild(button);
        form.parentNode.removeChild(form);
        const video = document.querySelector('#question-video');
        video.src = data.url;
        video.play();
    } else if (data.hasOwnProperty('url')) {
        const block = document.querySelector('#card-body-id').parentNode;
        const video = document.querySelector('#question-video');
        video.src = data.url;
        var left = 5
        // TODO: beautify timer
        const p = document.createElement('p');
        p.setAttribute('id', 'timer');
        block.appendChild(p);
        video.play();
        video.addEventListener('ended', function() {
            setInterval(function () {
                if (left == 1) {clearInterval(this);}
                p.innerText = left;
                left -= 1;
            }, 1000)
        })
    }
};

questionSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};
