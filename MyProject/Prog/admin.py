# coding=utf-8
from django.contrib import admin
from .models import Employee, Group, MonthJournal
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError

class EmployeeFormAdmin(ModelForm):
    def clean_employee_group(self):

        # get group where current employee is a leader
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and self.cleaned_data['employee_group'] != groups[0]:
            raise ValidationError(u'Працівник є керівником іншого проекту.', code='invalid')

        return self.cleaned_data['employee_group']

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'level', 'employee_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['employee_group']
    ordering = ['last_name']
    list_filter = ['employee_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name', 'level', 'notes']
    form = EmployeeFormAdmin

    def view_on_site(self, obj):
        return reverse('employee_edit', kwargs={'pk': obj.id})

# Register your models here.
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Group)
admin.site.register(MonthJournal)


