import asyncio
import json

import asgiref.sync
import channels.db
import channels.generic.websocket
import django.conf
import django.utils

import game.models


class QuestionConsumer(channels.generic.websocket.AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.question = None

    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        print('hello')  # noqa
        await asgiref.sync.sync_to_async(self.scope['session'].__setitem__)(
            'start_datetime', str(django.utils.timezone.now())
        )
        await asgiref.sync.sync_to_async(self.scope['session'].save)()
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        if self.question is None:
            # first message is question id
            # TODO: handle if there is no questionId
            question_id = data['questionId']
            self.question = await channels.db.database_sync_to_async(
                self.get_question
            )(question_id)
            message = json.dumps({'url': self.question.climax_video.url})
            await self.send(message)
            await asyncio.sleep(
                self.question.climax_second
                + django.conf.settings.ANSWER_BUFFER_SECONDS
            )
            end_message = json.dumps(
                {'end': True, 'url': self.question.video.url}
            )
            await self.send(end_message)
            return

    def get_question(self, question_id):
        return (
            game.models.Question.objects.published()
            .filter(pk=question_id)
            .first()
        )
