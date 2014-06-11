from django.db import models
from django.contrib.auth.models import User


class Contributor(models.Model):
  
    user = models.OneToOneField(User)

    # Addition info
    contact = models.CharField(max_length=12, blank=True)
    picture = models.ImageField(upload_to='profile_image', blank=True)
    specialised_subject = models.CharField(max_length=20, blank=False)
    validation_docs = models.FileField(upload_to='validation_docs',blank=False)
  
    def __unicode__(self):
        return self.user.username

class Reviewer(models.Model):
  
    user = models.OneToOneField(User)

    # Addition info
    contact = models.CharField(max_length=12, blank=True)
    picture = models.ImageField(upload_to='profile_image', blank=True)
    specialised_subject = models.CharField(max_length=20, blank=False)
    
    def __unicode__(self):
        return self.user.username



class Class(models.Model):
    """This will be class number like first, second .. eight .. tenth."""
    class_number = models.IntegerField(default=1)
    remark = models.TextField()

    def __unicode__(self):
        return u"%d" % (self.class_number)


class Subject(models.Model):
    """Subjects."""
    contributor = models.ForeignKey(Contributor)
    name = models.CharField(max_length=50)
    topic = models.CharField(max_length=200)
    class_number = models.ForeignKey(Class)
    pdf = models.FileField(upload_to='pdf', blank=True)
    video = models.FileField(upload_to='video', blank=True)
    animation = models.FileField(upload_to='animation', blank=True)
    pdf_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    animation_url = models.URLField(blank=True)
    uploaded_on = models.DateField(auto_now=True)
    summary = models.TextField(blank=False)
    rating = models.IntegerField(default=0)
    review = models.IntegerField(default=0) 

    def __unicode__(self):
        return u"%s : %s" % (self.name, self.topic)

    def increment_review(self):
        self.review += 1
        self.save()



class Contact(models.Model):
    """Contact us."""
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=False)
    message = models.TextField(max_length=500)


    def __unicode__(self):
        return u"%s - %s" % (self.name, self.email)


class Faq(models.Model):
    """FAQs"""
    question = models.TextField(max_length=500)
    answer = models.TextField() 


    def __unicode__(self):
        return self.question

class Comment(models.Model):

	subject=models.ForeignKey(Subject)
	user = models.ForeignKey(Reviewer)
	comment = models.TextField(max_length = 1000)
	submit_date = models.DateTimeField(auto_now=True)

	def __unicode__(self):
        	return self.comment

