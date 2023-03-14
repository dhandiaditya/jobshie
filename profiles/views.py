from django.shortcuts import render

# Create your views here.
'''

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm

@login_required
def profile(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    context = {'form': form}
    return render(request, 'profile.html', context)

@login_required
def create_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = UserProfileForm()
    context = {'form': form}
    return render(request, 'create_profile.html', context)


@login_required
def edit_profile(request):
    userprofile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=userprofile)
        if form.is_valid():
            userprofile = form.save(commit=False)  # don't save to DB yet
            userprofile.user = request.user  # set the user field
            userprofile.save()  # save to DB now
            return redirect('profile')
    else:
        form = UserProfileForm(instance=userprofile)

    context = {'form': form}
    return render(request, 'edit_profile.html', context)


    '''