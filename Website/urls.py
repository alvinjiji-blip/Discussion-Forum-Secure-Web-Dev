from django.urls import path
from Website import views

urlpatterns = [


    path('front_page/', views.front_page, name="front_page"),
    path('', views.user_login_page, name="user_login_page"),
    path('reg_page/', views.reg_page, name="reg_page"),
    path('profile_page/', views.profile_page, name="profile_page"),
    path('upload_profile/', views.upload_profile, name='upload_profile'),
    path('upload_cover/', views.upload_cover, name='upload_cover'),
    path('create_post/', views.create_post, name='create_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('login/', views.login, name='login'),
    path('reg_save/', views.reg_save, name='reg_save'),
    path('user_profile/<str:username>/', views.user_profile, name='user_profile'),
    path('logout/', views.logout, name='logout'),
    path('save_request/', views.save_request, name='save_request'),
    path('category_page/<int:c_id>/', views.category_page, name='category_page'),

]
