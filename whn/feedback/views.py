from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from feedback.forms import FeedbackAutherForm
from feedback.forms import FeedbackFileForm
from feedback.forms import FeedbackForm
from feedback.models import Feedback
from feedback.models import FeedbackAuther
from feedback.models import FeedbackFile


class FeedbackView(TemplateView):
    template_name = 'feedback/feedback.html'

    def get(self, request, *args, **kwargs):
        feedback_auther = FeedbackAutherForm(request.POST or None)
        feedback_form = FeedbackForm(request.POST or None)
        files_form = FeedbackFileForm(
            request.POST or None,
            files=request.FILES or None,
        )

        context = {
            'feedback_auther': feedback_auther,
            'feedback_form': feedback_form,
            'files_form': files_form,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        feedback_auther = FeedbackAutherForm(request.POST or None)
        feedback_form = FeedbackForm(request.POST or None)
        files_form = FeedbackFileForm(
            request.POST or None,
            files=request.FILES or None,
        )

        forms = (feedback_auther, feedback_form, files_form)

        if all(form.is_valid() for form in forms):
            text = feedback_form.cleaned_data[Feedback.text.field.name]
            email = feedback_auther.cleaned_data[
                FeedbackAuther.email.field.name
            ]

            subject_template_name = 'feedback/email_texts/feedback.html'
            context = {'text': text}
            mail_text = render_to_string(subject_template_name, context)
            send_mail(
                'Whn',
                mail_text,
                settings.ADMIN_EMAIL,
                [email],
                fail_silently=False,
            )

            feedback_item = Feedback.objects.create(
                **feedback_form.cleaned_data
            )
            FeedbackAuther.objects.create(
                feedback=feedback_item,
                **feedback_auther.cleaned_data,
            )
            for file in request.FILES.getlist(FeedbackFile.file.field.name):
                FeedbackFile.objects.create(
                    file=file,
                    feedback=feedback_item,
                )

            messages.success(request, 'Отзыв отправлен. Спасибо!')

            return redirect('feedback:feedback')

        context = {
            'feedback_auther': feedback_auther,
            'feedback_form': feedback_form,
            'files_form': files_form,
        }
        return render(request, self.template_name, context)
