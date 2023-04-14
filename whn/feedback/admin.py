from django.contrib import admin

from .models import Feedback, FeedbackAuther, FeedbackFile


class FeedbackAutherInline(admin.TabularInline):
    model = FeedbackAuther
    fields = ('name', 'email')


class FeedbackFileInline(admin.TabularInline):
    model = FeedbackFile
    fields = ('file',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    fields = ('text', 'status')
    list_display = ('text', 'status', 'created_on')
    inlines = (FeedbackAutherInline, FeedbackFileInline)
