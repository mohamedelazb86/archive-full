from django.shortcuts import render,redirect
from django.core.mail import send_mail

from .forms import SignForm,ActivateForm
from .models import Profile
from django.contrib.auth.models import User

# create function or new project
def signup(request):
    '''
    - create new user
    - stop activate this user
    - send email to this user
    - redirect activate html
    '''
    if request.method=='POST':
        form=SignForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            user=form.save(commit=False)
            user.is_active=False

            form.save()  #$ create new user and creat new profile
            profile=Profile.objects.get(user__username=username)
            # sendemail to this user
            send_mail(
            "Activate code ",
            f"Welcome mr {username} \n pls use this code {profile.code}",
            "r_mido99@yahoo.com",
            [email],
            fail_silently=False,
        )
            return redirect(f'/accounts/{username}/activate')


    else:
        form=SignForm()
    return render(request,'accounts/signup.html',{'form':form})

# create function to check this code for user

def activate_code(request,username):
    profile=Profile.objects.get(user__username=username)
    if request.method=='POST':
        form=ActivateForm(request.POST)
        if form.is_valid():
            code=form.cleaned_data['code']
            if code==profile.code:
                profile.code=''

                user=User.objects.get(username=username)
                user.is_active=True
                user.is_staff=True

                user.save()
                profile.save()

                return redirect('/accounts/login')
    else:
        form=ActivateForm()
    return render(request,'accounts/activate_code.html',{'form':form})
