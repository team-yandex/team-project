from asyncio import sleep
import json

from asgiref.sync import sync_to_async
from channels.consumer import database_sync_to_async
import channels.generic.websocket
from django.utils import timezone
from session.models import Session
from whn.settings import ANSWER_BUFFER_SECONDS

from game.models import Choice, Question
from users.models import User


class LobbyConsumer(channels.generic.websocket.AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']

        self.session = await self.get_session(self.session_id)
        if await self.is_avalaible():
            await self.channel_layer.group_add(
                self.session_id, self.channel_name
            )
            await self.add_user(self.scope['user'])
            message = {'type': 'connection'}
            await self.accept()
            await self.channel_layer.group_send(self.session_id, message)
        else:
            await self.close()

    async def connection(self, event):
        users = await self.get_all_users()
        await self.send(text_data=json.dumps({'users': users}))

    async def receive(self, text_data=None, bytes_data=None):
        # ээх, щас бы python 3.10 и pattern matching...
        data = json.loads(str(text_data))
        if data.get('event') == 'start':
            self.counter = 0
            await self.activate()
            await self.choose_questions(self.session.max_questions)
            message = {
                'type': 'get_question',
                'number': self.questions[self.counter],
            }
            await self.channel_layer.group_send(self.session_id, message)
        elif data.get('event') == 'answer':
            if (
                await self.is_correct(data['answer']) is True
                and not self.answered
            ):
                self.answered = True
                await self.send(json.dumps({'truth': 'Вы были правы'}))
                await self.update_score(self.scope['user'].pk)
            elif (
                await self.is_correct(data['answer']) is False
                and not self.answered
            ):
                self.answered = True
                await self.send(
                    text_data=json.dumps({'truth': 'Вы были неправы!'})
                )
            elif (
                await self.is_correct(data['answer']) is None
                and not self.answered
            ):
                self.answered = True
                await self.send(
                    text_data=json.dumps({'truth': 'Вы не успели!'})
                )

        elif data.get('event') == 'next':
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

        return await super().receive(text_data, bytes_data)

    async def get_question(self, event):
        self.answered = False
        await sync_to_async(self.scope['session'].__setitem__)(
            'start_datetime', str(timezone.now())
        )
        await sync_to_async(self.scope['session'].save)()
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
        await sleep(instance.climax_second + ANSWER_BUFFER_SECONDS)
        await self.send(text_data=json.dumps({'end': instance.video.url}))

    async def finish(self, event):
        await self.send(
            text_data=json.dumps({'finish': await self.final_leaderbord()})
        )

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
        return tuple([user.username for user in self.session.users.all()])

    @database_sync_to_async
    def activate(self):
        self.session.status = Session.Status.ACTIVE

    @database_sync_to_async
    def choose_questions(self, amount):
        queryset = Question.objects.published().order_by('?')
        self.questions = tuple(queryset.values_list('id', flat=True)[:amount])

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
        if type(id) == str:
            return None
        choice = Choice.objects.get(pk=id)
        if choice.is_correct is True:
            return True
        return False

    @database_sync_to_async
    def update_score(self, id):
        winner = User.objects.get(pk=id)
        winner.session_points += 1
        winner.save()

    @database_sync_to_async
    def final_leaderbord(self):
        self.session.status = Session.Status.ENDED
        return [
            [user.username, user.session_points]
            for user in self.session.users.all()
        ]
