from django.forms import CharField, Form


class ConnectSessionForm(Form):
    token = CharField(max_length=200)
