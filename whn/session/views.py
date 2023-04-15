from cryptography.fernet import Fernet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, TemplateView
from session.models import Session
from whn.settings import SESSION_CRYPTO


class CreateSessionView(LoginRequiredMixin, CreateView):
    model = Session
    fields = ['max_users', 'complexity', 'max_questions']
    template_name = 'session/create.html'

    def get_success_url(self):
        self.object.users.add(self.request.user)
        self.request.session['session_token'] = (
            Fernet(SESSION_CRYPTO.encode())
            .encrypt(str(self.object.id).encode())
            .decode()
        )
        return reverse('session:lobby')


class LobbyView(LoginRequiredMixin, TemplateView):
    template_name = 'session/lobby.html'
