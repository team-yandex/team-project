import datetime

import django.conf
import django.shortcuts
import django.urls
import django.utils
import django.views.generic

import game.forms
import game.models


class QuestionView(django.views.generic.UpdateView):
    template_name = 'game/question.html'
    form_class = game.forms.QuestionForm
    queryset = game.models.Question.objects.published()
    context_object_name = 'question'
    success_url = django.urls.reverse_lazy('game:result')

    def form_valid(self, form):
        start_datetime = datetime.datetime.fromisoformat(
            self.request.session['start_datetime']
        )
        end_datetime = start_datetime + datetime.timedelta(
            seconds=self.object.climax_second
            + django.conf.settings.ANSWER_BUFFER_SECONDS
        )
        if (
            form.cleaned_data['choices'].is_correct
            and django.utils.timezone.now() < end_datetime
        ):
            return django.shortcuts.render(
                self.request, 'game/result.html', context={'result': 'ok'}
            )
        return django.shortcuts.render(
            self.request, 'game/result.html', context={'result': 'not ok'}
        )


class ResultView(django.views.generic.TemplateView):
    template_name = 'game/result.html'


class SingleView(django.views.generic.TemplateView):
    template_name = 'game/single.html'

    def post(self, request, *args, **kwargs):
        question_id = game.models.Question.objects.random().id
        return django.shortcuts.redirect(
            django.urls.reverse('game:question', kwargs=dict(pk=question_id))
        )
