from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import DetailView
from .models import Post
from user.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from .forms import CommentForm, PostForm
from django.contrib import messages
from django.views.generic import DetailView
import time
from .nlp import check_and_censor


# Create your views here.
def home(request):
	posts = Post.objects.all()
	return render(request, 'threads.html', {'posts': posts})

def create_post(request):
#Here the logic behind the Create Post is done
#The Form is saved with the input and the current user
	context = {}
	form = PostForm(request.POST or None)


	# Hier PrÃ¼fung nach dem Inhalt, falls zu verletzend wird auf hauptseite redirected
	new_post = form.save(commit=False)



	#if new_post.content == str.empty:
	#	print("kein inhalt")
	#	return redirect('home')
		


	cleaned_content = check_and_censor(new_post.content)

	
	if cleaned_content == True:
		print('in der if')
		return redirect('home')
	

	print("weiter")
	if request.method == "POST":
		


		if form.is_valid():

			print("\n\n its valid")
			#new_post = form.save(commit=False)
			print(new_post.content)


			
			#cleaned_content = check_and_censor(new_post.content)
			
			


			new_post.content = cleaned_content
			new_post.user = request.user
			new_post.save()
			form.save_m2m()
			return redirect('home')
		
	context.update({
    	"form": form,
    })


	print("return ende")
	return render(request, "create_post.html", context)

def post_detail(request, pk):
	posts = Post.objects.get(pk=pk)	
	comments = posts.comments.filter(post_id=pk)
	
	return render(request, 'post_detail.html', {'posts': posts, 'comments': comments})

def edit_thread(request, post_id, user):
	field_value = 'user_id'
	post = Post.objects.get(pk=post_id)
	postuser = getattr(post, field_value)
	user_obj = User.objects.get(username=user)
	current_user = getattr(user_obj, 'id')
	if postuser == current_user:
		if request.method != 'POST':
			form=PostForm(instance=post)
		
		else:
			form = PostForm(instance=post, data=request.POST)
			if form.is_valid():
				form.save()
				return redirect('home')
		context = {'post': post, 'form': form}
		return render(request, 'edit_thread.html', context)
	else:
		messages.warning(request, "This Post was published by another user. You can only modify/delete your own!")
	return redirect('home')

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


def search_threads(request):
	if 'searched' in request.GET:
		searched = request.GET['searched']
		post = Post.objects.filter(title__icontains=searched)
		print(post) #wird nicht zurückgegeben hier Fehler
	else:	
		post = Post.objects.all()
	
	context = {'searched' :  searched, 'search' : post}
	return render(request, 'search_threads.html', context)

def create_comment(request, post_id):
	
	posts = Post.objects.get(pk=post_id)	
	comments = posts.comments.filter(post_id=post_id)

	if request.method=="POST":
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = posts
			new_comment.save()
	else:
		comment_form = CommentForm()

	return render(request, 'create_comment.html', {'comments': comments})