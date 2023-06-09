from uuid import UUID

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic.base import ContextMixin

from game.forms import QuestionForm
from game.models import Question
from session.forms import ConnectSessionForm
from session.models import Session


class CreateSessionView(LoginRequiredMixin, CreateView):
    model = Session
    fields = ['max_users', 'complexity', 'max_questions']
    template_name = 'session/create.html'

    def get_success_url(self):
        self.object.owner = self.request.user
        self.object.save()
        self.object.users.add(self.request.user)
        self.request.session['session_token'] = str(self.object.code)
        self.request.session['owner'] = self.request.user.username
        return reverse('session:lobby')


class ConnectSessionView(LoginRequiredMixin, FormView):
    form_class = ConnectSessionForm
    template_name = 'session/connect.html'
    success_url = reverse_lazy('session:lobby')

    def form_valid(self, form):
        # testing validity of uuid
        try:
            code = UUID(form.cleaned_data['code'], version=4)
        except ValueError:
            return redirect('session:connect')
        session = Session.objects.filter(code=code).first()
        if session:
            self.request.session['session_token'] = str(
                form.cleaned_data['code']
            )
            self.request.session['owner'] = session.owner.username
            return super().form_valid(form)
        return redirect('session:connect')


class LobbyView(LoginRequiredMixin, TemplateView, ContextMixin):
    template_name = 'session/lobby.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['session_id'] = self.request.session['session_token']
        return context


class QuestionView(UpdateView):
    template_name = 'session/question.html'
    form_class = QuestionForm
    queryset = Question.objects.published()
    context_object_name = 'question'
    success_url = reverse_lazy('game:result')
