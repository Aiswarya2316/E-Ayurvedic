from django.shortcuts import render



def home(request):
    return render(request,'home.html')



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.timezone import now




# Customer Registration
def customer_register(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer registered successfully!")
            return redirect("login")
    else:
        form = CustomerRegistrationForm()
    return render(request, "customer/register.html", {"form": form, "user_type": "Customer"})



# Seller Registration
def staf_register(request):
    if request.method == "POST":
        form = StafRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Seller registered successfully!")
            return redirect("login")
    else:
        form = StafRegistrationForm()
    return render(request, "staf/register.html", {"form": form, "user_type": "Seller"})



# Admin Registration
def admin_register(request):
    if request.method == "POST":
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Admin registered successfully!")
            return redirect("login")
    else:
        form = AdminRegistrationForm()
    return render(request, "admin/register.html", {"form": form, "user_type": "Admin"})



# --- User Login ---
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = None
            redirect_url = "login"  # Default in case of failure

            if Customer.objects.filter(email=email, password=password).exists():
                user = Customer.objects.get(email=email)
                request.session["user_type"] = "Customer"
                redirect_url = "customerhome"
            elif Staf.objects.filter(email=email, password=password).exists():
                user = Staf.objects.get(email=email)
                request.session["user_type"] = "Staf"
                redirect_url = "stafhome"
            elif AdminReg.objects.filter(email=email, password=password).exists():
                user = AdminReg.objects.get(email=email)
                request.session["user_type"] = "Admin"
                redirect_url = "adminhome"

            if user:
                request.session["user_id"] = user.id
                messages.success(request, f"Welcome {user.name}!")
                return redirect(redirect_url)
            else:
                messages.error(request, "Invalid credentials")

    form = LoginForm()
    return render(request, "login.html", {"form": form})



# Logout View
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")




def adminhome(request):
    return render(request,'admin/adminhome.html')



def stafhome(request):
    return render(request,'staf/stafhome.html')



def customerhome(request):
    return render(request,'customer/customerhome.html')



from django.shortcuts import render, redirect
from .models import Department, Doctor
from .forms import DepartmentForm, DoctorForm

def add_department(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')  # Redirect to department list view
    else:
        form = DepartmentForm()
    return render(request, 'staf/add_department.html', {'form': form})

def add_doctor(request):
    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')  # Redirect to doctor list view
    else:
        form = DoctorForm()
    return render(request, 'staf/add_doctor.html', {'form': form})







from django.shortcuts import render, get_object_or_404, redirect
from .models import Department, Doctor
from .forms import DepartmentForm, DoctorForm

def department_list(request):
    """View to list all departments"""
    departments = Department.objects.all()
    return render(request, 'staf/department_list.html', {'departments': departments})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Department, Doctor
from .forms import DepartmentForm, DoctorForm

def doctor_list(request):
    """View to list all doctors with an option to filter by department"""
    department_id = request.GET.get('department_id')  # Get department filter from URL parameters
    if department_id:
        department = get_object_or_404(Department, id=department_id)
        doctors = Doctor.objects.filter(department=department)
    else:
        doctors = Doctor.objects.all()  # Show all doctors if no department is selected
    
    departments = Department.objects.all()  # Get all departments for filtering
    return render(request, 'staf/doctor_list.html', {'doctors': doctors, 'departments': departments})






from django.shortcuts import render
from .models import Department, Doctor

def doctors_by_department(request):
    departments = Department.objects.all()
    selected_department = request.GET.get('department_id')
    
    if selected_department:
        doctors = Doctor.objects.filter(department_id=selected_department, available=True)
    else:
        doctors = Doctor.objects.filter(available=True)

    return render(request, 'customer/doctors_list.html', {'departments': departments, 'doctors': doctors})


def book_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == "POST":
        customer_name = request.POST.get('customer_name')
        customer_contact = request.POST.get('customer_contact')
        appointment_date = request.POST.get('appointment_date', '2025-01-01')  # Default date
        appointment_time = request.POST.get('appointment_time')

        if not appointment_time:
            appointment_time = '09:00'  # Default time if missing

        print(f"Received Data - Name: {customer_name}, Contact: {customer_contact}, Date: {appointment_date}, Time: {appointment_time}")

        if not appointment_date:
            return redirect('doctors_by_department')  # Handle missing date properly

        booking = Booking.objects.create(
            doctor=doctor,
            customer_name=customer_name,
            customer_contact=customer_contact,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status='Pending'
        )

        return redirect('payment', booking_id=booking.id)

    return redirect('doctors_by_department')


import uuid  # Fix: Import uuid
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import Booking, Payment

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def make_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        amount = int(booking.doctor.consultation_fee * 100)  # Convert to paisa

        # Create Razorpay order
        order_data = {
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1",
        }
        razorpay_order = razorpay_client.order.create(order_data)

        # Store order details in the database
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.doctor.consultation_fee,
            razorpay_order_id=razorpay_order['id'],
            transaction_id=str(uuid.uuid4()),
            status='Pending'
        )

        return JsonResponse({
            "order_id": razorpay_order['id'],
            "amount": amount,
            "key": settings.RAZORPAY_KEY_ID  # Ensure this is passed
        })

    # Handle GET requests (return the payment page)
    return render(request, "customer/payment.html", {
        "booking": booking,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })


@csrf_exempt
def razorpay_callback(request):
    if request.method == "POST":
        response_data = request.POST
        order_id = response_data.get('razorpay_order_id')
        payment_id = response_data.get('razorpay_payment_id')
        signature = response_data.get('razorpay_signature')

        payment = get_object_or_404(Payment, razorpay_order_id=order_id)

        try:
            # Verify payment signature
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            # Update payment status
            payment.razorpay_payment_id = payment_id
            payment.status = "Completed"
            payment.save()

            # Update booking status to "Paid"
            payment.booking.status = "Paid"
            payment.booking.save()

            return JsonResponse({"status": "success", "redirect_url": "/booking-history/"})

        except razorpay.errors.SignatureVerificationError:
            payment.status = "Failed"
            payment.save()
            return JsonResponse({"status": "failed"}, status=400)




def booking_history(request):
    customer_contact = request.GET.get("contact")  # Fetch from URL query param
    if customer_contact:
        bookings = Booking.objects.filter(customer_contact=customer_contact)
    else:
        bookings = Booking.objects.all()  # Show all if no filter is applied
    
    return render(request, "customer/booking_history.html", {"bookings": bookings})


def about (request):
    return render(request,'customer/about.html')



def staff_view_bookings(request):
    bookings = Booking.objects.all()  # Get all bookings
    return render(request, 'staf/staf_bookings.html', {'bookings': bookings})




# views.py
from datetime import timedelta
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from functools import wraps
import json
import time



import google.generativeai as genai
from groq import Groq

# Configuration
GEMINI_API_KEY = 'AIzaSyCFsU7s437e1uNS-YjNhkSdiOBsOTgNIv0'
GROQ_API_KEY = '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'

# Configure APIs
genai.configure(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

# class ModelManager:
#     def __init__(self):
#         # Set Groq as the default model
#         self.current_model = "groq"  # Default model set to Groq
#         self.last_error_time = 0
#         self.error_cooldown = 300  # 5 minutes cooldown before retrying failed model

#     def switch_model(self):
#         if self.current_model == "groq":
#             self.current_model = "gemini"
#         else:
#             self.current_model = "groq"
#         self.last_error_time = time.time()

class ModelManager:
    def __init__(self):
        self.current_model = "gemini"
        self.last_error_time = 0
        self.error_cooldown = 500  # 5 minutes cooldown before retrying failed model

    def switch_model(self):
        if self.current_model == "gemini":
            self.current_model = "groq"
        else:
            self.current_model = "gemini"
        self.last_error_time = time.time()

model_manager = ModelManager()

def handle_rate_limits(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # If enough time has passed since last error, try switching back to primary model
            if time.time() - model_manager.last_error_time > model_manager.error_cooldown:
                model_manager.current_model = "gemini"
            
            # Switch model and retry
            model_manager.switch_model()
            return func(*args, **kwargs)
    return wrapper

def review_with_gemini(code):
    model = genai.GenerativeModel(
        # model_name='models/gemini-1.5-pro-latest',
        model_name='models/gemini-1.5-flash',

        system_instruction = """
        You are an Ayurveda assistant that helps users improve their health and well-being through personalized Ayurvedic advice. Based on the user's inputs about their lifestyle, diet, physical condition, and wellness goals, your task is to provide tailored Ayurvedic suggestions. This includes recommending dietary changes, lifestyle adjustments, herbal remedies, daily routines, and self-care practices. Your responses should be grounded in Ayurvedic principles and provide actionable steps that are practical, safe, and aligned with the user's unique constitution (dosha). Always ensure the advice is personalized, holistic, and easy to integrate into the user's daily life.
        """


    )


    
    try:
        response = model.generate_content(code)
        print(f"Gemini response: {response.text}")  # Log the response text for debugging
        return response.text.strip()
    except Exception as e:
        print(f"Error with Gemini API: {str(e)}")  # Log the error from Gemini API
        raise  # Re-raise the exception after logging it

def review_with_groq(code):
    system_prompt = """        You are an Ayurveda assistant that helps users improve their health and well-being through personalized Ayurvedic advice. Based on the user's inputs about their lifestyle, diet, physical condition, and wellness goals, your task is to provide tailored Ayurvedic suggestions. This includes recommending dietary changes, lifestyle adjustments, herbal remedies, daily routines, and self-care practices. Your responses should be grounded in Ayurvedic principles and provide actionable steps that are practical, safe, and aligned with the user's unique constitution (dosha). Always ensure the advice is personalized, holistic, and easy to integrate into the user's daily life.."""
    
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": code}
        ],
        model="llama3-70b-8192",
        temperature=0.7,
        max_tokens=1000
    )
    return chat_completion.choices[0].message.content.strip()







from django.utils import timezone



from django.contrib.auth.decorators import login_required

def review_code_chat(request):
    # if not check_query_limit(request.user):
    #     return JsonResponse({"error": "Monthly query limit reached"}, status=403)

    if request.method == 'GET':
        # Get the current time and subtract 12 hours
        twelve_hours_ago = timezone.now() - timedelta(hours=12)
        
        # Filter PlagiarismChat for the current logged-in customer (request.user is assumed to be a Customer instance)
        chat_history = PlagarismChat.objects.filter(
            customer__id=request.session["user_id"],  # Use session user_id directly
            created_at__gte=twelve_hours_ago
        )
        
        # Render the chat history to the template
        return render(request, 'customer/chat.html', {
            'chat_history': chat_history
        })

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            code_content = data.get('code_content')
            
            if not code_content:
                return JsonResponse({"error": "Please provide some code"}, status=400)

            # Review the code using the appropriate model
            if model_manager.current_model == "gemini":
                review = review_with_gemini(code_content)
            else:
                review = review_with_groq(code_content)

            # Create a chat record
            chat = PlagarismChat.objects.create(
                customer_id=request.session["user_id"],  # ✅ Correct way
                code=code_content,
                review=review,
                model_used=model_manager.current_model,
                review_type='chat'
            )

            suggestion_points = [point.strip() for point in review.split('*') if point]

            # UserQueryCount.increment_query(request.user, 'chat')
            print(suggestion_points)
            return JsonResponse({
                "career_suggestion": suggestion_points
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)



from django.shortcuts import render

def chart(request):
    return render(request, 'chart.html')