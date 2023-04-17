// import $ from '../jquery-3.6.4'


const session_id = $('#session_id').text()
console.log(session_id)

const socket = new WebSocket(
  'ws://'
  + window.location.host
  + '/ws/room/'
  + session_id
  + '/'
)

socket.onopen = () => {
  socket.send(JSON.stringify({'session_id': session_id}))
}

var truth = ''

socket.onmessage = (message) => {
  const data = JSON.parse(message.data)
  if (data.hasOwnProperty('users')) {
    const users = $('#user-list')
    users.empty()
    for (let user of data.users) {
      let li = $('<li>')
      li.attr('class', 'list-group-item')
      li.text(user)
      users.append(li)
    }
  } else if (data.hasOwnProperty('question') && data.hasOwnProperty('video')) {
    $.ajax({
      url: location.protocol + '//' + location.host + '/session/question/' + data.question + '/',
      method: 'GET',
      success: (response) => {
        $('#container').empty()
        $('#container').append($.parseHTML(response))
        $('#question-video').attr('src', data.video)
        $('#question-video')[0].load()

        for (const choice of data.choices) {
          let btn = $('<button>')
          btn.attr('id', 'choice_' + choice.id)
          btn.attr('class', 'btn btn-ans trd-ans')
          btn.text(choice.label)
          btn.on('click', () => {
            socket.send(JSON.stringify({event: 'answer', answer: choice.id}))
          })
          $('.ans-box').append(btn)
        }

        // TODO: remove hardcode by json_script
        var left = 5
        // TODO: beautify timer
        const p = $('<p>');
        p.attr('id', 'timer')
        $('#card-body-id').append(p)
        $('#question-video')[0].play()
        $('#question-video').on('ended', function() {
          setInterval(function () {
              p.text(left);
              left -= 1;
          }, 800)
        })
      }
    })
  } else if (data.hasOwnProperty('end')) {
    socket.send(JSON.stringify({event: 'answer', answer: ''}))
    $('#timer').remove()
    $('.ans-box').empty()
    $('#question-video').attr('src', data.end)
    $('#question-video')[0].load()
    $('#question-video')[0].play()

    if ($('#user_id').length) {
      let next = $('<button>')
      next.attr('id', 'next')
      next.attr('class', 'btn btn-ans fth-ans')
      next.text('Дальше')
      next.on('click', () => {
        socket.send(JSON.stringify({event: 'next'}))
      })
      $('#card-body-id').append(next)
    }
  } else if (data.hasOwnProperty('finish')) {
    console.log(data.finish)
    $('#container').empty()
    $('#container').append($('<h2>Результаты</h2>'))
    $('#container').append($("<ul id=leaderbord class='list-group'></ul>"))
    for (const user of data.finish) {
      console.log(user)
      let li = $('<li>')
      li.attr('class', 'list-group-item')
      li.text('Пользователь: ' + user[0] + ', очки: ' + user[1])
      $('#leaderbord').append(li)
    }
  } else if (data.hasOwnProperty('truth')) {
    let ans = $('<p>')
    ans.text(data.truth)
    $('#card-body-id').append(ans)
  }
}

$('#start').on('click', () => {
  socket.send(JSON.stringify({event: 'start'}))
})

socket.onclose = () => {
}
