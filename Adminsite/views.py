from django.shortcuts import render,redirect
from Website.models import CategoryDB,RegisterDB,CategoryRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Admin_RegDB

# Create your views here.
def category_page(request):
    return render(request,"Add_Category.html")

def save_category(request):
    if request.method =="POST":
        c_name = request.POST.get('cat_name')
        c_img = request.FILES['cat_image']
        obj=CategoryDB(Cat_Name=c_name,Cat_Image=c_img)
        obj.save()
        return redirect(category_page)
def edit_category(request,c_id):
    data = CategoryDB.objects.get(id=c_id)
    return render(request,"Edit_Category.html",{'data':data})

def display_category(request):
    data = CategoryDB.objects.all()
    return render(request,"Display_Category.html",{'data':data})

def display_users(request):
    users = RegisterDB.objects.all()

    return render(request,"Display_User.html",{'users':users})

def display_request(request):
    req = CategoryRequest.objects.all()

    return render(request,"Category_Requests.html",{'req':req})

def update_category(request,c_id):
    if request.method =="POST":
        cn =request.POST.get('cat_name')
        try:
            ima = request.FILES['cat_image']
            fs = FileSystemStorage()
            file = fs.save(ima.name, ima)
        except MultiValueDictKeyError:
            file = CategoryDB.objects.get(id=c_id).Cat_Image
    CategoryDB.objects.filter(id=c_id).update(Cat_Name=cn,Cat_Image=file)
    return redirect(display_category)

def delete_category(req,c_id):
    x=CategoryDB.objects.filter(id=c_id)
    x.delete()
    return redirect(display_category)

def delete_user(request, user_id):
    user = RegisterDB.objects.filter(id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('display_users')

def delete_req(request, user_id):
    x = CategoryRequest.objects.filter(id=user_id)
    x.delete()
    messages.success(request, "Request deleted successfully.")
    return redirect(display_request)

def admin_login_page(request):
    return render(request,"Admin_Login.html")

def admin_login(request):
    if request.method=="POST":
        l_name=request.POST.get('lo_mail')
        l_pwd=request.POST.get('lo_pass')
        user = Admin_RegDB.objects.filter(email=l_name, password=l_pwd).first()
        if user:
            request.session['Username'] = l_name
            request.session['Password'] = l_pwd
            return redirect(category_page)
        else:
            return redirect(admin_login_page)
    else:
        return redirect(admin_login_page)
    

def admin_reg_page(request):
    return render(request,"Admin_Reg.html")
def admin_reg_save(request):
    if request.method =="POST":
        mail=request.POST.get('reg_mail')
        pwd=request.POST.get('reg_pass')
        obj=Admin_RegDB(email=mail,password=pwd)
        obj.save()
        return redirect(admin_reg_page)