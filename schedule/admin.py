from django.contrib import admin
from django.forms.widgets import CheckboxChoiceInput
from django.utils.translation import ugettext_lazy as _
from random import choice
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




class ModelInline(admin.StackedInline):#generic.GenericStackedInline):
    model = Rule
    # fields = ('name',)

class EventAdmin(admin.ModelAdmin):
    model = Event
    fields = ('category', 'title', 'description', 'locations', 'media', 'admission_price', 'start', 'end', 'rule', 'end_recurring_period', 'tags', 'sponsors', 'sponsor_text')
    list_filter = (EventsFilter,)


from django import forms

class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule


    CHOISES_WEEKDAYS = ((0, 'Sunday'),
                        (1, 'Monday'),
                        (2, 'Tuesday'),
                        (3, 'Wednesday'),
                        (4, 'Thursday'),
                        (5, 'Friday'),
                        (6, 'Saturday'))


    CHOISES_PATTERN = ((3, 'Daily'), (2, 'Weekly'), (1, 'Monthly'), (0, 'Yearly'))
    CHOISES_RANGE_YEAR = ((i,'%s'%i)for i  in xrange(1,13))
    CHOISES_RANGE_MONTHLY = ([(i,'%s'%i)for i  in xrange(1,13)])
    CHOISES_RANGE_WEEKLY = ((i,'%s'%i)for i  in xrange(1,53))
    # When DAILY range
    # we can repeat via "N" days
    CHOISES_RANGE_DAYS =  ([(i,'%s'%i)for i  in xrange(1,31)])

    CHOICES_MONTH = (('January', 'January',),
                     ('February', 'February',),
                     ('March', 'March',),
                     ('April', 'April',),
                     ('May', 'May',),
                     ('June', 'June',),
                     ('July', 'July',),
                     ('August', 'August',),
                     ('September', 'September',),
                     ('October', 'October',),
                     ('November', 'November',),
                     ('December', 'December',),
                    )
    CHOICES_MONTLY = (('Day','Day "11" of every "1" Month(s)'), ('The','The "Second" "Friday" of every "2" month(s)'))

    CHOICES_YEARLY = ((0, 'On "Month" "Day"'), (1,'On the "First" "Monday" of "September"'))



    CHOICE_EVERY_DAY = (("Every day", "Every day"), ('Every', 'Every'))
    CHOICE_NUMBERAL_DAYS = ((0,'FIRST',),
                            (1,'SECOND',),
                            (2, 'THIRD',),
                            (3, 'FOURTH',))

    pattern = forms.ChoiceField(widget=forms.RadioSelect(),#attrs={'onchange':'onchange_handler()',}),
                                choices=CHOISES_PATTERN,
                                label='Recurrence pattern',
                                )

    WEEKLY_WEEKDAYS = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=CHOISES_WEEKDAYS,
                                         label='Weekdays',
                                         required=False)

    every_weekday = forms.ChoiceField(widget=forms.RadioSelect,
                                    choices=(('Every day', 'Every day'),),
                                             required=False)

    daily_range = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:100%'}),
                                    choices=CHOISES_RANGE_DAYS,
                                    label='Repeat Every day(s)',
                                    required=False)

    yearly_range = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:100%'}),
                                     choices=CHOISES_RANGE_YEAR,
                                     label='Repeat every',
                                     required=False)

    X_range = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:100%'}),
                                choices=CHOICE_NUMBERAL_DAYS,
                                label='On the',
                                required=False)

    monthly_range = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:100%'}),
                                      choices=CHOICES_MONTH,
                                      label='Month',
                                      required=False)

    MONTHLY_select_weekday = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:100%'}),
                                        choices=CHOISES_WEEKDAYS,
                                        label='',
                                        required=False)

    select_weekday_1 = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:100%'}),
                                        choices=CHOISES_WEEKDAYS,
                                        label='',
                                        required=False)

    DAILY_repeat_days = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:50px'}),
                                           choices=CHOISES_RANGE_DAYS,
                                           label='Every',
                                           required=False)

    DAILY_options = forms.ChoiceField(widget=forms.RadioSelect,
                                    choices=CHOICE_EVERY_DAY,
                                    label='Options',
                                    required=False,
                                    )

    WEEKLY_select_range = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:50px'}),
                                           choices=CHOISES_RANGE_WEEKLY,
                                           label='Repeat every weekday',
                                           required=False)

    MONTHLY_radio = forms.ChoiceField(widget=forms.RadioSelect,
                                      choices=CHOICES_MONTLY,
                                      label='Chose type of date',
                                      required=False)

    MONTHLY_select_range_days = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:100%'}),
                                      choices=CHOISES_RANGE_DAYS,
                                      label='Day',
                                      required=False)

    MONTHLY_select_range_month = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:100%'}),
                                      choices=CHOISES_RANGE_MONTHLY,
                                      label='of every',
                                      required=False)

    MONTHLY_select_range_numberals = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:100%'}),
                                      choices=CHOICE_NUMBERAL_DAYS,
                                      label='The',
                                      required=False)
    MONTHLY_select_range_month_1 = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:100%'}),
                                      choices=CHOISES_RANGE_MONTHLY,
                                      label='of every',
                                      required=False)

    RADIO_yearly = forms.ChoiceField(widget=forms.RadioSelect,
                                      choices=CHOICES_YEARLY,
                                      label='Chose type of date',
                                      required=False,
                                     )
    YEARLY_select_range_month = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:100%'}),
                                      choices=CHOICES_MONTH,
                                      label='On',
                                      required=False)

    YEARLY_select_range_monthly = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:100%'}),
                                      choices=CHOISES_RANGE_DAYS,
                                      label='Day',
                                      required=False)

    YEARLY_select_range_numberals = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:100%'}),
                                      choices=CHOICE_NUMBERAL_DAYS,
                                      label='On the',
                                      required=False)

    YEARLY_select_weekday = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:100%'}),
                                        choices=CHOISES_WEEKDAYS,
                                        label='',
                                        required=False)

    YEARLY_select_range_monthly_2 = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:100%'}),
                                      choices=CHOICES_MONTH,
                                      label='of',
                                      required=False)

    def _media(self):
        js = ['/static/scripts/admin/check_forms.js',]
        return forms.Media(js=js)

    media = property(_media)


class RuleAdmin(admin.ModelAdmin):
    form = RuleForm
    fieldsets = (
        (None, {
            'fields': ('name','description',
                       ('pattern',),
                        # DAILY
                       'DAILY_options', 'DAILY_repeat_days',

                        #WEEKLY
                       'WEEKLY_select_range',
                       'WEEKLY_WEEKDAYS',


                        # MONTHLY

                        'MONTHLY_radio',
                        ('MONTHLY_select_range_days',
                         'MONTHLY_select_range_month',),

                        ('MONTHLY_select_range_numberals', 'MONTHLY_select_weekday', 'MONTHLY_select_range_month_1'),

                        #YEARLY

                        'RADIO_yearly',
                        ('YEARLY_select_range_month','YEARLY_select_range_monthly'),
                        ('YEARLY_select_range_numberals', 'YEARLY_select_weekday','YEARLY_select_range_monthly_2',),
            )

        }),
)

# admin.site.register(Calendar, CalendarAdminOptions)
admin.site.register(Rule, RuleAdmin)
admin.site.register(Event, EventAdmin)
#admin.site.register([Rule, Event, CalendarRelation])
admin.site.register(Category)