import pathlib
import tempfile
import unittest

import channels.db
import channels.routing
import channels.security.websocket
import channels.sessions
import channels.testing
import django.conf
import django.core.files
import django.test
import django.utils
import moviepy.editor

import game.consumers
import game.forms
import game.models


class QuestionViewTest(django.test.TestCase):
    """test question view"""

    fixtures = ['questions.json']
    QUESTION_ID = 1

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.question = game.models.Question.objects.published().get(
            pk=cls.QUESTION_ID
        )
        cls.form = game.forms.QuestionForm(instance=cls.question)
        cls.question_url = django.urls.reverse('game:question')
        cls.application = (
            channels.security.websocket.AllowedHostsOriginValidator(
                channels.sessions.SessionMiddlewareStack(
                    channels.routing.URLRouter(
                        [
                            django.urls.re_path(
                                r'ws/test/session/(?P<session_id>\w+)/$',
                                game.consumers.QuestionConsumer.as_asgi(),
                            ),
                        ]
                    )
                )
            )
        )

    def test_form_key_in_context(self):
        """test that key form is in context"""
        response = django.test.Client().get(self.question_url)
        self.assertIn('form', response.context)

    def test_form_in_context_is_questionform(self):
        """test that form in context is instance of QuestionForm"""
        response = django.test.Client().get(self.question_url)
        form = response.context['form']
        self.assertIsInstance(form, game.forms.QuestionForm)

    def test_question_key_in_context(self):
        """test that key question is in context"""
        response = django.test.Client().get(self.question_url)
        self.assertIn('question', response.context)

    # TODO: restore removed test with mocking random

    def test_choice_label_correct(self):
        """test choice field label is correct"""
        text_label = self.form.fields['choices'].label
        self.assertEqual(text_label, 'Что будет дальше?')

    @unittest.skip
    async def test_socket_connected(self):
        """test question socket could be connected"""
        communicator = channels.testing.WebsocketCommunicator(
            self.application, f'ws/test/session/{self.QUESTION_ID}/'
        )
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

    @unittest.skip
    async def test_socket_gives_climax_video_url(self):
        """test after getting question id socket responding
        with climax video url"""
        communicator = channels.testing.WebsocketCommunicator(
            self.application, f'ws/test/session/{self.QUESTION_ID}/'
        )
        await communicator.connect()
        await communicator.send_json_to({'questionId': self.QUESTION_ID})
        message = await communicator.receive_json_from()
        self.assertDictEqual(message, {'url': self.question.climax_video.url})
        await communicator.disconnect()

    @unittest.skip
    @django.test.override_settings(ANSWER_BUFFER_SECONDS=float('-inf'))
    async def test_socket_gives_video_url(self):
        """test after timeout socket gives answer video"""
        communicator = channels.testing.WebsocketCommunicator(
            self.application, f'ws/test/session/{self.QUESTION_ID}/'
        )
        await communicator.connect()
        await communicator.send_json_to({'questionId': self.QUESTION_ID})
        await communicator.receive_from()  # do nothin with climax video
        message = await communicator.receive_json_from()
        self.assertDictEqual(
            message, {'end': True, 'url': self.question.video.url}
        )
        await communicator.disconnect()

    def test_moves_to_results(self):
        """test after choosing choice moves to results"""
        # FIXME: question is random so form is invalid
        correct_choice = self.question.choices.filter(is_correct=True).first()
        answer_data = {'choices': correct_choice.id}
        client = django.test.Client()
        session = client.session
        session['start_datetime'] = str(django.utils.timezone.now())
        session.save()
        response = client.post(
            self.question_url,
            data=answer_data,
            follow=True,
        )
        self.assertTemplateUsed(response, 'game/result.html')


class QuestionModelTest(django.test.TestCase):
    fixtures = ['questions.json']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.question = game.models.Question.objects.first()

    @django.test.override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_climax_video_created(self):
        video_path = pathlib.Path('game') / 'fixtures' / 'Да_ты_че.mp4'
        climax_second = 3
        with video_path.open(mode='rb') as f:
            question = game.models.Question(
                video=django.core.files.File(f, video_path.name),
                score=5,
                climax_second=climax_second,
                complexity=game.models.Question.Complexity.easy,
            )
            question.save()
        climax_video = moviepy.editor.VideoFileClip(question.climax_video.path)
        self.assertEqual(climax_video.duration, climax_second)

    def test_question_published_with_only_one_correct_answer(self):
        """test question published with only one correct answer"""
        self.assertTrue(self.question.is_published)
        choice = self.question.choices.filter(is_correct=False).first()
        choice.is_correct = True
        choice.save()
        self.question.save(update_fields=[])
        self.assertFalse(self.question.is_published)

    def test_question_published_with_4_choices(self):
        """test question published with 4 choices"""
        self.assertTrue(self.question.is_published)
        choice = game.models.Choice(label='test', question=self.question)
        choice.save()
        self.question.save(update_fields=[])
        self.assertFalse(self.question.is_published)

    def test_question_published_with_4_normilized_choices(self):
        """test question published with 4 normilized choices"""
        self.assertTrue(self.question.is_published)
        older_choice = self.question.choices.order_by('id').first()
        self.assertEqual(older_choice.label, 'Ничего не случиться')
        choice = self.question.choices.exclude(id=older_choice.id).first()
        for label in (
            'Ничего   не\tслучиться\n',
            'Ничего, не, случиться?',
            'НичегО Не СЛУЧИТЬСЯ',
            'Ни чего не слу читься',
        ):
            with self.subTest(label=label):
                choice.label = label
                choice.save()
                self.question.save(update_fields=[])
                self.assertFalse(self.question.is_published)
