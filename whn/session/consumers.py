from asyncio import sleep
import json
import random

from asgiref.sync import sync_to_async
from channels.consumer import database_sync_to_async
import channels.generic.websocket
from django.utils import timezone
from session.models import Session
from whn.settings import ANSWER_BUFFER_SECONDS

from game.models import Choice, Question


class LobbyConsumer(channels.generic.websocket.AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.questions = []
        self.answered = False

    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']

        self.session = await self.get_session(self.session_id)
        await self.accept()
        if await self.is_avalaible():
            await self.channel_layer.group_add(
                self.session_id, self.channel_name
            )
            await self.add_user(self.scope['user'])
            message = {'type': 'connection'}
            await self.channel_layer.group_send(self.session_id, message)
        else:
            await self.send(text_data=json.dumps({'overloaded': True}))
            await self.close()

    async def connection(self, event):
        users = await self.get_all_users()
        await self.send(text_data=json.dumps({'users': users}))

    async def receive(self, text_data=None, bytes_data=None):
        # ээх, щас бы python 3.10 и pattern matching...

        data = json.loads(text_data or '{event: "None"}')
        event = data.get('event')
        if event == 'start':
            self.counter = 0
            await self.activate()
            await self.choose_questions(self.session.max_questions)
            message = {
                'type': 'get_question',
                'number': self.questions[self.counter],
            }
            await self.channel_layer.group_send(self.session_id, message)
        elif event == 'answer' and not self.answered:
            if await self.is_correct(data['answer']) is True:
                self.answered = True
                await self.send(json.dumps({'success': 'Вы были правы!'}))
                await self.update_score()
            elif await self.is_correct(data['answer']) is False:
                self.answered = True
                await self.send(
                    text_data=json.dumps({'success': 'Вы были неправы!'})
                )
            elif await self.is_correct(data['answer']) is None:
                self.answered = True
                await self.send(
                    text_data=json.dumps({'success': 'Вы не успели!'})
                )

        elif event == 'next':
            self.counter += 1
            if self.counter == len(self.questions):
                message = {'type': 'finish'}
                await self.channel_layer.group_send(self.session_id, message)
            else:
                message = {
                    'type': 'get_question',
                    'number': self.questions[self.counter],
                }
                await self.channel_layer.group_send(self.session_id, message)

    async def get_question(self, event):
        self.answered = False
        instance = await self.question_by_id(event['number'])
        await self.send(
            text_data=json.dumps(
                {
                    'question': instance.id,
                    'video': await self.get_video_by_id(instance.id),
                    'choices': await self.get_choices(instance.id),
                }
            )
        )
        await sync_to_async(self.scope['session'].__setitem__)(
            'start_datetime', str(timezone.now())
        )
        await sync_to_async(self.scope['session'].save)()
        await sleep(instance.climax_second + ANSWER_BUFFER_SECONDS)
        await self.send(text_data=json.dumps({'end': instance.video.url}))

    async def finish(self, event):
        await self.send(
            text_data=json.dumps({'finish': await self.final_leaderbord()})
        )

    async def disconnect(self, code):
        await self.disconnect_user()
        await self.channel_layer.group_send(
            self.session_id, {'type': 'connection'}
        )
        await sync_to_async(self.scope['session'].pop)(
            'question_id'
        )
        await sync_to_async(self.scope['session'].save)()
        return await super().disconnect(code)

    @database_sync_to_async
    def get_session(self, code):
        return Session.objects.get(code=code)

    @database_sync_to_async
    def is_avalaible(self):
        return (
            self.session.users.count() < self.session.max_users
            and self.session.status == Session.Status.UPCOMING
        )

    @database_sync_to_async
    def add_user(self, user):
        user.session_points = 0
        user.save()
        self.session.users.add(user)

    @database_sync_to_async
    def get_all_users(self):
        return list(self.session.users.values_list('username', flat=True))

    @database_sync_to_async
    def activate(self):
        self.session.status = Session.Status.ACTIVE
        self.session.save()

    @database_sync_to_async
    def choose_questions(self, amount):
        queryset = random.sample(
            list(
                Question.objects.published()
                .filter(complexity=self.session.complexity)
                .values_list('id', flat=True)
            ),
            k=amount,
        )
        self.questions = queryset

    @database_sync_to_async
    def get_video_by_id(self, id):
        obj = Question.objects.get(pk=id)
        return obj.climax_video.url

    @database_sync_to_async
    def question_by_id(self, id):
        return Question.objects.published().get(pk=id)

    @database_sync_to_async
    def get_choices(self, id):
        choices = Choice.objects.filter(question__pk=id)
        return [{'id': choice.pk, 'label': choice.label} for choice in choices]

    @database_sync_to_async
    def is_correct(self, id):
        if isinstance(id, str):
            return None
        choice = Choice.objects.get(pk=id)
        return choice.is_correct

    @database_sync_to_async
    def update_score(self):
        self.scope['user'].session_points += 1
        self.scope['user'].save()

    @database_sync_to_async
    def final_leaderbord(self):
        self.session.status = Session.Status.ENDED
        self.session.save()
        return sorted(
            self.session.users.only('session_points', 'username').values(
                'session_points', 'username'
            ),
            key=lambda user: -user['session_points'],
        )

    @database_sync_to_async
    def disconnect_user(self):
        self.session.users.remove(self.scope['user'])
        self.session.save()
