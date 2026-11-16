from django.shortcuts import render, redirect,get_object_or_404
from .models import RegisterDB,Post,Like,Comment,UserProfile,CategoryDB,CategoryRequest
from django.http import JsonResponse
from django.conf import settings
import os
from django.contrib import messages
import json
from django.contrib.auth.decorators import login_required


# Create your views here.
def front_page(request):
    if 'Username' not in request.session:
        return redirect('user_login_page')  # Redirect to login if not logged in

    username = request.session.get('Username')
    user = RegisterDB.objects.filter(username=username).first()
    items = Post.objects.all()
    data = CategoryDB.objects.all()
    return render(request,"Front.html",{'data':data,'items':items,'user':user})

def save_request(request):
    if request.method == "POST":
        if 'Username' not in request.session:
            return redirect('user_login_page')  # Redirect if user is not logged in

        username = request.session.get('Username')
        user = RegisterDB.objects.filter(username=username).first()

        if not user:
            return redirect('user_login_page')  # Ensure user exists

        cnm = request.POST.get('category_name')
        cim = request.FILES.get('category_image')  # Use request.FILES for image uploads

        obj = CategoryRequest(user=user, name=cnm, image=cim)  # Assign user
        obj.save()

        return redirect(front_page)


def user_login_page(request):
    return render(request,"User_Loginpage.html")

def login(request):
    if request.method=="POST":
        l_name=request.POST.get('lo_name')
        l_pwd=request.POST.get('lo_pass')
        user = RegisterDB.objects.filter(username=l_name, password=l_pwd).first()
        if user:
            request.session['Username'] = l_name
            request.session['Password'] = l_pwd
            return redirect(front_page)
        else:
            return redirect(user_login_page)
    else:
        return redirect(user_login_page)

def reg_page(request):
    return render(request,"User_Registrationpage.html")
def reg_save(request):
    if request.method =="POST":
        f_name=request.POST.get('reg_name')
        u_name=request.POST.get('reg_uname')
        mob=request.POST.get('reg_mob')
        mail=request.POST.get('reg_mail')
        pwd=request.POST.get('reg_pass')
        obj=RegisterDB(full_name=f_name,username=u_name,email=mail,phone=mob,password=pwd)
        obj.save()
        return redirect(user_login_page)
def profile_page(request):
    if 'Username' not in request.session:
        return redirect('user_login_page')  # Redirect to login if not logged in

    username = request.session.get('Username')
    user = RegisterDB.objects.filter(username=username).first()
    categories = CategoryDB.objects.all()

    if not user:
        messages.error(request, "User not found.")
        return redirect('user_login_page')

    # Fetch or create user profile
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        bio = request.POST.get('bio')
        place = request.POST.get('place')
        gender = request.POST.get('gender')

        # Update user profile
        user_profile.bio = bio
        user_profile.place = place
        user_profile.gender = gender
        user_profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile_page')

    posts = Post.objects.filter(user=user).order_by('-created_at')

    # Get all users except the logged-in user
    friends = RegisterDB.objects.exclude(username=username)

    return render(request, "Profile_Page.html", {
        'user': user,
        'user_profile': user_profile,
        'posts': posts,
        'friends': friends,  # Passing the users list to template
        'categories': categories,
    })





def upload_profile(request):
    if request.method == "POST" and request.FILES.get('profile_image'):
        username = request.session.get('Username')
        user = RegisterDB.objects.filter(username=username).first()

        if user:
            # Delete old profile image if it exists
            if user.profile_image:
                old_image_path = os.path.join(settings.MEDIA_ROOT, str(user.profile_image))
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            # Save new image
            user.profile_image = request.FILES['profile_image']
            user.save()

            return JsonResponse({'profile_image_url': user.profile_image.url})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def upload_cover(request):
    if request.method == "POST" and request.FILES.get('cover_photo'):
        username = request.session.get('Username')
        user = RegisterDB.objects.filter(username=username).first()

        if user:
            # Delete old cover photo if it exists
            if user.cover_photo:
                old_cover_path = os.path.join(settings.MEDIA_ROOT, str(user.cover_photo))
                if os.path.exists(old_cover_path):
                    os.remove(old_cover_path)

            # Save new cover photo
            user.cover_photo = request.FILES['cover_photo']
            user.save()

            return JsonResponse({'cover_photo_url': user.cover_photo.url})

    return JsonResponse({'error': 'Invalid request'}, status=400)





def create_post(request):
    if request.method == "POST":
        user = RegisterDB.objects.filter(username=request.session.get('Username')).first()
        category = request.POST.get("category")
        print(category)
        cat=CategoryDB.objects.get(id=category)
        caption = request.POST.get('caption')
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        if not user:
            return JsonResponse({"error": "User not found"}, status=400)

        if not caption and not image and not video:
            return JsonResponse({"error": "Post cannot be empty"}, status=400)

        post = Post.objects.create(user=user, caption=caption, image=image, video=video,category=cat)
        post.save()
        return redirect('profile_page')

    return JsonResponse({"error": "Invalid request"}, status=400)




def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # post = Post.objects.get(id=post_id)
    user = RegisterDB.objects.filter(username=request.session.get('Username')).first()

    like, created = Like.objects.get_or_create(post=post, user=user)
    if not created:
        like.delete()

    return JsonResponse({'like_count': post.like_set.count()})

def add_comment(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        user = RegisterDB.objects.filter(username=request.session.get('Username')).first()

        data = json.loads(request.body)
        comment_text = data.get('comment')

        print("comment",comment_text)
        comment = Comment.objects.create(post=post, user=user, text=comment_text)
        comment.save()

        return JsonResponse({'comment_user': user.full_name, 'comment_text': comment_text})

def user_profile(request, username):
    user = RegisterDB.objects.filter(username=username).first()

    if not user:
        messages.error(request, "User not found.")
        return redirect('profile_page')

    user_profile, created = UserProfile.objects.get_or_create(user=user)
    posts = Post.objects.filter(user=user).order_by('-created_at')

    return render(request, "User_Profile.html", {
        'user': user,
        'user_profile': user_profile,
        'posts': posts
    })

def logout(request):
    if request.method=="POST":
        request.session.flush()
    return redirect(user_login_page)

def category_page(request, c_id):
    if 'Username' not in request.session:
        return redirect('user_login_page')  # Redirect to login if not logged in

    username = request.session.get('Username')
    user = RegisterDB.objects.filter(username=username).first()
    category = CategoryDB.objects.get(id=c_id)
    posts = Post.objects.filter(category=category).select_related('user')
    return render(request, "Category.html", {'data': category, 'posts': posts,'user':user})




