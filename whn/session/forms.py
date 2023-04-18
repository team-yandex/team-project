from django.forms import CharField, Form


class ConnectSessionForm(Form):
    code = CharField()
