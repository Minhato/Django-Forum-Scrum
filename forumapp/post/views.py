import time
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from user.models import User
from .forms import CommentForm, PostForm
from .models import Comment, Post, User
from .nlp import check_and_censor


def home(request):
    '''Go back to home and open all posts.

    Keyword arguments:
    posts -- all posts in database

    '''
    posts = Post.objects.all()
    return render(request, 'post.html', {'posts': posts})


def create_post(request):
    '''Create a post by using returned form. Content is cleaned and saved.

    Keyword arguments:
    form -- input by PostForm

    '''
    context = {}
    form = PostForm(request.POST, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            new_post = form.save(commit=False)
            cleaned_content = check_and_censor(new_post.content)
            if cleaned_content == True:
                    messages.warning(request, "Your post was not published. The content was too explicit.")
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


def edit_post(request, post_id, user):
    '''Edit a post by using returned form. Previous post is overwritten by using new data, if user is the creator of post. Content is cleaned and saved. 

    Keyword arguments:
    form -- input by PostForm
    post -- assessed post by primary key

    '''
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
                
                post = form.save(commit=False)

                cleaned_content = check_and_censor(post.content)
                if cleaned_content == True:
                    messages.warning(request, "Your changes were not saved. The content was too explicit.")
                    return redirect('home')
                post.content = cleaned_content
                post.save()

                form.save()
            return redirect('home')
        context = {'post': post, 'form': form}
        return render(request, 'edit_post.html', context)
    else:
        messages.warning(request, "This Post was published by another user. You can only modify your own!")
    return redirect('home')


def delete_post(request, post_id, user):
    '''Delete a post if user is the creator of post. Admin can always delete.

    Keyword arguments:
    post -- assessed post by primary key

    '''
    post = Post.objects.get(pk=post_id)
    postuser = getattr(post, 'user_id')

    user_obj = User.objects.get(username=user)
    current_user = getattr(user_obj, 'id')

    if postuser == current_user or request.user.is_superuser:
        messages.success(request, "Your Post was successfully deleted.")
        post.delete()
    else:
        messages.warning(request, "This Post was published by another user. You can only modify/delete your own!")
    return redirect('home')


def post_detail(request, pk):
    '''Return post and its comments by primary key. 

    Keyword arguments:
    posts -- assessed post by primary key
    comments -- all comments that belong to posts

    '''
    posts = Post.objects.get(pk=pk)	
    comments = posts.comments.filter(post_id=pk, parent = None)
    return render(request, 'post_detail.html', {'posts': posts, 'comments': comments})


def search_post(request):
    '''Filter for post titles. 

    Keyword arguments:
    searched -- entered input

    '''

    if 'searched' in request.GET:
        searched = request.GET['searched']
        if searched == '':
            return redirect('home')
        post = Post.objects.filter(Q(title__contains=searched) | Q(description__contains=searched))
    context = {'searched' :  searched, 'search' : post}
    return render(request, 'search_post.html', context)


def totallikes(request, pk):
    '''Return total sum of likes and dislikes. 

    Keyword arguments:
    total_likes -- count of likes

    '''
    post = get_object_or_404(Post, id= request.POST.get('post_id'))
    message = Post.objects.get(id = post.pk)
    total_likes = message.likes.count()
    return total_likes


def upvote(request, pk):
    '''Upvote a post. Creates sum of likes and dislikes and calculates total votes.

    Keyword arguments:
    total_dislikes -- number of all dislikes that belong to the post
    total_likes -- number of all likes that belong to the post

    '''
    post = get_object_or_404(Post, id= request.POST.get('post_id'))
    post.likes.add(request.user)
    message = Post.objects.get(id = post.pk)
    alle_Nutzer_Dislike = post.dislikes.all()
    # zum prüfen ob Nutzer bereits im Dislike ist, wenn ja dann lösche Ihn daraus
    # Um ein Liken und gleichzeitiges disliken zu verhindern
    if request.user in alle_Nutzer_Dislike:
        post.dislikes.remove(request.user)
    total_dislikes = message.dislikes.count()
    total_likes = message.likes.count()
    post.votes = total_likes - total_dislikes
    post.save()			 
    return redirect('post-detail', post.pk)


def downvote(request, pk):
    '''Downvote a post. Creates sum of likes and dislikes and calculates total votes.

    Keyword arguments:
    total_dislikes -- number of all dislikes that belong to the post
    total_likes -- number of all likes that belong to the post

    '''
    post = get_object_or_404(Post, id= request.POST.get('post_id2'))
    post.dislikes.add(request.user)
    message = Post.objects.get(id = post.pk)
    alle_Nutzer_like = post.likes.all()
    # Wenn der Thread ein Like enthält wird dieses entfernt
    if request.user in alle_Nutzer_like:
        post.likes.remove(request.user)
    total_dislikes = message.dislikes.count()
    total_likes = message.likes.count()
    post.votes = total_likes - total_dislikes
    post.save()			 
    return redirect('post-detail', post.pk)
    

def create_comment(request):
    '''Create a comment or reply based on the parent id. Content is cleaned and saved. Checks which user makes the comment or reply.

    Keyword arguments:
    parent_id -- id of comment the reply is made to 
    comment -- content of the comment
    reply -- content of the reply

    '''

    if request.method=="POST":
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        user = request.user
        comment = request.POST.get('comment_content')
        reply = request.POST.get('reply_content')


        cleaned_content_comment = False
        cleaned_content_reply = False


        if comment != None:
            cleaned_content_comment = check_and_censor(comment)
        if reply != None:
            cleaned_content_reply = check_and_censor(reply)

        if cleaned_content_comment == True or cleaned_content_reply == True:
            messages.warning(request, "Your Comment/Reply was not published. The content was too explicit.")
            return redirect('home')
        reply = cleaned_content_reply
        comment = cleaned_content_comment



        parent_id = request.POST.get("parent_id")
        message = 'Du hast eine neue Antwort! :' + str(comment) 
        field_object = Post._meta.get_field('user')
        email = getattr(post,'user')
        post_user_id = getattr(post,'user_id')
        post_user = User.objects.get(id = post_user_id)
        post_user_email = getattr(post_user, 'email')


        if parent_id == None:
            comment_form = Comment(post=post, user=user, comment_content=comment)
            comment_form.save()
            send_email(post_id,'New reply to your Post!', message, post_user_email)
            messages.success(request, "Your comment has been published successfully.")
        else:
            comment_form = Comment(post=post, user=user,  comment_content = reply, parent_id =parent_id)
            comment_form.save()
            send_email(post_id,'New reply to your Comment!', message, post_user_email)
            messages.success(request, "Your reply has been published successfully.")
    else:
        comment_form = Comment()
        messages.success(request, "Your comment could not be published.")

    return redirect(f'post/{post_id}')


def delete_comment(request, comment_id):
    '''Delete a comment or reply by primary key. Checks which user made the comment or reply. Admin can always delete.

    Keyword arguments:
    comment -- comment object
    commentuser_id -- id of original creator
    current_user -- id of logged in user

    '''
    comment = Comment.objects.get(pk=comment_id)
    commentuser_id = getattr(comment, 'user_id')
    post_id = getattr(comment, 'post_id')

    user_obj = User.objects.get(pk=commentuser_id)
    commentuser = getattr(user_obj, 'username')

    current_user = request.user

    if str(commentuser) == str(current_user) or request.user.is_superuser:
        messages.success(request, "Your Comment was successfully deleted.")
        comment.delete()
    else:
        messages.warning(request, "This Comment was published by another user. You can only delete your own!")
    return redirect('post-detail', post_id)


def upvote_comment(request, pk):
    '''Upvote a comment. Creates sum of likes and dislikes and calculates total votes.

    Keyword arguments:
    total_dislikes -- number of all dislikes that belong to the post
    total_likes -- number of all likes that belong to the post

    '''
    comment = get_object_or_404(Comment, id= request.POST.get('comment_id'))
    comment.likes.add(request.user)
    message = Comment.objects.get(id = comment.pk)
    alle_Nutzer_Dislike = comment.dislikes.all()
    if request.user in alle_Nutzer_Dislike:
        comment.dislikes.remove(request.user)
    total_dislikes = message.dislikes.count()
    total_likes = message.likes.count()
    comment.votes = total_likes - total_dislikes
    comment.save()			 
    return redirect('post-detail', pk)


def downvote_comment(request, pk):
    '''Downvote a comment. Creates sum of likes and dislikes and calculates total votes.

    Keyword arguments:
    total_dislikes -- number of all dislikes that belong to the post
    total_likes -- number of all likes that belong to the post

    '''
    comment = get_object_or_404(Comment, id= request.POST.get('comment_id2'))
    comment.dislikes.add(request.user)
    message = Comment.objects.get(id = comment.pk)
    alle_Nutzer_like = comment.likes.all()
    if request.user in alle_Nutzer_like:
        comment.likes.remove(request.user)
    total_dislikes = message.dislikes.count()
    total_likes = message.likes.count()
    comment.votes = total_likes - total_dislikes
    comment.save()			 
    return redirect('post-detail', pk)


def send_email(post_id, subject, message, email):
    '''Send e-mail notification to user.

    '''
    send_mail(subject= subject, message= message, from_email= settings.EMAIL_HOST_USER, recipient_list= ['simplyforumcrew@gmail.com', email], fail_silently= False)
    return redirect(f'post/{post_id}')
