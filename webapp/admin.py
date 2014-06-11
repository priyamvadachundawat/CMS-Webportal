from django.contrib import admin

from webapp.models import Comment, Contributor, Reviewer, Class, Subject
from webapp.models import Contact, Faq

admin.site.register(Contributor)
admin.site.register(Comment)
admin.site.register(Reviewer)
admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(Contact)
admin.site.register(Faq)



