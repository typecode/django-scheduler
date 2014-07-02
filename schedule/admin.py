from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from schedule.models import Event, Rule, Category
from datetime import datetime
from django import forms
from schedule.forms import EventForm, SpanForm

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


class ModelInline(admin.StackedInline):
    model = Rule
    # fields = ('name',)

class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('creator', 'created_on', 'calendar')
    class Media:
        js = (
            '/static/scripts/admin/schedule_event.js',
        )


class EventAdmin(admin.ModelAdmin):
    model = Event
    form = EventAdminForm

    fields = ('category', 'title', 'description', 'locations', 'image', 'admission_price', 'start', 'end', 'rule', 'end_recurring_period', 'tags', 'sponsors', 'sponsor_text')
    list_filter = (EventsFilter,)


class RuleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RuleForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            ins = kwargs.get('instance')
            pattern = ins.frequency
            if ins.params:
                params = ins.params.split(';')
            else:
                params = ''
            param_dict = self.get_param(params)

            if pattern == 'DAILY':

                self.initial['pattern'] = pattern
                if param_dict['interval'] == 1:
                    self.initial['DAILY_options'] = 'Every day'
                else:
                    self.initial['DAILY_options'] = 'Every'
                    self.initial['DAILY_repeat_days'] = param_dict.get('interval')

            elif pattern == 'WEEKLY':

                self.initial['pattern'] = pattern
                self.initial['WEEKLY_select_range'] = param_dict.get('interval')
                self.initial['WEEKLY_WEEKDAYS'] = param_dict.get('byweekday')

            elif pattern == 'MONTHLY':

                self.initial['pattern'] = pattern
                self.initial['MONTHLY_radio'] = '0'
                self.initial['MONTHLY_select_range_days'] = param_dict.get('bymonthday')
                self.initial['MONTHLY_select_range_month'] = param_dict.get('interval')

            elif pattern == 'YEARLY':

                self.initial['pattern'] = pattern
                self.initial['RADIO_yearly'] = '0'
                self.initial['YEARLY_select_range_month'] = param_dict.get('bymonth')
                self.initial['YEARLY_select_range_monthly'] = param_dict.get('bymonthday')

    @staticmethod
    def get_param(params):
        param_dict = []
        if params is None:
            return {}

        for param in params:
            param = param.split(':')
            if len(param) == 2:
                param = (str(param[0]), [int(p) for p in param[1].split(',')])
                if len(param[1]) == 1:
                    param = (param[0], param[1][0])
                param_dict.append(param)
        return dict(param_dict)

    class Meta:
        model = Rule

    CHOISES_WEEKDAYS = ((1, 'Monday'),
                        (2, 'Tuesday'),
                        (3, 'Wednesday'),
                        (4, 'Thursday'),
                        (5, 'Friday'),
                        (6, 'Saturday'),
                        (0, 'Sunday'),
    )

    CHOISES_PATTERN = (('DAILY', 'Daily'),
                       ('WEEKLY', 'Weekly'),
                       ('MONTHLY', 'Monthly'),
                       ('YEARLY', 'Yearly'))
    CHOISES_RANGE_YEAR = ((i, '%s' % i) for i in xrange(1, 13))
    CHOISES_RANGE_MONTHLY = ([(i, '%s' % i) for i in xrange(1, 13)])
    CHOISES_RANGE_WEEKLY = ((i, '%s' % i) for i in xrange(1, 53))
    # When DAILY range
    # we can repeat via "N" days
    CHOISES_RANGE_DAYS = ([(i, '%s' % i) for i in xrange(1, 31)])

    CHOICES_MONTH = ((1, 'January',),
                     (2, 'February',),
                     (3, 'March',),
                     (4, 'April',),
                     (5, 'May',),
                     (6, 'June',),
                     (7, 'July',),
                     (8, 'August',),
                     (9, 'September',),
                     (10, 'October',),
                     (11, 'November',),
                     (12, 'December',),
    )
    CHOICES_MONTLY = ((0, 'Day "11" of every "1" Month(s)'), (1, 'The "Second" "Friday" of every "2" month(s)'))

    CHOICES_YEARLY = ((0, 'On "Month" "Day"'), (1, 'On the "First" "Monday" of "September"'))

    CHOICE_EVERY_DAY = (("Every day", "Every day"), ('Every', 'Every'))
    CHOICE_NUMBERAL_DAYS = ((1, 'First',),
                            (2, 'Second',),
                            (3, 'Third',),
                            (4, 'Fourth',),
                            (5, 'Fifth',))

    pattern = forms.ChoiceField(widget=forms.RadioSelect(),
                                choices=CHOISES_PATTERN,
                                label='Recurrence pattern', )

    WEEKLY_WEEKDAYS = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                choices=CHOISES_WEEKDAYS,
                                                label='Weekdays',
                                                required=False)

    every_weekday = forms.ChoiceField(widget=forms.RadioSelect,
                                      choices=(('Every day', 'Every day'),),
                                      required=False)

    daily_range = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width:100%'}),
                                    choices=CHOISES_RANGE_DAYS,
                                    label='Repeat Every day(s)',
                                    required=False)

    yearly_range = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width:100%'}),
                                     choices=CHOISES_RANGE_YEAR,
                                     label='Repeat every',
                                     required=False)

    X_range = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width:100%'}),
                                choices=CHOICE_NUMBERAL_DAYS,
                                label='On the',
                                required=False)

    monthly_range = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width:100%'}),
                                      choices=CHOICES_MONTH,
                                      label='Month',
                                      required=False)

    MONTHLY_select_weekday = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width:100%'}),
                                               choices=CHOISES_WEEKDAYS,
                                               label='',
                                               required=False)

    select_weekday_1 = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width:100%'}),
                                         choices=CHOISES_WEEKDAYS,
                                         label='',
                                         required=False)

    DAILY_repeat_days = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width:50px'}),
                                          choices=CHOISES_RANGE_DAYS,
                                          label='Every',
                                          required=False)

    DAILY_options = forms.ChoiceField(widget=forms.RadioSelect,
                                      choices=CHOICE_EVERY_DAY,
                                      label='Options',
                                      required=False,
    )

    WEEKLY_select_range = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width:50px'}),
                                            choices=CHOISES_RANGE_WEEKLY,
                                            label='Repeat every weekday',
                                            required=False)

    MONTHLY_radio = forms.ChoiceField(widget=forms.RadioSelect,
                                      choices=CHOICES_MONTLY,
                                      label='Chose type of date',
                                      required=False)

    MONTHLY_select_range_days = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'style': 'width:100%'}),
                                                  choices=CHOISES_RANGE_DAYS,
                                                  label='Day',
                                                  required=False)

    MONTHLY_select_range_month = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width:100%'}),
                                                   choices=CHOISES_RANGE_MONTHLY,
                                                   label='of every',
                                                   required=False)

    MONTHLY_select_range_numberals = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width:100%'}),
                                                       choices=CHOICE_NUMBERAL_DAYS,
                                                       label='The',
                                                       required=False)
    MONTHLY_select_range_month_1 = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width:100%'}),
                                                     choices=CHOISES_RANGE_MONTHLY,
                                                     label='of every',
                                                     required=False)

    RADIO_yearly = forms.ChoiceField(widget=forms.RadioSelect,
                                     choices=CHOICES_YEARLY,
                                     label='Chose type of date',
                                     required=False,
    )
    YEARLY_select_range_month = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width:100%'}),
                                                  choices=CHOICES_MONTH,
                                                  label='On',
                                                  required=False)

    YEARLY_select_range_monthly = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'style': 'width:100%'}),
                                                    choices=CHOISES_RANGE_DAYS,
                                                    label='Day',
                                                    required=False)

    YEARLY_select_range_numberals = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width:100%'}),
                                                      choices=CHOICE_NUMBERAL_DAYS,
                                                      label='On the',
                                                      required=False)

    YEARLY_select_weekday = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width:100%'}),
                                              choices=CHOISES_WEEKDAYS,
                                              label='',
                                              required=False)

    YEARLY_select_range_monthly_2 = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width:100%'}),
                                                      choices=CHOICES_MONTH,
                                                      label='of',
                                                      required=False)

    def _media(self):
        js = ['/static/scripts/admin/check_forms.js', ]
        return forms.Media(js=js)

    media = property(_media)


class RuleAdmin(admin.ModelAdmin):
    form = RuleForm
    fieldsets = (
        (None, {
            'fields': ('name', 'description',
                       ('pattern',),
                       # DAILY [u'Every day']
                       'DAILY_options', 'DAILY_repeat_days',

                       #WEEKLY
                       'WEEKLY_select_range',
                       'WEEKLY_WEEKDAYS',


                       # MONTHLY

                       'MONTHLY_radio',
                       ('MONTHLY_select_range_days',
                       'MONTHLY_select_range_month',),

                       ('MONTHLY_select_range_numberals', 'MONTHLY_select_weekday', 'MONTHLY_select_range_month_1'),

                       # #YEARLY

                       'RADIO_yearly',
                       ('YEARLY_select_range_month', 'YEARLY_select_range_monthly'),
                       ('YEARLY_select_range_numberals', 'YEARLY_select_weekday', 'YEARLY_select_range_monthly_2',),

            # 'params',
            # 'frequency',
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        # {'count': 1, 'byminute': [1, 2, 4, 5], 'bysecond': 1}
        # pattern (0: yearly, 1: monthly, 2:weekly, 3:daily)
        # 'DAILY_options': [u'Every day' or 'Every'] if 'Every" : DAILY_repeat_days': [u'14']
        #

        new_data = form.cleaned_data
        # DAILY
        if new_data.get('pattern') == 'DAILY':
            obj.frequency = new_data.get('pattern')
            # >>> list(rrule(DAILY, dtstart=datetime(2007,1,2), count=3))
            # >>> [datetime.datetime(2007, 1, 2, 0, 0),
            #      datetime.datetime(2007, 1, 3, 0, 0),
            #      datetime.datetime(2007, 1, 4, 0, 0)]

            if new_data.get('DAILY_repeat_days'):
                # >>> list(rrule(DAILY, dtstart=datetime(2007,1,2), count=3, interval=3))
                # >>> [datetime.datetime(2007, 1, 2, 0, 0),
                #      datetime.datetime(2007, 1, 5, 0, 0),
                #      datetime.datetime(2007, 1, 8, 0, 0)]

                obj.params = 'interval:' + new_data.get('DAILY_repeat_days')
                print obj.params

            obj.save()

        # WEEKLY
        if new_data.get('pattern') == 'WEEKLY':

            # 'WEEKLY_WEEKDAYS': [u'SU', u'TU'],
            #  u'WEEKLY_select_range': [u'2']
            # >>> list(rrule(WEEKLY, dtstart=datetime(2014,6,23),count=4, byweekday=(MO,TU)))
            #     [datetime.datetime(2014, 6, 23, 0, 0),
            #      datetime.datetime(2014, 6, 24, 0, 0),
            #      datetime.datetime(2014, 6, 30, 0, 0),
            #      datetime.datetime(2014, 7, 1, 0, 0)]

            obj.frequency = new_data.get('pattern')
            interval = new_data.get('WEEKLY_select_range')
            if new_data.get('WEEKLY_WEEKDAYS'):
                byweekday = ''
                for day in new_data.get('WEEKLY_WEEKDAYS'):
                        byweekday += day + ','
                else:
                    byweekday = byweekday[:-1] + ';'

                obj.params = 'interval:{0};byweekday:{1}'.format(interval, byweekday,)
            else:
                obj.params = 'interval:{0}'.format(interval,)

            obj.save()

        # MONTHLY
        if new_data.get('pattern') == 'MONTHLY':

            # 'MONTHLY_select_range_month': [u'12']
            # 'MONTHLY_select_range_days': [u'30']
            # >>> list(rrule(MONTHLY, dtstart=datetime(2014,6,23),count=4))
            # [datetime.datetime(2014, 6, 23, 0, 0),
            #  datetime.datetime(2014, 7, 23, 0, 0),
            #  datetime.datetime(2014, 8, 23, 0, 0),
            #  datetime.datetime(2014, 9, 23, 0, 0)]

            obj.frequency = new_data.get('pattern')
            if new_data['MONTHLY_radio'] == '0':
                bymonthday = ','.join(map(str, new_data.get('MONTHLY_select_range_days')))

                interval = new_data['MONTHLY_select_range_month']
                obj.params = 'bymonthday:{0};interval:{1};'.format(bymonthday, interval,)

            print request.POST
            # TODO NOT WORKING byweekday:1(2);
            if new_data['MONTHLY_radio'] == '1':

                # MONTHLY_select_weekday': [u'4']
                # MONTHLY_select_range_month_1': [u'6']
                # MONTHLY_select_range_numberals : [u'2'] # Second

                interval = new_data.get('MONTHLY_select_range_month_1')
                day = new_data.get('MONTHLY_select_weekday')
                numberal = new_data.get('MONTHLY_select_range_numberals')
                obj.params = 'interval:{0};byweekday:{1}({2})'.format(interval, day, numberal)

            obj.save()

        # YEARLY
        # 'YEARLY_select_range_month': [u'February']
        # 'YEARLY_select_range_monthly': [u'15']
        if new_data.get('pattern') == 'YEARLY':
            obj.frequency = new_data.get('pattern')
            print request.POST
            if new_data['RADIO_yearly'] == '0':
                bymonthday = ','.join(map(str, new_data.get('YEARLY_select_range_monthly')))
                bymonth = new_data.get('YEARLY_select_range_month')
                # bymonthday = new_data.get('YEARLY_select_range_monthly')
                obj.params = 'bymonth:{0};bymonthday:{1};'.format(bymonth, bymonthday,)

            obj.save()



# admin.site.register(Calendar, CalendarAdminOptions)
admin.site.register(Rule, RuleAdmin)
admin.site.register(Event, EventAdmin)
#admin.site.register([Rule, Event, CalendarRelation])
admin.site.register(Category)

