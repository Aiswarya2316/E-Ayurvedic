from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('stafhome',views.stafhome,name='stafhome'),
    path('customerhome',views.customerhome,name='customerhome'),
    path("registercustomer/", views.customer_register, name="customer_register"),
    path("registerstaf/", views.staf_register, name="seller_register"),
    path("registeradmin/", views.admin_register, name="admin_register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:department_id>/doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:doctor_id>/book/', views.book_doctor, name='book_doctor'),
    path('booking/success/', views.booking_success, name='booking_success'),


]
