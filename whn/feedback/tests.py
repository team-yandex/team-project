import tempfile

import django.test
import django.urls

import feedback.forms
import feedback.models


class FeedbackAutherTest(django.test.TestCase):
    """test feedback auther"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.form = feedback.forms.FeedbackAutherForm()

    def test_feedback_auther_key_in_context(self):
        """test that key feedback_auther is in context"""
        response = django.test.Client().get(
            django.urls.reverse('feedback:feedback')
        )
        self.assertIn('feedback_auther', response.context)

    def test_form_in_context_is_feedbackform(self):
        """test that form in context is instance of FeedbackAutherForm"""
        response = django.test.Client().get(
            django.urls.reverse('feedback:feedback')
        )
        form = response.context['feedback_auther']
        self.assertIsInstance(form, feedback.forms.FeedbackAutherForm)

    def test_name_label_correct(self):
        """test name field label is correct"""
        name_label = self.form.fields['name'].label
        self.assertEqual(name_label, 'Имя')

    def test_name_help_text(self):
        """test name field help text is correct"""
        name_help_text = self.form.fields['name'].help_text
        self.assertEqual(name_help_text, 'Максимальная длина 64 символа')

    def test_mail_label_correct(self):
        """test mail field label is correct"""
        mail_label = self.form.fields['email'].label
        self.assertEqual(mail_label, 'Контактная электронная почта')

    def test_mail_help_text(self):
        """test mail field help text is correct"""
        mail_help_text = self.form.fields['email'].help_text
        self.assertEqual(mail_help_text, 'На этот адрес будет отправлен ответ')

    def test_shows_email_placeholder(self):
        """test form shows email palceholder"""
        self.assertIn('placeholder="default@example.com"', self.form.as_p())


class FeedbackFileTest(django.test.TestCase):
    """test feedback file"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.form = feedback.forms.FeedbackFileForm()

    def test_feedback_form_key_in_context(self):
        """test that key feedback_form is in context"""
        response = django.test.Client().get(
            django.urls.reverse('feedback:feedback')
        )
        self.assertIn('files_form', response.context)

    def test_form_in_context_is_feedbackform(self):
        """test that form in context is instance of FeedbackFileForm"""
        response = django.test.Client().get(
            django.urls.reverse('feedback:feedback')
        )
        form = response.context['files_form']
        self.assertIsInstance(form, feedback.forms.FeedbackFileForm)

    def test_file_label_correct(self):
        """test file field label is correct"""
        file_label = self.form.fields['file'].label
        self.assertEqual(file_label, 'Файл')

    def test_file_help_text(self):
        """test file field help text is correct"""
        file_help_text = self.form.fields['file'].help_text
        self.assertEqual(file_help_text, 'При необходимости прикрепите файлы')


class FeedbackTest(django.test.TestCase):
    """test feedback"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.form = feedback.forms.FeedbackForm()

    def test_feedback_form_key_in_context(self):
        """test that key feedback_form is in context"""
        response = django.test.Client().get(
            django.urls.reverse('feedback:feedback')
        )
        self.assertIn('feedback_form', response.context)

    def test_form_in_context_is_feedbackform(self):
        """test that form in context is instance of FeedbackForm"""
        response = django.test.Client().get(
            django.urls.reverse('feedback:feedback')
        )
        form = response.context['feedback_form']
        self.assertIsInstance(form, feedback.forms.FeedbackForm)

    def test_text_label_correct(self):
        """test text field label is correct"""
        text_label = self.form.fields['text'].label
        self.assertEqual(text_label, 'Текст сообщения')

    def test_text_help_text(self):
        """test text field help text is correct"""
        text_help_text = self.form.fields['text'].help_text
        self.assertEqual(text_help_text, 'Максимальная длина 200 символов')


class FeedbackViewTest(django.test.TestCase):
    """test feedback view"""

    @classmethod
    def setUpClass(cls):
        cls.form_data = {
            'text': 'Test text',
            'email': 'test@test.ru',
            'name': 'test',
        }
        return super().setUpClass()

    def test_redirect(self):
        """test after form input redirects back"""
        response = django.test.Client().post(
            django.urls.reverse('feedback:feedback'),
            data=self.form_data,
            follow=True,
        )
        self.assertRedirects(
            response, django.urls.reverse('feedback:feedback')
        )

    def test_feedback_record_saved(self):
        """test after form input new feedback record saved"""
        text = self.form_data['text']
        email = self.form_data['email']
        name = self.form_data['name']
        django.test.Client().post(
            django.urls.reverse('feedback:feedback'), data=self.form_data
        )
        fb = feedback.models.Feedback.objects.first()
        self.assertEqual(fb.auther.email, email)
        self.assertEqual(fb.auther.name, name)
        self.assertEqual(fb.text, text)

    @django.test.override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_feedback_attachments_saved(self):
        """test after form input with attachments new attachments
        records saved"""
        attachments_count = feedback.models.FeedbackFile.objects.count()
        with open('feedback/fixtures/file.jpg', 'rb') as f1, open(
            'feedback/fixtures/file.txt', 'r'
        ) as f2:
            data = {'file': [f1, f2], **self.form_data}
            django.test.Client().post(
                django.urls.reverse('feedback:feedback'), data=data
            )

        self.assertEqual(
            attachments_count + 2,  # two files sent
            feedback.models.FeedbackFile.objects.count(),
        )
