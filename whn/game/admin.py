import django.contrib.admin

import game.models


django.contrib.admin.site.register(game.models.Choice)


class InlineChoice(django.contrib.admin.StackedInline):
    model = game.models.Choice


@django.contrib.admin.register(game.models.Question)
class QuestionAdmin(django.contrib.admin.ModelAdmin):
    inlines = [InlineChoice]
