from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.generic import CreateView, ListView
from .form import JobseekerSignUpForm,JobseekerForm, CompanySignUpForm, CompanyForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Jobseeker, Company
from django.contrib.auth.decorators import login_required, user_passes_test



class jobseeker_register(CreateView):
    model = User
    form_class = JobseekerSignUpForm
    template_name = '../templates/jobseeker_register.html'

    def form_valid(self, form):
        user = form.save()
        jobseeker_form = JobseekerForm(self.request.POST)
        if jobseeker_form.is_valid():
            jobseeker = jobseeker_form.save(commit=False)
            jobseeker.user = user
            jobseeker.save()
        login(self.request, user)
        return redirect('jobseeker_dashboard', user_id=user.id)


class company_register(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = '../templates/company_register.html'

    def form_valid(self, form):
        user = form.save()
        company_form = CompanyForm(self.request.POST)
        if company_form.is_valid():
            company = company_form.save(commit=False)
            company.user = user
            company.save()
        login(self.request, user)
        return redirect('jobseekers_profiles_view', user_id=user.id)


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_jobseeker:
                    return redirect('jobseeker_dashboard', user_id=user.id)
                elif user.is_company:
                    return redirect('jobseekers_profiles_view')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, '../templates/login.html', context={'form': AuthenticationForm()})


def logout_view(request):
    logout(request)
    return redirect('/')


SKILLS_CHOICES = [
    ('Python', 'Python'),
    ('Django', 'Django'),
    ('SaaS', 'SaaS'),
    ('AWS', 'AWS'),
]

@login_required
@user_passes_test(lambda u: u.is_jobseeker)
def jobseeker_profile_edit(request):
    jobseeker = Jobseeker.objects.get(user=request.user)
    if request.method == 'POST':
        form = JobseekerForm(request.POST, instance=jobseeker)
        if form.is_valid():
            jobseeker = form.save(commit=False)
            jobseeker.skills.clear()  # clear existing skills
            for skill in form.cleaned_data['skills']:
                jobseeker.skills.add(skill)
            jobseeker.save()
            form.save()
            return redirect('jobseeker_dashboard', user_id=request.user.id)
            
    else:
        initial_skills = jobseeker.skills.all()
        initial = {'skills': initial_skills}
        form = JobseekerForm(instance=jobseeker, initial=initial)
    context = {'jobseeker': jobseeker, 'form': form, 'skills_choices': SKILLS_CHOICES}
    
    return render(request, 'jobseeker_profile_edit.html', context)


@login_required
@user_passes_test(lambda u: u.is_company)
def company_profile_edit(request):
    company = Company.objects.get(user=request.user)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_dashboard', user_id=request.user.id)
            
    else:
        form = CompanyForm(instance=company)
    context = {'company': company, 'form': form}
    
    return render(request, 'company_profile_edit.html', context)

@login_required
@user_passes_test(lambda u: u.is_jobseeker)
def jobseeker_dashboard(request, user_id):
    # Get the currently logged-in user
    user = request.user
    # If the user is not a company, only allow them to view their own information
    if user.id != user_id:
        return HttpResponseForbidden()
    jobseeker = Jobseeker.objects.get(user=user_id)
    context = {
        'cover_photo': jobseeker.cover_photo,
        'full_name': jobseeker.full_name,
        'phone_number': jobseeker.phone_number,
        'location': jobseeker.location,
        'age': jobseeker.age,
        'gender': jobseeker.gender
    }
    return render(request, 'jobseeker_dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_company)
def company_dashboard(request, user_id):
    # Get the currently logged-in user
    user = request.user
    # If the user is not a company, only allow them to view their own information
    if user.id != user_id:
        return HttpResponseForbidden()
    company = Company.objects.get(user=user_id)
    context = {
       
        'phone_number': company.phone_number,
        'company_name': company.company_name,
        'designation': company.designation,

    }
    return render(request, 'company_dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_company)
def jobseekers_profiles_view(request):
    '''
    companys = Company.objects.all()
    jobseekers = Jobseeker.objects.all()
    context = {'companys': companys, 'jobseekers': jobseekers}
    return render(request, 'jobseekers_profiles_view.html', context)
    '''
    user = request.user
    #company = Company.objects.get(user=user_id)

    queryset = Jobseeker.objects.all()
    search_query = request.GET.get('q')
    if search_query:
        queryset = queryset.filter(
            Q(user__full_name__icontains=search_query) #|
            #Q(user__last_name__icontains=search_query)
        )
    else:
        view = SearchResultsListView()
        view.request = request
        queryset = view.get_queryset()

    context = {'jobseekers': queryset}
    return render(request, 'jobseekers_profiles_view.html', context)

@login_required
@user_passes_test(lambda u: u.is_company)
def jobseeker_dashboard_for_company(request, user_id):
        # Get the currently logged-in user
    user = request.user

    # Check if the user is an company
    if user.is_company:
        # If the user is an company, show them their own information
        if user.id == user_id:
            jobseeker = user.jobseeker
            context = {
                'cover_photo': jobseeker.cover_photo,
                'full_name': jobseeker.full_name,
                'phone_number': jobseeker.phone_number,
                'location': jobseeker.location,
                'age': jobseeker.age,
                'gender': jobseeker.gender
            }
            return render(request, 'compnany_dashboard.html', context)
        else:
            # If the user is a company but the requested user is not themselves, allow them to view the jobseeker's information
            jobseeker = Jobseeker.objects.get(user=user_id)
            context = {
                'cover_photo': jobseeker.cover_photo,
                'full_name': jobseeker.full_name,
                'phone_number': jobseeker.phone_number,
                'location': jobseeker.location,
                'age': jobseeker.age,
                'gender': jobseeker.gender
            }
            return render(request, 'jobseeker_dashboard_for_company.html', context)





'''
@login_required
@user_passes_test(lambda u: u.is_jobseeker)
def jobseeker_detail(request):
    jobseeker = Jobseeker.objects.get(user=request.user)
    context = {'jobseeker': jobseeker}
    return render(request, 'jobseeker_detail.html', context)
'''


class SearchResultsListView(ListView): # new
    model = Jobseeker
    context_object_name = 'jobseekers_profiles_view'
    template_name = '../templates/search_results.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # Retrieve filter parameters from the form
        gender = self.request.GET.get('gender')
        age = self.request.GET.get('age')
   

        # Apply filters to the query
        if gender:
            queryset = queryset.filter(gender = gender)
        if age:
            queryset = queryset.filter(age = age)


        return queryset

