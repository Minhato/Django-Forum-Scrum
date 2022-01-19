import time
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from user.forms import ProfileForm, SignUpForm
from .models import Profile



def signup(request):
	'''Create a user by using returned form.

    Keyword arguments:
    form -- input by SignUpForm
	
	'''

	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.profile.first_name = form.cleaned_data['first_name']
			user.profile.last_name = form.cleaned_data['last_name']
			user.profile.email = form.cleaned_data['email']
			user.profile.department = form.cleaned_data['department']
			user.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			return redirect('home')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})


def login(request):
	'''Login into user account. Authentificate by entering correct username and password.

    Keyword arguments:
    form -- input by AuthenticationForm
	
	'''

	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')


			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('home')	
			else:				
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()			
	return render(request=request, template_name="login.html", context={"login_form":form})


def profile(request):
	'''Update user-profile with returned image.

    Keyword arguments:
    form -- input by ProfileForm
	profile_obj -- object that is updated

	'''

	if request.method=="POST":
		current_user = request.user
		profile = Profile(user=current_user)
		form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)

		if form.is_valid():
			profile_obj = profile.save(update_fields=['image'])
			profile_obj = current_user.refresh_from_db()
			messages.success(request, "Your Profile Picture was updated.")
			return render(request, "profile.html",{'obj': profile_obj})
			
	else:
		form=ProfileForm()	
	return render(request, 'profile.html', {'form': form})
