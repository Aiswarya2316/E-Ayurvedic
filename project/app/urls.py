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
    path('add-department/', views.add_department, name='add_department'),
    path('add-doctor/', views.add_doctor, name='add_doctor'),
    path('departments/', views.department_list, name='department_list'),
    path('doctors/', views.doctor_list, name='doctor_list'), 
    path('doctorss/', views.doctors_by_department, name='doctors_by_department'),
    path('book-doctor/<int:doctor_id>/', views.book_doctor, name='book_doctor'),
    path('payment/<int:booking_id>/', views.make_payment, name='payment'),
    path('razorpay-callback/', views.razorpay_callback, name='razorpay_callback'),
    path("booking-history/", views.booking_history, name="booking_history"),
    path("about/", views.about, name="about"),
    path('stafbookings/', views.staff_view_bookings, name='staff-bookings'),
    path('chat-review/', views.review_code_chat, name='chat_review'),

]
