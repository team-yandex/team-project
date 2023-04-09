import django.test
import django.urls

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

    def test_form_key_in_context(self):
        """test that key form is in context"""
        response = django.test.Client().get(
            django.urls.reverse('game:question', args=[self.QUESTION_ID])
        )
        self.assertIn('form', response.context)

    def test_form_in_context_is_questionform(self):
        """test that form in context is instance of QuestionForm"""
        response = django.test.Client().get(
            django.urls.reverse('game:question', args=[self.QUESTION_ID])
        )
        form = response.context['form']
        self.assertIsInstance(form, game.forms.QuestionForm)

    def test_question_key_in_context(self):
        """test that key question is in context"""
        response = django.test.Client().get(
            django.urls.reverse('game:question', args=[self.QUESTION_ID])
        )
        self.assertIn('question', response.context)

    def test_correct_question_in_context(self):
        """test that correct question is in context"""
        response = django.test.Client().get(
            django.urls.reverse('game:question', args=[self.QUESTION_ID])
        )
        self.assertEqual(response.context['question'].id, self.question.id)

    def test_correct_choices_showed(self):
        """test that correct choices showed"""
        response = django.test.Client().get(
            django.urls.reverse('game:question', args=[self.QUESTION_ID])
        )
        for choice in self.question.choices.all():
            self.assertContains(response, choice.label)

    def test_choice_label_correct(self):
        """test choice field label is correct"""
        text_label = self.form.fields['choices'].label
        self.assertEqual(text_label, 'Что будет дальше?')

    def test_redirects_to_results(self):
        """test after choosing choice redirects to results"""
        correct_choice = self.question.choices.filter(is_correct=True).first()
        answer_data = {'choices': correct_choice.id}
        response = django.test.Client().post(
            django.urls.reverse('game:question', args=[self.QUESTION_ID]),
            data=answer_data,
            follow=True,
        )
        self.assertRedirects(response, django.urls.reverse('game:result'))
