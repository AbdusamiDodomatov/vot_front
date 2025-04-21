from django.contrib import admin
from .models import Election, Choice

class ElectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'total_votes')  # Показываем название и общее количество голосов

    @admin.display(description='Jami ovozlar')
    def total_votes(self, obj):
        return sum(choice.votes for choice in obj.choices.all())

admin.site.register(Election, ElectionAdmin)
admin.site.register(Choice)
