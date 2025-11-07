from django.db import models

class registration(models.Model):
    username=models.CharField(max_length=50,null=True,blank=True)
    business=models.CharField(max_length=50,null=True,blank=True)
    email=models.EmailField(unique=True,null=True,blank=True)
    password=models.CharField(max_length=10,null=True,blank=True)
    profilepic=models.ImageField(upload_to='profilepic/',null=True,blank=True)
    phone=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.username

class founderregisration(models.Model):
    username=models.CharField(max_length=50,null=True,blank=True)
    business=models.CharField(max_length=50,null=True,blank=True)
    email=models.EmailField(unique=True,null=True,blank=True)
    password=models.CharField(max_length=10,null=True,blank=True)
    profilepic=models.ImageField(upload_to='profilepic/',null=True,blank=True)
    phone=models.IntegerField(null=True,blank=True)
    bio = models.TextField(null=True, blank=True)  # Assuming you added this

    def __str__(self):
        return self.username

class investorregistration(models.Model):
    username = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=10, null=True, blank=True)
    profilepic = models.ImageField(upload_to='profilepic/', null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)  # Assuming you added this
    interested_sectors = models.TextField(null=True, blank=True)  # Assuming you added this
    
    def __str__(self):
        return self.username if self.username else "Unknown User"
    

from django.utils.timezone import now   
class ChatMessage(models.Model):
    sender = models.CharField(max_length=100)  # Artist or Buyer username
    receiver = models.CharField(max_length=100)  # Receiver's username
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)
    media=models.FileField(upload_to='chat_media/',null=True,blank=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"
    
class Startup(models.Model):
    user=models.ForeignKey(founderregisration,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='startups/logos/')
    bio = models.TextField()
    description = models.TextField()
    stockprice=models.IntegerField(blank=True,null=True)
    totalstock=models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.name
    from django.db import models
from django.contrib.auth.models import User


class Investment(models.Model):
    user = models.ForeignKey('investorregistration', on_delete=models.CASCADE)  # Linking to the custom investorregistration model
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)  # Linking to the Startup model
    num_stocks = models.IntegerField()  # Number of stocks purchased
    total_investment = models.DecimalField(max_digits=10, decimal_places=2)  # Total amount invested
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE)  # Linking the payment made for this investment
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.num_stocks} stocks in {self.startup.name} by {self.user}"
 

   
class Payment(models.Model):
    investor = models.ForeignKey('investorregistration', on_delete=models.CASCADE)
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255)
    razorpay_order_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # The total amount paid
    status = models.CharField(max_length=50, choices=[('success', 'Success'), ('failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.investor.username} for {self.startup.name}"

class Paymen(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Completed', 'Completed'), ('Pending', 'Pending')])
    

    def __str__(self):
        return f"Payment of {self.amount_received} for {self.investment.startup.name}"


class Paymentmodel(models.Model):
    email=models.EmailField()
    investment = models.CharField(max_length=255)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Completed', 'Completed'), ('Pending', 'Pending')])