from django.db import models

class Customer(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.PositiveBigIntegerField()
    password = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    symptoms = models.ManyToManyField('Symptom', related_name='customers')

    def __str__(self):
        return self.name

class Staf(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    expertise = models.ManyToManyField('Symptom', related_name='staff_experts')

    def __str__(self):
        return self.name

class AdminReg(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.PositiveBigIntegerField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Symptoms Model
class Symptom(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Remedy Model
class Remedy(models.Model):
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    description = models.TextField()
    herbal_medicine = models.TextField()
    dietary_plan = models.TextField()
    yoga_practice = models.TextField()
    lifestyle_adjustment = models.TextField()

    def __str__(self):
        return f"Remedy for {self.symptom.name}"
    
# Treatment Model - Now includes feedback & progress tracking
class Treatment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staf, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    remedy = models.ForeignKey(Remedy, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Ongoing', 'Ongoing'), ('Completed', 'Completed')], 
        default='Pending'
    )
    feedback = models.TextField(blank=True, null=True)  # Customer feedback

    def __str__(self):
        return f"Treatment for {self.customer.name} by {self.staff.name} - {self.status}"
    

# models.py
from django.db import models
from django.contrib.auth.models import User  # Using Django's built-in User model

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Doctor(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='doctors')
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    location = models.CharField(max_length=255, blank=True, null=True)  # New field for location

    def __str__(self):
        return self.name

    
class Booking(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')  # ForeignKey to Customer
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Paid', 'Paid')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.customer.name} - {self.doctor.name} on {self.appointment_date}"


from django.db import models

class Payment(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')],
        default='Pending'
    )

    def __str__(self):
        return f"Payment for {self.booking} - {self.status}"


class PlagarismChat(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Tie the chat to a customer
    code = models.TextField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    model_used = models.CharField(max_length=20)
    review_type = models.CharField(max_length=20)  # 'live', 'chat', or 'file'
    
    def __str__(self):
        return f"Plagiarism Chat by {self.customer.name} on {self.created_at}"