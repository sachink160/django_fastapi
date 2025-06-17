from django.contrib import admin
from .models import Domain, Internship

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mobile', 'domain', 'user', 'start_date', 'end_date', 'is_pay', 'is_complete')
    list_filter = ('domain', 'is_pay', 'is_complete', 'start_date', 'end_date')
    search_fields = ('name', 'mobile', 'domain__name', 'user__username')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    list_editable = ('is_pay', 'is_complete')
    fieldsets = (
        (None, {
            'fields': ('name', 'mobile', 'domain', 'user', 'description')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Status', {
            'fields': ('is_pay', 'is_complete')
        }),
    )
