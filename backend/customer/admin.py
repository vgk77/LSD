from django.contrib import admin

from .models import Customer, Ticket


class TicketsInline(admin.TabularInline):
    fields = ['message', 'status']
    model = Ticket
    extra = 0
    readonly_fields = ['message']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram_id', 'id')
    fields = ('id', 'telegram_id', 'name')
    readonly_fields = ('id', )
    inlines = [TicketsInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('topic', 'status', 'number', 'created_at', 'updated_at', )
    readonly_fields = ('number', )
