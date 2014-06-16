from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from schedule.models import Event, Rule, Category
from datetime import datetime


# class CalendarAdminOptions(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("name",)}
#     search_fields = ['name']

class EventsFilter(admin.SimpleListFilter):
    title = 'Filter'
    parameter_name = 'end'

    def lookups(self, request, model_admin):
        return (
            ('gte', _('by datetime of next occurance'))
            ,)

    def queryset(self, request, queryset):
        if self.value() == 'gte':
            return queryset.filter(end__gte=datetime.now())


class EventAdmin(admin.ModelAdmin):
    model = Event
    fields = ('category', 'title', 'description', 'locations', 'admission_price', 'start', 'end', 'rule', 'end_recurring_period', 'sponsor_text')
    list_filter = (EventsFilter,)

#admin.site.register(Calendar, CalendarAdminOptions)
admin.site.register(Rule)
admin.site.register(Event, EventAdmin)
#admin.site.register([Rule, Event, CalendarRelation])
admin.site.register(Category)