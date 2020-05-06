from django.shortcuts import render, get_object_or_404 
from pms.models import Student, Supervisor, SupervisorPreference, EligibleStudent
from pms.forms import (UserForm, StudentProfileForm, LoginForm, SearchForm, SupervisorProfileForm,
                        EligibleStudentForm, UploadFileForm, SupervisorPreferenceForm)
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User, Group
from django.views.generic import TemplateView, CreateView, ListView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from ga.pystsup.utilities.generateData import getData
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
import django_excel as excel
from itertools import chain
from ga.ga import runGA
import subprocess
import json
import re
import os


def admin_check(user):
    return user.groups.filter(name='admin').count()

def super_check(user):
    return user.groups.filter(name='superadmin').count()

def student_check(user):
    return user.groups.filter(name='student').count()

def supervisor_check(user):
    return user.groups.filter(name='supervisor').count()

def paging(request, object_list, count):
    paginator = Paginator(object_list, count) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return page, posts

def index(request):
    student = Group.objects.get(name='student').user_set.all()
    admin = Group.objects.get(name='admin').user_set.all()
    supervisor = Group.objects.get(name='supervisor').user_set.all()
    if request.user.is_authenticated:
        if request.user in admin:  
            return HttpResponseRedirect(reverse('pms:cord'))
        elif request.user in student:
            return HttpResponseRedirect(reverse('pms:student'))
        elif request.user in supervisor:
            return HttpResponseRedirect(reverse('pms:supervisor'))
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                usr_name = re.sub(r'\W+', '', cd['username'])
                user = authenticate(request,username=usr_name, password=cd['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        if user in admin:  
                            return HttpResponseRedirect(reverse('pms:cord'))
                        elif user in student:
                            return HttpResponseRedirect(reverse('pms:student'))
                        elif user in supervisor:
                            return HttpResponseRedirect(reverse('pms:supervisor'))
                    else:
                        messages.error(request, 'Disbaled Account. See your Cordinator')
                else:
                    messages.error(request, 'Wrong Username or Password')
        else:
            form = LoginForm()
    return render(request, 'index.html', {'form': form})

def reg_done(request):
    return render(request,'register_done.html')

@login_required
def student_profile(request):
    return render(request,'student/profile.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

@login_required
def allstudent(request):
    stds = Student.objects.all()
    page, std = paging(request, stds, 15)
    return render(request,'student/student.html', {'std':std, 'page':page })

@login_required
def allsup(request):
    sups = Supervisor.objects.all()
    page, sup = paging(request, sups, 15)
    return render(request,'supervisor/supervisor.html', {'sup':sup, 'page':page })

@user_passes_test(admin_check)
@login_required
def alladmin(request):
    sups = User.objects.filter(groups='3')
    page, admin = paging(request, sups, 15)
    return render(request,'cordinator/admin.html', {'admin':admin, 'page':page })

@user_passes_test(admin_check)
@login_required
def upload(request):
    if request.method == "POST":
        if 'bash' in request.POST:
            fileform = UploadFileForm(request.POST, request.FILES)
            if fileform.is_valid():
                try:
                    request.FILES['sheet'].save_to_database( model=EligibleStudent, mapdict=['matricNo', 'name'])
                # request.FILES['sheet'].save_to_database( model=User, mapdict=['username', 
                # 'first_name', 'last_name', 'password', 'email' ])
                    messages.success(request, 'Upload was Succesful')
                except:
                    messages.error(request, 'Students Data has been uploaded  before')
            else:
                messages.error(request, 'Error Uploading File')
            el_form = EligibleStudentForm()

        elif 'single' in request.POST:
            el_form = EligibleStudentForm(request.POST)
            if el_form.is_valid():
                try:
                    el_form.save()
                    messages.success(request, 'Student Added Succesfully')
                except:
                    messages.error(request, 'Students Data already exist')
            else:
                messages.error(request, 'Error adding Student')
            fileform = UploadFileForm()
    else:
        fileform = UploadFileForm()
        el_form = EligibleStudentForm()
    return render(request, 'cordinator/upload_student.html', {'fileform': fileform, 'el_form': el_form })

@user_passes_test(admin_check)
@login_required
def std_upload(request):
    if request.method == "POST":
        fileform = UploadFileForm(request.POST, request.FILES)
        if fileform.is_valid():
            try:
                request.FILES['sheet'].save_to_database( model=User, mapdict=['username', 
                'first_name', 'last_name', 'password', 'email' ])
                messages.success(request, 'Upload was Succesful')
            except:
                messages.error(request, 'Students Data has been uploaded  before')
        else:
            messages.error(request, 'Error Uploading File')
    else:
        fileform = UploadFileForm()
    return render(request, 'cordinator/upload_std.html', {'fileform': fileform })

@user_passes_test(admin_check)
@login_required
def uploadview(request):
    return excel.make_response_from_tables(['matricNo', 'name'], 'uploadview.html')


def register(request):

    #get all username in user model
    eligible = EligibleStudent.objects.values_list('matricNo', flat=True)
    
    if request.method == 'POST':
        
        userform = UserForm(request.POST)
        profileform = StudentProfileForm(request.POST, request.FILES)

        if userform.is_valid() and profileform.is_valid():
            cd = userform.cleaned_data

            if cd['username'] in eligible:
                user = userform.save(commit=False)
                user_p = profileform.save(commit=False)
                user.set_password(cd['password'])
                user.save()

                #assigning current registered user to profile
                user_p.user = user
                user_p.save()

                #adding user to group
                Group.objects.get(name="student").user_set.add(user)
                return HttpResponseRedirect(reverse('pms:index'))
            else:
                messages.error(request, 'Ineligible for registration..Meet the Cordinator')
    else:
        userform = UserForm()
        profileform = StudentProfileForm()
    return render(request,'student/register.html',{'userform': userform, 'profileform': profileform})

@user_passes_test(admin_check)
@login_required
def sup_register(request):
    
    if request.method == 'POST':
        
        userform = UserForm(request.POST)
        profileform = SupervisorProfileForm(request.POST, request.FILES)
        
        if userform.is_valid() and profileform.is_valid():
            cd = userform.cleaned_data
            cf = profileform.cleaned_data
            user = userform.save(commit=False)
            user_p = profileform.save(commit=False)
            user.set_password(cd['password'])
            user.save()

            #assigning current registered user to profile
            user_p.user = user
            user_p.save()

            #adding user to group
            Group.objects.get(name="supervisor").user_set.add(user)
            return HttpResponseRedirect(reverse('pms:super_detail', args=[ cf['surname'].lower() ]))
        else:
            messages.error(request, 'Invalid Form Submision')
    else:
        userform = UserForm()
        profileform = SupervisorProfileForm()
    return render(request,'supervisor/register.html',{'userform': userform, 'profileform': profileform})


@user_passes_test(super_check)
@login_required
def admin_register(request):
    
    if request.method == 'POST':
        
        userform = UserForm(request.POST)
        
        if userform.is_valid():
            cd = userform.cleaned_data
            user = userform.save(commit=False)
            user.set_password(cd['password'])
            user.save()

            #adding user to group
            Group.objects.get(name="admin").user_set.add(user)
            messages.success(request, 'Admin Added Succesfully')
        else:
            messages.error(request, 'Invalid Form Submision')
    else:
        userform = UserForm()
    return render(request,'cordinator/register.html',{'userform': userform})

def std_register(request):
    
    if request.method == 'POST':
        
        userform = UserForm(request.POST)
        profileform = StudentProfileForm(request.POST, request.FILES)
        
        if userform.is_valid() and profileform.is_valid():
            cd = userform.cleaned_data
            cf = profileform.cleaned_data
            user = userform.save(commit=False)
            user_p = profileform.save(commit=False)
            user.set_password(cd['password'])
            user.save()

            #assigning current registered user to profile
            user_p.user = user
            user_p.save()

            #adding user to group
            Group.objects.get(name="student").user_set.add(user)
            return HttpResponseRedirect(reverse('pms:student_detail', args=[ cd['username'].lower() ]))
        else:
            messages.error(request, 'Invalid Form Submision')
    else:
        userform = UserForm()
        profileform = StudentProfileForm()
    return render(request,'student/register.html',{'userform': userform, 'profileform': profileform})


class eligible(ListView):
    model = EligibleStudent
    def get_queryset(self):
        return EligibleStudent.objects.all()
    
@login_required
class uploadCreateView(CreateView):
    model = EligibleStudent
    template_name = "coordinator/upload"
    success_url = reverse_lazy('eligble_student')

@login_required
def searchs(request):
    results = ""
    page = ""
    name = "Student"
    query = request.GET.get("q")
    if query:
        sup = Supervisor.objects.filter(Q(user__username__icontains=query)|Q(surname__icontains=query)|
                Q(user__last_name__icontains=query)|Q(user__first_name__icontains=query) )
                
        std = Student.objects.filter(Q(user__username__icontains=query)|Q(surname__icontains=query)|
                Q(user__last_name__icontains=query)|Q(user__first_name__icontains=query) )
        total = sup.count() + std.count()
        result = list(chain(sup, std))
        page, results = paging(request, result, 7)
        
    return render(request, 'search.html', {'results': results, 'page':page, 'query':query, 'name': name, 'total':total})

@login_required
def cord(request):
    if request.user.is_authenticated:
        el_std = EligibleStudent.objects.all().count
        std = Student.objects.all()
        sup = Supervisor.objects.all().count
        reg_std = Student.objects.filter(supervisor__isnull=True).count
        al_sup = std.values_list("supervisor__surname", flat=True).distinct()
        
    return render(request, 'cordinator/profile.html', {"el_std":el_std, "std":std.count, "sup":sup, 
                                                    "reg_std":reg_std, "al_sup":al_sup.count})

def simpleForm(request, formName, url):
    if request.method == "POST":
        form = formName(request.POST)
        if form.is_valid():
            std = form.save(commit=False)
            std.user = request.user
            std.save()
            messages.success(request, 'Added Succesfully')
        else:
            messages.error(request, "Error in Form Submissionsss")
    else:
        form = formName()
    return form

@login_required
def supervisor(request):
    prefer = SupervisorPreference.objects.filter(user=request.user)
    allocated = Student.objects.filter(supervisor=request.user.supervisors)
    if request.method == "POST":
        preferForm = SupervisorPreferenceForm(request.POST)
        if preferForm.is_valid():
            std = preferForm.save(commit=False)
            std.user = request.user
            std.save()
            messages.success(request, "Added Succesfully")
    else:
        preferForm = SupervisorPreferenceForm()
    return render(request, 'supervisor/profile.html', {'prefer':prefer, 'preferForm': preferForm, 'allocated': allocated})

@login_required
def super_profile(request):
    data = get_object_or_404(Supervisor, user=request.user )
    return render(request, 'supervisor/myprofile.html', {'data': data})

@login_required
def student(request):
    data = get_object_or_404(Student, user=request.user )
    return render(request, 'student/profile.html', {'data': data })

@login_required                                
def student_profile(request):
    data = get_object_or_404(Student, user=request.user )
    return render(request, 'student/profiledetail.html', {'data': data})                                

@login_required
def student_detail(request, username):
    data = get_object_or_404(Student, slug=username )
    return render(request, 'student/profiledetail.html', {'data': data})

@login_required
def super_detail(request, surname):
    data = get_object_or_404(Supervisor, slug=surname )
    std = Student.objects.filter(supervisor__surname=surname.capitalize())
    return render(request, 'supervisor/profiledetail.html', {'data': data, "std":std})

def mypage(request):
    return render(request, 'test/mypage.html')

def faq_search_autocomplete(request):
    if request.is_ajax():
        q = request.GET.get('q')
        names = User.objects.filter(username__istartswith=q)

        result = []
        for name in names:
            name_json = {}
            name_json['id'] = name.id
            name_json['label'] = name.username
            name_json['value'] = name.username
            result.append(name_json)
        data = json.dumps(result)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@login_required
def allocate(request):
    suplist = Supervisor.objects.all().values_list("user__username","surname", "user__first_name", 
                                                    "user__last_name","capacity","AOC1", "AOC2")
    stulist = Student.objects.all().values_list("user__username","surname", "user__first_name", "user__last_name",
                                                "AOC1", "AOC2", "supervisor_1__surname", "supervisor_2__surname")

    file_path = os.path.join(settings.MEDIA_ROOT, "acm.txt")
    form = UploadFileForm(request.POST, request.FILES)
    
    if request.POST.get("submit"):
        subprocess.call(["gnome-terminal -x python ga.py"], stdout=subprocess.PIPE, stderr=None, shell=True )
    
    elif request.POST.get("submit2"):
        messages.error(request, "Student's Count is higher than Total Supervisor Capacity.")
    count = 0
    for i in range(1, len(suplist)):
        count += suplist[i][4]

    return render(request, 'cordinator/allocate.html', {"form":form, "count":count, "std": stulist.count} )

@user_passes_test(super_check)
@login_required
def deactivate(request, pk, group):        
    user = get_object_or_404(User, pk=pk)
    user.is_active = False
    user.save()
    if group == "admin":
        return HttpResponseRedirect(reverse('pms:admin_list'))
    elif group == "supervisor":
        return HttpResponseRedirect(reverse('pms:sup_list'))
    elif group == "student":
        return HttpResponseRedirect(reverse('pms:std_list'))

@user_passes_test(super_check)
@login_required  
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    stds = Student.objects.all()
    page, std = paging(request, stds, 15)
    data = dict()
    context = {'page':page, 'std':std}
    if request.method == 'POST':
        user.delete()
        data['form_is_valid'] = True
        data['stdlist'] = render_to_string('student/student.html', context, request=request)
    else:
        context = {'user': user}
        data['request_form'] = render_to_string('cordinator/delete_user.html', context, request=request)
    return JsonResponse(data)

@user_passes_test(super_check)
@login_required  
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    data = dict()
    
    if request.method == 'POST':
        userform = UserForm(request.POST, instance=user)
        profileform = StudentProfileForm(request.POST, instance=user.students)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            data['form_is_valid'] = True
            userlist = get_object_or_404(Student, user__pk=pk)
            context = {'userlist': userlist}
            data['stdlist'] = render_to_string('student/profiledetail.html', context, request=request)
        else:
            messages.error(request, 'Error updating your profile')

    else:
        userform = UserForm(instance=user)
        profileform = StudentProfileForm(instance=user.students)
    context = {'userform': userform, 'profileform':profileform }
    data['request_form'] = render_to_string('student/edit.html', context, request=request)
    return JsonResponse(data)
