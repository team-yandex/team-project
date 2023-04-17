import datetime

import django.conf
import django.http
import django.shortcuts
import django.urls
import django.utils
import django.views.generic


import game.forms
import game.models


class QuestionView(django.views.generic.UpdateView):
    template_name = 'game/question.html'
    form_class = game.forms.QuestionForm
    context_object_name = 'question'

    def get_object(self, queryset=None):
        question_id = self.request.session.get('question_id')
        if question_id is None:
            exclude = None
            if self.request.user.is_anonymous:
                exclude = self.request.session.get('seen_questions')
            question = game.models.Question.objects.random(exclude=exclude)
            if question is None:
                raise django.http.Http404('Вопросы закончились')
            self.request.session['question_id'] = question.id
            if self.request.user.is_anonymous:
                if exclude is None:
                    self.request.session['seen_questions'] = [question.id]
                else:
                    self.request.session['seen_questions'].append(question.id)
            return question
        return game.models.Question.objects.get(pk=question_id)

    def form_valid(self, form):
        if 'question_id' in self.request.session:
            self.request.session.pop('question_id')
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
            if self.request.user.is_anonymous:
                if self.request.session.get('score') is not None:
                    self.request.session['score'] += self.object.score
                else:
                    self.request.session['score'] = self.object.score
            return django.shortcuts.render(
                self.request, 'game/result.html', context={'success': True}
            )
        return django.shortcuts.render(
            self.request, 'game/result.html', context={'success': False}
        )

    def form_invalid(self, form):
        return django.shortcuts.render(
            self.request, 'game/result.html', context={'success': False}
        )


class ResultView(django.views.generic.TemplateView):
    template_name = 'game/result.html'


class SingleView(django.views.generic.TemplateView):
    template_name = 'game/single.html'
