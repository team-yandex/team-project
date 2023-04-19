from django.forms import CharField
from django.forms import Form


class ConnectSessionForm(Form):
    code = CharField()
