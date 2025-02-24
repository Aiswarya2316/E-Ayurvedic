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