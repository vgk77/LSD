from django.contrib import admin

from .models import Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    fields = ('id', 'name', 'text')
    readonly_fields = ('id', )
    search_fields = ('name', )
