import whn.settings


def answer_time(request):
    return {'ANSWER_BUFFER_SECONDS': whn.settings.ANSWER_BUFFER_SECONDS}
