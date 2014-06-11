from django.shortcuts import HttpResponse, render_to_response
from django.template import RequestContext
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth import authenticate , login, logout
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, mail_admins
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


from webapp.models import Contributor, Reviewer, Subject

from webapp.forms import ContributorForm , UserForm, ContributorUploadForm


def index(request):
	return render_to_response("webapp/index.html")


def userlogin(request):
    """Login form.
    
    Arguments:
    - `request`:
    """
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user1 = authenticate(username=username, password=password)

        if user1 is not None:
            # Is the account active? It could have been disabled.
            if user1.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
		u=User.objects.get(username=user1.username)
		if Contributor.objects.filter(user=u):		
			login(request,user1)
			return HttpResponseRedirect('/cprofile')
            	else:
			login(request,user1)
			return HttpResponseRedirect('/rprofile')
	    else:
                # An inactive account was used - no logging in!
                messages.info(request, "Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            messages.error(request, "Bad login!")
            return render_to_response('webapp/login.html', context)
    else:
        return render_to_response('webapp/login.html', context)



def user_logout(request):
	context=RequestContext(request)
	logout(request)
	return HttpResponseRedirect('/')
      


def upload(request):
        context = RequestContext(request)

    # Download APK and increment the count
    #if request.GET:
        #subject = get_object_or_404(Subject, id=request.GET['id'])
        # increment download count
        #project.increment_download_count()
        #return HttpResponseRedirect('/media/%s' % project.apk)
	
    ## **	uploads = Subject.objects.filter(contributor=request.user)
        uploads = Subject.objects.filter(contributor__user__username=request.user)
	context_dict = {'uploads': uploads}
    	return render_to_response('upload.html', context_dict, context)

def review(request,id):
	context = RequestContext(request)
	#comments = Comment.objects.all()
	rev = Reviewer.objects.filter(user_id=id)
	uploads = Subject.objects.filter(approve=False).filter(name=rev.specialised_subject)
	print hi
	#context_dict = { 'uploads' :uploads, 'comments' : comments}
	context_dict={ 'uploads' : uploads}
	return render_to_response("review.html",context_dict,context)

def home(request):
	context = RequestContext(request)
	return render_to_response('panda/home.html',context)

def contributor_signup(request):

	"""Request for new contributor to signup"""
	context = RequestContext(request)
	registered = False
	if request.method == 'POST':
	        print "we have a request to register"    
		user_form = UserForm(data=request.POST)
	        contributor_form = ContributorForm(data=request.POST)
	        if user_form.is_valid() and contributor_form.is_valid():
			user = user_form.save()
                	print "Forms are Valid"
            		print user.username
            		print user.first_name
            		user.set_password(user.password)
           		user.save()

                        contributor = contributor_form.save(commit=False)
			contributor.user = user

                        if 'picture' in request.FILES:
                		contributor.picture = request.FILES['picture']
			if 'validation_docs' in request.FILES:
	                	contributor.validation_docs=request.FILES['validation_docs']
                      	contributor.save()                       
			registered = True
                        email_subject="New Contributor has registered"
	                email_message="""
New Contributor has registered.
	    	
Details:
Name:""" + user.first_name + """  """ + user.last_name + """"
Email:""" + user.email + """
Waiting for your your approval"""
	#		send_mail(email_subject, email_message, 'khushbu.ag23@gmail.com', ['pri.chundawat@gmail.com'],fail_silently=False)
			messages.success(request,"form successfully submitted. Waiting for activation  from admin.")
			return HttpResponseRedirect(reverse('webapp.views.index'))
	        else:
			if contributor_form.errors or user_form.errors:
				print user_form.errors, contributor_form.errors
	else:
		contributor_form = ContributorForm()
		user_form = UserForm()	
           
        context_dict = {'user_form':user_form, 'contributor_form': contributor_form, 'registered': registered}
        return render_to_response('webapp/signup.html', context_dict, context)



		
def commentpost(request):
	return render_to_response('templates/comments/post.html')


def contributor_upload(request):
	"""Request for new upload by the contributor"""
	context = RequestContext(request)
	uploaded= False
	if request.method == 'POST':
	        print "we have a request for upload by the contributor"    
	        contributor_upload_form = ContributorUploadForm(request.POST,request.FILES)
		if contributor_upload_form.is_valid():	
			print "Forms are valid"
			subject=contributor_upload_form.save(commit=False)
			# contri=Contributor.objects.get(user_id=id)
      			contri = Contributor.objects.get(user=request.user)
			subject.contributor=contri
			subject.name=contri.specialised_subject
			if 'pdf' in request.FILES:
                		subject.pdf=request.FILES['pdf']
			if 'video' in request.FILES:
                		subject.video = request.FILES['video']
			if 'animation' in request.FILES:
                		subject.animation = request.FILES['animation']
			                     
                        subject.save()
			uploaded = True
			return HttpResponseRedirect(reverse('webapp.views.contributor_profile'))
	        else:
			if contributor_upload_form.errors:
				print contributor_upload_form.errors
	else:
		contributor_upload_form = ContributorUploadForm()	
           
        context_dict = {'contributor_upload_form': contributor_upload_form, 'uploaded':uploaded}
        return render_to_response("webapp/upload.html", context_dict, context)


@login_required
def contributor_profile(request):
	context = RequestContext(request)
        uploads = Subject.objects.filter(contributor__user__username=request.user)
	context_dict = {'uploads': uploads}
    	return render_to_response('contributor.html', context_dict, context)


@login_required
def reviewer_profile(request):
	context = RequestContext(request)
	rev = Reviewer.objects.filter(user=request.user)
	uploads = Subject.objects.all()
	context_dict={ 'uploads' : uploads}
	return render_to_response("reviewer.html",context_dict,context)
