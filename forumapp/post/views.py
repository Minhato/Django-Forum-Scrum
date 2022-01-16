from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import DetailView
from .models import Post, Comment, User
from .models import Post
from user.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from .forms import CommentForm, PostForm
from django.contrib import messages
from django.views.generic import DetailView
import time
from django.conf import settings
#from .nlp import check_and_censor
from django.core.mail import send_mail


# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request, 'threads.html', {'posts': posts})

def create_post(request):
#Here the logic behind the Create Post is done
#The Form is saved with the input and the current user
    context = {}
    form = PostForm(request.POST, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            print("\n\n its valid")
            new_post = form.save(commit=False)
            #cleaned_content = check_and_censor(new_post.content)
            cleaned_content = new_post.content
            if cleaned_content == True:
                    print('in der if')
                    return redirect('home')
            new_post.content = cleaned_content
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            form.save()
            return redirect('home')
    context.update({
        "form": form,
    })
    return render(request, "create_post.html", context)

def post_detail(request, pk):
	posts = Post.objects.get(pk=pk)	
	comments = posts.comments.filter(post_id=pk, parent = None)
	
	return render(request, 'post_detail.html', {'posts': posts, 'comments': comments})



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

def send_email(post_id, betreff, nachricht, email):
    send_mail(subject= betreff, message= nachricht, from_email= settings.EMAIL_HOST_USER, recipient_list= ['simplyforumcrew@gmail.com', email], fail_silently= False)
    #send_mail('test mail', 'Test body', 'simplyforumcrew@gmail.com', ['simplyforumcrew@gmail.com'])
    return redirect(f'post/{post_id}')


def upvote_comment(request, pk):
	print("upvote drin post pk =")
	comment = get_object_or_404(Comment, id= request.POST.get('comment_id'))
	print(comment.pk)
	comment.likes.add(request.user)
	print("die likes")
	nachricht =Comment.objects.get(id = comment.pk)
	alle_Nutzer_Dislike = comment.dislikes.all()
	if request.user in alle_Nutzer_Dislike:
		print("bin drin")
		comment.dislikes.remove(request.user)
	else:
		print("bin nicht drin")
	total_dislikes = nachricht.dislikes.count()
	total_likes = nachricht.likes.count()
	comment.votes = total_likes - total_dislikes
	comment.save()			 
	print(comment.votes)
	#return render(request,'post_detail.html', { 'all_likes': total_likes}) funktioniert nicht kp was für ein html reinkommt
	#return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))
	return redirect('post-detail', pk)

def downvote_comment(request, pk):
	print("downvote drin post pk =")
	comment = get_object_or_404(Comment, id= request.POST.get('comment_id2'))
	print(comment.pk)
	comment.dislikes.add(request.user)
	print("die dislikes")
	nachricht =Comment.objects.get(id = comment.pk)
	alle_Nutzer_like = comment.likes.all()
	if request.user in alle_Nutzer_like:
		print("bin drin")
		comment.likes.remove(request.user)
	else:
		print("bin nicht drin")
	total_dislikes = nachricht.dislikes.count()
	total_likes = nachricht.likes.count()
	comment.votes = total_likes - total_dislikes
	comment.save()			 
	print(comment.votes)
	#return render(request,'post_detail.html', { 'all_likes': total_likes}) funktioniert nicht kp was für ein html reinkommt
	#return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))
	return redirect('post-detail', pk)
	
def search_threads(request):
    if 'searched' in request.GET:
        searched = request.GET['searched']
        post = Post.objects.filter(title__icontains=searched)
        print(post) #wird nicht zurückgegeben hier Fehler
    else:	
        post = Post.objects.all()
    
    context = {'searched' :  searched, 'search' : post}
    return render(request, 'search_threads.html', context)

def create_comment(request):

    if request.method=="POST":
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        user = request.user
        comment = request.POST.get('comment_content')
        reply = request.POST.get('reply_content')
        parent_id = request.POST.get("parent_id")
        nachricht = 'Du hast eine neue Antwort! :' + str(comment) 
        field_object = Post._meta.get_field('user')
        email = getattr(post,'user')
        post_user_id = getattr(post,'user_id')
        post_user = User.objects.get(id = post_user_id)
        post_user_email = getattr(post_user, 'email')
        print(post_user_email)


        if parent_id == None:
            comment_form = Comment(post=post, user=user, comment_content=comment)
            comment_form.save()
            send_email(post_id,'Neue Antwort auf deinen Post!', nachricht, post_user_email)
            messages.success(request, "Your comment has been posted successfully")
        else:
            comment_form = Comment(post=post, user=user,  comment_content = reply, parent_id =parent_id)
            comment_form.save()
            send_email(post_id,'Neue Antwort auf dein Kommentar', nachricht, post_user_email)
            messages.success(request, "Your reply has been posted successfully")
    else:
        comment_form = Comment()
        messages.success(request, "Your comment couldn't be posted")

    return redirect(f'post/{post_id}')


def delete_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    commentuser_id = getattr(comment, 'user_id')
    post_id = getattr(comment, 'post_id')

    user_obj = User.objects.get(pk=commentuser_id)
    commentuser = getattr(user_obj, 'username')

    current_user = request.user

    if     str(commentuser) == str(current_user) or request.user.is_superuser:
        messages.success(request, "Your Comment was successfully deleted")
        comment.delete()
    else:
        messages.warning(request, "This Comment was published by another user. You can only delete your own!")
    return redirect('post-detail', post_id)



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
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('home')
        context = {'post': post, 'form': form}
        return render(request, 'edit_thread.html', context)
    else:
        messages.warning(request, "This Post was published by another user. You can only modify/delete your own!")
    return redirect('home')

