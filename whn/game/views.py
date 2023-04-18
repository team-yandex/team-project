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
            if self.request.user.is_authenticated:
                exclude = self.request.user.seen_questions.values_list(
                    'id', flat=True
                )
            else:
                exclude = self.request.session.get('seen_questions')
            question = game.models.Question.objects.random(exclude=exclude)
            return question
        return game.models.Question.objects.get(pk=question_id)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, *kwargs)
        if self.object is None:
            return django.shortcuts.render(self.request, 'game/completed.html')
        self.request.session['question_id'] = self.object.id
        if self.request.user.is_authenticated:
            question = self.request.user.seen_questions.filter(
                pk=self.object.id
            ).first()
            self.request.user.seen_questions.add(self.object)
        else:
            if 'seen_questions' in self.request.session:
                self.request.session['seen_questions'].append(question.id)
            else:
                self.request.session['seen_questions'] = [question.id]
        return response

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
        video = self.object.video
        if (
            form.cleaned_data['choices'].is_correct
            and django.utils.timezone.now() < end_datetime
        ):
            if self.request.user.is_authenticated:
                self.request.user.score += self.object.score
                self.request.user.save()
            else:
                if self.request.session.get('score') is not None:
                    self.request.session['score'] += self.object.score
                else:
                    self.request.session['score'] = self.object.score
            return django.shortcuts.render(
                self.request,
                'game/result.html',
                context={
                    'success': True,
                    'video': video,
                    'earned': self.object.score,
                },
            )
        return django.shortcuts.render(
            self.request,
            'game/result.html',
            context={'success': False, 'video': video, 'earned': -1},
        )


class ResultView(django.views.generic.TemplateView):
    template_name = 'game/result.html'


class SingleView(django.views.generic.TemplateView):
    template_name = 'game/single.html'
