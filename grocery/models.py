from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    image = models.FileField(null=True)
    name = models.CharField(max_length=100, null=True)
    price = models.IntegerField(null=True)
    desc = models.TextField(null=True)
    qty = models.IntegerField(default=1,null=True)

    def __str__(self):
        return self.category.name+"--"+self.name

class Status(models.Model):
    name = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dob = models.DateField(null=True)
    city = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=50, null=True)
    contact = models.CharField(max_length=10, null=True)
    image = models.FileField(null=True)
    forget_password_token=models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    verified=models.CharField(max_length=100,null=True,default="False")

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    quantity = models.CharField(max_length=100, default="1", null=True)
    total = models.IntegerField(null=True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.profile.user.username + " . " + self.product.name


from .constants import PaymentStatus
class Booking(models.Model):
    #status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    booking_id = models.CharField(max_length=200,null=True)
    quantity = models.CharField(max_length=100,null=True)
    book_date = models.CharField(max_length=30, null=True)
    total = models.IntegerField(null=True)
    status = models.CharField(("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(("Order ID"), max_length=40, null=True, blank=True
    )
    payment_id = models.CharField(("Payment ID"), max_length=36,null=True, blank=True
    )
    signature_id = models.CharField(("Signature ID"), max_length=128, null=True, blank=True
    )


   # def __str__(self):
     #   return self.book_date+" "+self.profile.user.username


class Send_Feedback(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    message1 = models.TextField(null=True)
    date = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.profile.user.username


class Blogpost(models.Model):
    posttitle = models.CharField(max_length=500)
    postdetail = models.TextField()
    postimage = models.FileField()
    postdate = models.DateField()
    def __str__(self):
        return self.posttitle

