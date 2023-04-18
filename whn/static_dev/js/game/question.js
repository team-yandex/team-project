const questionId = JSON.parse(document.getElementById('question-id').textContent)

const questionSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/session/'
    + questionId 
    + '/'
);

questionSocket.onopen = function(e) {
    questionSocket.send(JSON.stringify({'questionId': questionId}))   
}



questionSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.hasOwnProperty('end') && data.end) {
        questionSocket.close()
        console.log(123123131)
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
        var left = document.querySelector('#answer-time').innerText
        console.log(left, typeof left)
        const p = document.createElement('p');
        p.setAttribute('id', 'timer');
        video.play();
        video.addEventListener('ended', function() {
            block.appendChild(p);
            setInterval(function () {
                if (left == 1) {clearInterval(this);}
                p.innerText = left;
                left -= 1;
            }, 800)
        })
    }
};

questionSocket.onclose = function(e) {
    console.log('Socket closed')
};
