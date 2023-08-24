from django.contrib import admin
from .models import UserToDoctorMessage, DoctorToUserMessage

@admin.register(UserToDoctorMessage)
class UserToDoctorMessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'receiver', 'timestamp')
    list_filter = ('sender', 'receiver', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'message_content')
    readonly_fields = ('message_id', 'timestamp')

@admin.register(DoctorToUserMessage)
class DoctorToUserMessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'receiver', 'timestamp')
    list_filter = ('sender', 'receiver', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'message_content')
    readonly_fields = ('message_id', 'timestamp')
