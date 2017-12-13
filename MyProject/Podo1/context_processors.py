from settings import PORTAL_URL
from Prog.models import Group, Employee

def accounting_proc(request):
    return {'PORTAL_URL': request.build_absolute_uri ()}



def get_current_leader(request):
    """Returns currently selected group or None"""
    # we remember selected group in a cookie
    pk = request.COOKIES.get('current_leader')
    if pk:
        try:
            employee = Employee.objects.get(pk=int(pk))
        except Employee.DoesNotExist:
            return None
        else:
            return employee
    else:
        return None

def get_leader(request):
    """Returns list of existing groups"""
    # deferred import of Group model to avoid cycled imports
    # get currently selected group
    cur_leader = get_current_leader(request)
    employee = []
    for leader in Employee.objects.all().order_by('last_name'):
        leader.append({
            'id': leader.id,
            'last_name': leader.last_name,
            #'first_name': leader.first_name,
            'selected': cur_leader and cur_leader.id == employee.id and True or False})
    return employee

#For checkbox on main page
def leader_processor(request):
    return {'LEADER': get_leader(request)}


def get_current_group(request):
    """Returns currently selected group or None"""
    # we remember selected group in a cookie
    pk = request.COOKIES.get('current_group')
    if pk:
        try:
            group = Group.objects.get(pk=int(pk))
        except Group.DoesNotExist:
            return None
        else:
            return group
    else:
        return None


def get_groups(request):
    """Returns list of existing groups"""
    # deferred import of Group model to avoid cycled imports
    # get currently selected group
    cur_group = get_current_group(request)
    groups = []
    for group in Group.objects.all().order_by('title'):
        groups.append({
            'id': group.id,
            'title': group.title,
            'leader': group.leader and (u'%s %s' % (group.leader.first_name,group.leader.last_name)) or None,
            'selected': cur_group and cur_group.id == group.id and True or False})
    return groups

#For checkbox on main page
def groups_processor(request):
    return {'GROUPS': get_groups(request)}