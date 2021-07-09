from django.db import models
from django.db.models.signals import post_save , pre_save
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

#from django.contrib.auth import get_user_model
# Create your models here.

#User = get_user_model() #used for forgien key

class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False) #recommend to use your own user



class Task(models.Model):
    task_name=models.CharField(max_length=20)
    task_descrption=models.TextField()
    agent = models.ForeignKey("Agent",null=True,blank=True, on_delete=models.SET_NULL)
    done=models.BooleanField(default=False)
    def __str__(self):
        return self.task_name




class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
         
   
class Lead(models.Model):
    SOURCE_CHOICES = (
         ('Crucial','Crucial'),
         ('Not Crucial', 'Not Crucial'),
         ('Normal', 'Normal'),
     )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(default=0)
    organisation = models.ForeignKey(UserProfile,default=2,on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent",null=True,blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category",related_name="leads", null=True,blank=True, on_delete=models.SET_NULL)
    #related name in views instead of doing the reverse lockup leads_set.all we can say leads.all
    description =models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)
    phone_number=models.CharField(max_length=20)
    email=models.EmailField()
    location=models.CharField(max_length=20)
    Lead_status = models.CharField(choices=SOURCE_CHOICES, max_length=100)
    spendings = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

    # phoned = models.BooleanField(default=False)
    # source = models.CharField(choices=SOURCE_CHOICES, max_length=100)

    # profile_picture = models.ImageField(blank=True,null=True)
    # special_files = models.FileField()

class Agent(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    salary = models.IntegerField(default=0)
    position = models.CharField(max_length=20)
    Task = models.ForeignKey("Task",null=True,related_name="Agent",blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name}"

class Category(models.Model):
    name = models.CharField(max_length=30) #New , Contacted , Converted , Un converted 
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.name
    

 

# class Customer(models.Model):
#     First_name = models.CharField(max_length=50)
#     Last_name = models.CharField(max_length=50)
#     City = models.CharField( max_length=50)
#     State = models.CharField( max_length=50)
#     email = models.EmailField(_(""), max_length=254)
#     LoyaltyScore = int



def post_user_created_signal(sender , instance, created,**kwargs):
    print(instance , created)
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User )