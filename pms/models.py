from django.db import models
from django.contrib.auth.models import User
from .storage import OverwriteStorage
from django.utils import timezone
import random, string
import os
from django.urls import reverse
from django.template.defaultfilters import slugify

def content_file_name(instance, filename):
    name =''.join(random.choice(string.ascii_letters + string.digits) for x in range(3))
    name2 =''.join(random.choice(string.ascii_letters + string.digits) for x in range(3))
    ext = filename.split('.')[-1]
    filename = "img{}{}{}.{}".format(name, instance.user.id, name2, ext)
    return os.path.join('images/{}'.format(instance), filename)

class Supervisor(models.Model):
    choice_sex = {("M","Male"), ("F","Female")}
    choice = {("android","Android"), ("hardware","Hardware"), ("networking","Networking"), ("web", "Web"),
                    ("artificial intelligence","Artificial Intelligence"), ("robotics", "Robotics"),
                    ("iot","Iot"), ("machine learning", "Machine Learning"), ("security", "Security")
                    }
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supervisors')
    surname = models.CharField(max_length=20)
    phone_no = models.CharField(max_length=11, blank=True)
    image = models.ImageField(storage=OverwriteStorage(), upload_to=content_file_name, blank=True)
    capacity = models.PositiveIntegerField(blank=True)
    allowed = models.PositiveIntegerField(blank=True)
    created = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=20) 
    AOC1 = models.CharField(max_length=50, choices=choice)
    AOC2 = models.CharField(max_length=50, choices=choice)

    def __str__(self):
        return self.surname
    
    def get_absolute_url(self):
        return reverse('pms:super_detail', args=[self.slug])

    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/static/images/bgp.png"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.surname)
        super(Supervisor, self).save(*args, **kwargs)
    
class Student(models.Model):
    choice_sex = {("M","Male"), ("F","Female")}
    choice_option = {
                    ("Computer Engineering","Computer Engineering"),
                    ("Computer Science with Mathematics","Computer Science with Mathematics"),
                    ("Computer Science with Economics","Computer Science with Economics")
                    }
    choice = {("android","Android"), ("hardware","Hardware"), ("networking","Networking"), ("web", "Web"),
                    ("artificial intelligence","Artificial Intelligence"), ("robotics", "Robotics"),
                    ("iot","Iot"), ("machine learning", "Machine Learning"), ("security", "Security")
                    }
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='students')
    surname = models.CharField(max_length=20)
    phone_no = models.CharField(max_length=11)
    image = models.ImageField(storage=OverwriteStorage(), upload_to=content_file_name, blank=True)
    option = models.CharField(max_length=40, choices=choice_option)
    gender = models.CharField(max_length=30, choices=choice_sex)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.PROTECT, blank=True, null=True, related_name="sup")
    created = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=20) 
    matricNo = models.CharField(max_length=20)
    supervisor_1 = models.ForeignKey(Supervisor, on_delete=models.PROTECT, blank=True, null=True, related_name="sup_1")
    supervisor_2 = models.ForeignKey(Supervisor, on_delete=models.PROTECT, blank=True, null=True, related_name="sup_2")
    AOC1 = models.CharField(max_length=50, blank=True, choices=choice)
    AOC2 = models.CharField(max_length=50, blank=True, choices=choice)

    def __str__(self):
        return self.slug

    def setSupervisor(self, name):
        self.supervisor = name
        self.save()
    
    def get_absolute_url(self):
        return reverse('pms:student_detail', args=[self.slug])
    
    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/static/images/bgp.png"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        self.matricNo = slugify(self.user)
        super(Student, self).save(*args, **kwargs)
    
class SupervisorPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supervisor_prefer')
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name="sup_student")
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.student)

class EligibleStudent(models.Model):
    matricNo = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
            return self.matricNo

class Test(models.Model):
    choice_sex = {("M","Male"), ("F","Female")}
    choice_option = {("Computer Engineering","Computer Engineering"),
                    ("Computer Science with Mathematics","Computer Science with Mathematics"),
                    ("Computer Science with Economics","Computer Science with Economics")
                    }
    choice = {("android","Android"), ("hardware","Hardware"), ("networking","Networking"), ("web", "Web"),
                    ("artificial intelligence","Artificial Intelligence"), ("robotics", "Robotics"),
                    ("iot","Iot"), ("machine learning", "Machine Learning"), ("security", "Security")
                    }
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='studentss')
    surname = models.CharField(max_length=20)
    phone_no = models.CharField(max_length=11)
    image = models.ImageField(storage=OverwriteStorage(), upload_to=content_file_name, blank=True)
    option = models.CharField(max_length=40, choices=choice_option)
    gender = models.CharField(max_length=30, choices=choice_sex)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.PROTECT, blank=True, null=True, related_name="supa")
    created = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=20) 
    matricNo = models.CharField(max_length=20)
    supervisor_1 = models.ForeignKey(Supervisor, on_delete=models.PROTECT, blank=True, null=True, related_name="supa_1")
    supervisor_2 = models.ForeignKey(Supervisor, on_delete=models.PROTECT, blank=True, null=True, related_name="supa_2")
    AOC1 = models.CharField(max_length=50, blank=True, choices=choice)
    AOC2 = models.CharField(max_length=50, blank=True, choices=choice)

    def __str__(self):
        return self.surname

    def save(self, *args, **kwargs):
        self.slug = slugify(self.surname)
        self.matricNo = slugify(self.user)
        super(Test, self).save(*args, **kwargs)

class Test2(models.Model):
    user = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test_1')
    created = models.DateTimeField(default=timezone.now)