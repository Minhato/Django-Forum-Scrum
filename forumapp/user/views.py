from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from user.forms import SignUpForm, PostForm, ProfileForm
from django.contrib import messages
from django.views.generic import DetailView
from .models import Post, Profile
import time

# Create your views here.
def home(request):
	posts = Post.objects.all()
	return render(request, 'threads.html', {'posts': posts})

#def threads(request):
 #   return render(request, 'threads.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
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
        "title": "OZONE: Create New Post"
    })
	return render(request, "create_post.html", context)

def post_detail(request, pk):
	posts = Post.objects.get(pk=pk)
	#template_name = 'post_detail.html'
	return render(request, 'post_detail.html', {'posts': posts})

def delete_post(request, post_id, user):
	post = Post.objects.get(pk=post_id)
	postuser = getattr(post, 'user_id')

	user_obj = User.objects.get(username=user)
	current_user = getattr(user_obj, 'id')

	if postuser == current_user:
		messages.success(request, "Your Post was successfully deleted")
		post.delete()
	else:
		messages.warning(request, "This Post was published by another user. You can only modify/delete your own!")
	return redirect('home')

def profile(request):
	if request.method=="POST":
		current_user = request.user
		profile = Profile(user=current_user)
		form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)

		if form.is_valid():
			form.save()
			profile_obj = form.instance
			messages.success(request, "Your Profile Picture was updated.")
			return render(request, "profile.html",{'obj': profile_obj})
	else:
		form=ProfileForm()	
	return render(request, 'profile.html', {'form': form})