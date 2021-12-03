from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from user.forms import SignUpForm, PostForm
from django.contrib import messages
import logging
from .models import Post

logger = logging.getLogger("meinLogger")
# Create your views here.
def home(request):
	posts = Post.objects.all()
	return render(request, 'threads.html', {'posts': posts})

#def threads(request):
 #   return render(request, 'threads.html')

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
				messages.info(request, f"You are now logged in as {username}.")
				return redirect('home')
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def create_post(request):
#Here the logic behind the Create Post is done
#The Form is saved with the input and the current user
	context = {}
	form = PostForm(request.POST or None)
	if request.method == "POST":
		if form.is_valid():
			print("\n\n its valid")
			new_post = form.save(commit=False)
			new_post.user = request.user
			new_post.save()
			form.save_m2m()
			return redirect('home')
	context.update({
    	"form": form,
    })
	return render(request, "create_post.html", context)


def edit_thread(request, post_id):
# Function for the Edit of an existing Thread
    post = Post.objects.get(id=post_id)	
    if request.method != 'POST':
        form = PostForm(instance=post)

    else:
        form = PostForm(instance=post, data=request.POST) 
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'post': post, 'form': form}
    return render(request, 'edit_thread.html', context)
