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
        console.log(response)
        $('#container').empty()
        $('#container').append($.parseHTML(response))
        console.log(data.video, $('#question_video'))
        $('#question-video').attr('src', data.video)
        $('#question-video')[0].load()

        console.log(data.choices)
        for (const choice of data.choices) {
          console.log(choice)
          let btn = $('<button>')
          btn.attr('id', 'choice_' + choice.id)
          btn.attr('class', 'btn btn-ans trd-ans')
          btn.text(choice.label)
          btn.on('click', () => {
            socket.send(JSON.stringify({event: 'answer', answer: choice.id}))
          })
          $('.ans-box').append(btn)
        }
        $('#question-video')[0].play()
      }
    })
  } else if (data.hasOwnProperty('end')) {
    socket.send(JSON.stringify({event: 'answer', answer: ''}))
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
  } else if (data.hasOwnProperty('truth')) {
    console.log(data.truth)
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
