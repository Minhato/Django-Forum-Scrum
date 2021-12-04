from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from user.forms import SignUpForm, PostForm
from django.contrib import messages
from django.views.generic import DetailView
from .models import Post
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
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

def nachricht(request):
	user = request.user
	nachricht = messages.info(request,f"You are now logged in as {user.username}.")
	return nachricht

def login(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
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
	field_value = 'user_id'
	post = Post.objects.get(pk=post_id)
	postuser = getattr(post, field_value)

	user_obj = User.objects.get(username=user)
	current_user = getattr(user_obj, 'id')

	if postuser == current_user:
		messages.success(request, "Your Post was successfully deleted")
		post.delete()
	else:
		messages.warning(request, "This Post was published by another user. You can only modify/delete your own!")
	return redirect('home')

def totallikes(request, pk):
	post = get_object_or_404(Post, id= request.POST.get('post_id'))
	print(post.pk)
	nachricht =Post.objects.get(id = post.pk)
	total_likes = nachricht.likes.count()
	return total_likes

def upvote(request, pk):
	print("upvote drin post pk =")
	post = get_object_or_404(Post, id= request.POST.get('post_id'))
	print(post.pk)
	post.likes.add(request.user)
	print("die likes")
	nachricht =Post.objects.get(id = post.pk)
	alle_Nutzer_Dislike = post.dislikes.all()
	if request.user in alle_Nutzer_Dislike:
		print("bin drin")
		post.dislikes.remove(request.user)
	else:
		print("bin nicht drin")
	total_dislikes = nachricht.dislikes.count()
	total_likes = nachricht.likes.count()
	post.votes = total_likes - total_dislikes
	post.save()			 
	print(post.votes)
	#return render(request,'post_detail.html', { 'all_likes': total_likes}) funktioniert nicht kp was für ein html reinkommt
	#return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))
	return redirect('post-detail', post.pk)


def downvote(request, pk):
	print("downvote drin post pk =")
	post = get_object_or_404(Post, id= request.POST.get('post_id2'))
	print(post.pk)
	post.dislikes.add(request.user)
	print("die dislikes")
	nachricht =Post.objects.get(id = post.pk)
	alle_Nutzer_like = post.likes.all()
	if request.user in alle_Nutzer_like:
		print("bin drin")
		post.likes.remove(request.user)
	else:
		print("bin nicht drin")
	total_dislikes = nachricht.dislikes.count()
	total_likes = nachricht.likes.count()
	post.votes = total_likes - total_dislikes
	post.save()			 
	print(post.votes)
	#return render(request,'post_detail.html', { 'all_likes': total_likes}) funktioniert nicht kp was für ein html reinkommt
	#return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))
	return redirect('post-detail', post.pk)

class PostDetailView(DetailView):
	model = Post
	template_name = 'post_detail.html'
	def get_context_data(self,*args, **kwargs):
		#user_menu = User.objects.all()
		totallikes = get_object_or_404(Post, id=self.kwargs('post_id'))
		dielikes = Post.objects.get(id = self.kwargs('post_id'))

		context = super(PostDetailView, self).get_context_data(**kwargs)
		context["total_likes"] = dielikes
		return context