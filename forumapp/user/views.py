from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from user.forms import SignUpForm
from django.contrib import messages
import logging

logger = logging.getLogger("meinLogger")
# Create your views here.
def home(request):
    return render(request, 'base.html')


def signup(request):
    if request.method == 'POST':
		#ruft die Methode SignupForm auf die wir geschrieben haben in forms.py 
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
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

def login(request):
	#TO:DO delete logs, kp wie man prints anschauen kann im terminal
	print("hallo")
	logging.info("Hallo")
	logger.info("hallo2")
	logging.error("TEST")
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
				#quasi wenn user vorhanden, dann wird eingeloggt
				login(request, user)
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})