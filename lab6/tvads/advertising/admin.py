from django.contrib import admin

from .models import Advertisement, Agent, Customer, Program


class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'price_per_minute')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'inn', 'bank_name')


class AgentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'phone', 'percent', 'get_total_cost', 'get_salary')


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'program', 'air_date', 'duration',
                    'get_cost', 'agent', 'is_aired', 'get_excerpt')


admin.site.register(Program, ProgramAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)
