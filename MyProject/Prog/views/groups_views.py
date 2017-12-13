# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from Prog.models import Group, Employee
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Podo1.context_processors import get_current_leader
from django.forms import ModelForm
from django.views.generic import UpdateView, DeleteView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


###############################################################################################
def groups_list(request):
    groups = Group.objects.all ()

    # try to order groups list
    order_by = request.GET.get ('order_by', '')
    if order_by in ('title', 'leader'):
        groups = groups.order_by (order_by)
    if request.GET.get ('reverse', '') == '1':
        groups = groups.reverse ()

    # paginate groups
    paginator = Paginator (groups, 5)
    page = request.GET.get ('page')
    try:
        groups = paginator.page (page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        groups = paginator.page (1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver
        # last page of results.
        groups = paginator.page (paginator.num_pages)

    return render (request, 'Prog\\groups\\groups_list.html', {'groups': groups})


###################################################################################################
@login_required
def groups_add(request):
    # was form posted?
    if request.method == "POST":
        # was form add button clicked?
        if request.POST.get ('add_button') is not None:
            errors = {}
            # validate group data will go here
            data = {#'notes': request.POST.get ('notes')
                    }
            # validate user input
            title = request.POST.get ('title', '').strip ()
            if not title:
                errors['title'] = u"Назва проекту є обов'язковою"
            else:
                data['title'] = title

            leader = request.POST.get ('leader', '').strip ()
            if not leader:
                errors['leader'] = u"Оберіть проект для працівника"
            else:
                groups = Employee.objects.filter (pk=leader)
                if len (groups) != 1:
                    errors['leader'] = u"Оберіть коректний проект"
                else:
                    data['leader'] = groups[0]


            employee = request.POST.get ('employee', '').strip ()

            if not employee:
                errors['employee'] = u"Оберіть працівників"
            else:
                groups = Group.objects.filter (pk=employee)
                if len (groups) != 1:
                    errors['employee'] = u"Оберіть коректного працівника"
                else:
                    data['employee'] = groups[0]

            if not errors:
                # create employee object
                group = Group (
                    title=request.POST['title'],
                    leader=request.POST['leader'],
                    employee_group=Group.objects.get (pk=request.POST['employee_group']),
                    notes=request.POST['notes'],
                )
                # save it to database
                group = Group (**data)
                group.save ()

                # redirect user to employees list
                return HttpResponseRedirect (u'%s?status_message=Проект успішно створено!' % reverse ('groups'))

            else:
                # render form with errors and previous user input
                return render (request, 'Prog\\groups\\groups_add.html',
                               {'leader': Employee.objects.all ().order_by ('last_name'),
                                'errors': errors})
        elif request.POST.get ('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect (u'%s?status_message=Створення проекту скасовано!' % reverse ('groups'))
    else:
        # initial form render
        return render (request, 'Prog\\groups\\groups_add.html',
                       {'employee': Employee.objects.all().order_by('last_name')})


#######################################################################################
class GroupUpdateForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(GroupUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # set form tag attributes
        self.helper.form_action = reverse('groups_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.layout[-1] = FormActions(
        Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
        Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),)

class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'Prog\\groups\\groups_edit.html'
    form_class = GroupUpdateForm

    @method_decorator (login_required)
    def dispatch(self, *args, **kwargs):
        return super (GroupUpdateView, self).dispatch (*args, **kwargs)

    def get_success_url(self):
        return u'%s?status_message=Проект успішно збережено!' % reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Редагування проекту відмінено!' % reverse('groups'))
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)

####################################################################################
class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'Prog\groups\groups_delete.html'

    @method_decorator (login_required)
    def dispatch(self, *args, **kwargs):
        return super (GroupDeleteView, self).dispatch (*args, **kwargs)

    def get_success_url(self):
        return u'%s?status_message=Проект успішно видалено!' % reverse('home')