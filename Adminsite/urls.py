from django.urls import path
from Adminsite import views

urlpatterns = [
    path('category_page/',views.category_page,name="category_page"),
    path('save_category/',views.save_category,name="save_category"),
    path('display_category/',views.display_category,name="display_category"),
    path('display_users/',views.display_users,name="display_users"),
    path('display_request/',views.display_request,name="display_request"),
    path('admin_login_page/',views.admin_login_page,name="admin_login_page"),
    path('admin_login/',views.admin_login,name="admin_login"),
    path('admin_reg_page/',views.admin_reg_page,name="admin_reg_page"),
    path('admin_reg_save/',views.admin_reg_save,name="admin_reg_save"),
    path('edit_category/<int:c_id>/',views.edit_category,name="edit_category"),
    path('update_category/<int:c_id>/',views.update_category,name="update_category"),
    path('delete_category/<int:c_id>/',views.delete_category,name="delete_category"),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('delete_req/<int:user_id>/', views.delete_req, name='delete_req'),

]