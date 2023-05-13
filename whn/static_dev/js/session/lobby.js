const session_id = $('#session_id span').text()

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
        $('#question-video')[0].load() // hope it really loads syncronously
        socket.send(JSON.stringify({event: 'timer-begin'}))

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

        var left = $('#answer-time').text()
        const p = $('<p>')
        p.text(left)
        p.attr('id', 'timer')
        $('#question-video')[0].play()
        $('#question-video').on('ended', function() {
          $('#card-body-id').append(p)
          setInterval(function () {
              left -= 1;
              p.text(left);
          }, 1000)
        })
      }
    })
  } else if (data.hasOwnProperty('end')) {
    socket.send(JSON.stringify({event: 'answer', answer: ''}))
    $('#timer').remove()
    $('.ans-box').empty()
    $('#question-video').attr('src', data.end)
    $('#question-video')[0].load()
    $('#question-video').off('ended')
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
    $('#container').empty()
    $('#container').append($('<h2>Результаты</h2>'))
    $('#container').append($("<ul id=leaderbord class='list-group'></ul>"))
    for (const user of data.finish) {
      let li = $('<li>')
      li.attr('class', 'list-group-item')
      li.text(`Пользователь: ${user.username}, правильных: ${user.session_points}`)
      $('#leaderbord').append(li)
    }
  } else if (data.hasOwnProperty('success')) {
    let ans = $('#main-label')
    ans.text(data.success)
  } else if (data.hasOwnProperty('overloaded')){
    $('#container').empty()
    $('#container').append($('<h2>Свободных мест нет :(</h2>'))
  }
}

$('#start').on('click', () => {
  socket.send(JSON.stringify({event: 'start'}))
})

socket.onclose = () => {
  console.log('Socket was closed')
}
