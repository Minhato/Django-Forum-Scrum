from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
#from user.forms import SignUpForm
from django.contrib import messages
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
#from forumapp.user.forms import SignUpForm
from user.forms import ProfileForm, SignUpForm
from django.contrib import messages
from django.views.generic import DetailView
from .models import Profile
import time



#def threads(request):
 #   return render(request, 'threads.html')

def signup(request):
    if request.method == 'POST':
		#ruft die Methode SignupForm auf die wir geschrieben haben in forms.py 
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
			#nutzt das authenticationForm von django 
            user = authenticate(username=username, password=raw_password)
			#login auskommentiert da wir nur wollen dass man sich registriert ohne automatisches einloggen
            #login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def nachricht(request):
	user = request.user
	nachricht = messages.info(request,f"You are now logged in as {user.username}.")
	return nachricht

def login(request):
	if request.method == "POST":
		#nutzt das template von django
		print("in POST ")
		form = AuthenticationForm(request, data=request.POST)
		#um zu prüfen ob die Form richtig ist, idk ob nötig
		if form.is_valid():
			print("Form ist valid")
			#return ein python objekt 
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			print("TEST")
			print(username, " und passwort ", password )

			user = authenticate(username=username, password=password)
			if user is not None:
				print("test")
				login(request, user)
				return redirect('home')	
				#messages.info(request, f"You are now logged in as {username}.")		
			else:
				
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	nachricht()				
	return render(request=request, template_name="login.html", context={"login_form":form})

def profile(request):
	if request.method=="POST":
		current_user = request.user
		profile = Profile(user=current_user)
		form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)

		if form.is_valid():
			#form.save()
			profile_obj = profile.save(update_fields=['image'])
			messages.success(request, "Your Profile Picture was updated.")
			return render(request, "profile.html",{'obj': profile_obj})
	else:
		form=ProfileForm()	
	return render(request, 'profile.html', {'form': form})
