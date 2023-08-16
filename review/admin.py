from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'doctor', 'rating', 'created_at', 'is_show')
    list_filter = ('doctor', 'is_show', 'created_at')
    search_fields = ('user__username', 'doctor__doctor_name', 'content')
    list_per_page = 10

    fieldsets = (
        ('Review Information', {
            'fields': ('user', 'doctor', 'rating', 'content', 'is_show', 'created_at'),
        }),
    )

    readonly_fields = ('created_at',)
