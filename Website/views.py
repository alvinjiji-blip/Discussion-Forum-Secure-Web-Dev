
from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    RegisterDB, Post, Like, Comment, UserProfile,
    CategoryDB, CategoryRequest
)
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
import os
import json


# Homepage
def front_page(request):
    if 'Username' not in request.session:
        return redirect('user_login_page')

    username = request.session.get('Username')
    user = RegisterDB.objects.filter(username=username).first()

    if not user:
        request.session.flush()
        messages.error(request, "Please sign in again.")
        return redirect('user_login_page')

    items = Post.objects.all().order_by('-created_at')
    data = CategoryDB.objects.all()

    return render(request, "Front.html", {
        'data': data,
        'items': items,
        'user': user
    })


# Category request
def save_request(request):
    if request.method == "POST":
        if 'Username' not in request.session:
            return redirect('user_login_page')

        username = request.session.get('Username')
        user = RegisterDB.objects.filter(username=username).first()

        if not user:
            return redirect('user_login_page')

        cnm = request.POST.get('category_name', '').strip()
        cim = request.FILES.get('category_image')

        if not cnm:
            messages.error(request, "Please enter a category name.")
            return redirect('front_page')

        CategoryRequest.objects.create(
            user=user,
            name=cnm,
            image=cim
        )

        messages.success(request, "Category request submitted successfully.")
        return redirect('front_page')

    return redirect('front_page')


# Login page
def user_login_page(request):
    if 'Username' in request.session:
        username = request.session.get('Username')

        if RegisterDB.objects.filter(username=username).exists():
            return redirect('front_page')

        request.session.flush()

    return render(request, "User_Loginpage.html")


# Login
def login(request):
    if request.method != "POST":
        return redirect('user_login_page')

    l_name = request.POST.get('lo_name', '').strip()
    l_pwd = request.POST.get('lo_pass', '')

    if not l_name or not l_pwd:
        messages.error(request, "Please enter both username and password.")
        return redirect('user_login_page')

    user = RegisterDB.objects.filter(
        username=l_name,
        password=l_pwd
    ).first()

    if user:
        request.session.flush()
        request.session['Username'] = user.username
        return redirect('front_page')

    messages.error(request, "Invalid username or password. Please try again.")
    return redirect('user_login_page')


# Registration page
def reg_page(request):
    return render(request, "User_Registrationpage.html")


# Save registration
def reg_save(request):
    if request.method == "POST":

        f_name = request.POST.get('reg_name', '').strip()
        u_name = request.POST.get('reg_uname', '').strip()
        mob = request.POST.get('reg_mob', '').strip()
        mail = request.POST.get('reg_mail', '').strip()
        pwd = request.POST.get('reg_pass', '')
        profile_photo = request.FILES.get('reg_profile_image')

        # Check required fields
        if not f_name or not u_name or not mail or not pwd:
            messages.error(request, "Please fill in all required fields.")
            return redirect('reg_page')

        # Check duplicate username
        if RegisterDB.objects.filter(username=u_name).exists():
            messages.error(request, "Username already exists. Please choose another.")
            return redirect('reg_page')

        # Check duplicate email
        if RegisterDB.objects.filter(email__iexact=mail).exists():
            messages.error(request, "Email already used. Please use another email.")
            return redirect('reg_page')

        # Save new user with profile photo
        obj = RegisterDB(
            full_name=f_name,
            username=u_name,
            email=mail,
            phone=mob,
            password=pwd,
            profile_image=profile_photo
        )

        obj.save()

        messages.success(request, "Registration successful. Please sign in.")
        return redirect('user_login_page')

    return redirect('reg_page')


# Logged-in user's profile
def profile_page(request):
    if 'Username' not in request.session:
        return redirect('user_login_page')

    username = request.session.get('Username')
    user = RegisterDB.objects.filter(username=username).first()

    if not user:
        request.session.flush()
        return redirect('user_login_page')

    user_profile, created = UserProfile.objects.get_or_create(user=user)
    categories = CategoryDB.objects.all()

    if request.method == 'POST':
        bio = request.POST.get('bio')
        place = request.POST.get('place')
        gender = request.POST.get('gender')

        user_profile.bio = bio
        user_profile.place = place
        user_profile.gender = gender
        user_profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile_page')

    posts = Post.objects.filter(user=user).order_by('-created_at')
    friends = RegisterDB.objects.exclude(username=username)

    return render(request, "Profile_Page.html", {
        'user': user,
        'user_profile': user_profile,
        'posts': posts,
        'friends': friends,
        'categories': categories,
    })


# Upload profile picture
def upload_profile(request):
    if request.method == "POST" and request.FILES.get('profile_image'):
        username = request.session.get('Username')
        user = RegisterDB.objects.filter(username=username).first()

        if not user:
            return JsonResponse({'error': 'User not found'}, status=400)

        if user.profile_image:
            old_image_path = os.path.join(
                settings.MEDIA_ROOT,
                str(user.profile_image)
            )

            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        user.profile_image = request.FILES['profile_image']
        user.save()

        return JsonResponse({
            'profile_image_url': user.profile_image.url
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


# Upload cover photo
def upload_cover(request):
    if request.method == "POST" and request.FILES.get('cover_photo'):
        username = request.session.get('Username')
        user = RegisterDB.objects.filter(username=username).first()

        if not user:
            return JsonResponse({'error': 'User not found'}, status=400)

        if user.cover_photo:
            old_cover_path = os.path.join(
                settings.MEDIA_ROOT,
                str(user.cover_photo)
            )

            if os.path.exists(old_cover_path):
                os.remove(old_cover_path)

        user.cover_photo = request.FILES['cover_photo']
        user.save()

        return JsonResponse({
            'cover_photo_url': user.cover_photo.url
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


# Create post
def create_post(request):
    if request.method == "POST":
        user = RegisterDB.objects.filter(
            username=request.session.get('Username')
        ).first()

        if not user:
            return redirect('user_login_page')

        category_id = request.POST.get("category")
        caption = request.POST.get('caption')
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        if not caption and not image and not video:
            messages.error(request, "Post cannot be empty.")
            return redirect('profile_page')

        category = get_object_or_404(CategoryDB, id=category_id)

        Post.objects.create(
            user=user,
            caption=caption,
            image=image,
            video=video,
            category=category
        )

        return redirect('profile_page')

    return JsonResponse({"error": "Invalid request"}, status=400)


# Like or unlike post
def like_post(request, post_id):
    if 'Username' not in request.session:
        return JsonResponse({'error': 'Please login first.'}, status=401)

    post = get_object_or_404(Post, id=post_id)

    user = RegisterDB.objects.filter(
        username=request.session.get('Username')
    ).first()

    if not user:
        return JsonResponse({'error': 'User not found.'}, status=400)

    like, created = Like.objects.get_or_create(
        post=post,
        user=user
    )

    if not created:
        like.delete()

    return JsonResponse({
        'like_count': post.like_set.count()
    })


# Add comment
def add_comment(request, post_id):
    if request.method == "POST":
        if 'Username' not in request.session:
            return JsonResponse({'error': 'Please login first.'}, status=401)

        post = get_object_or_404(Post, id=post_id)

        user = RegisterDB.objects.filter(
            username=request.session.get('Username')
        ).first()

        if not user:
            return JsonResponse({'error': 'User not found.'}, status=400)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid data.'}, status=400)

        comment_text = data.get('comment', '').strip()

        if not comment_text:
            return JsonResponse({'error': 'Comment cannot be empty.'}, status=400)

        Comment.objects.create(
            post=post,
            user=user,
            text=comment_text
        )

        return JsonResponse({
            'comment_user': user.full_name,
            'comment_text': comment_text
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


# View another user's profile
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


# Logout
def logout(request):
    if request.method == "POST":
        request.session.flush()

    return redirect('user_login_page')


# Category page
def category_page(request, c_id):
    if 'Username' not in request.session:
        return redirect('user_login_page')

    username = request.session.get('Username')
    user = RegisterDB.objects.filter(username=username).first()

    if not user:
        request.session.flush()
        return redirect('user_login_page')

    category = get_object_or_404(CategoryDB, id=c_id)

    posts = Post.objects.filter(
        category=category
    ).select_related('user').order_by('-created_at')

    return render(request, "Category.html", {
        'data': category,
        'posts': posts,
        'user': user
    })
