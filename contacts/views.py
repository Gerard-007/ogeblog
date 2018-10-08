# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect, Http404
from .forms import contactForm
from django.conf import settings
from django.core.mail import send_mail


#Create your views here.

def contact(request):
    title = 'Send us a message'
    contact_form = contactForm(request.POST or None)
    confirm_message = None

    if contact_form.is_valid():
        comment = contact_form.cleaned_data['comment']
        name = contact_form.cleaned_data['name']
        phone = contact_form.cleaned_data['phone']
        subject = 'Contact email recieved from musicadence.com'
        message = 'name: {} \n message: {} \n mobile: {}'.format(name, comment, phone)
        from_email = contact_form.cleaned_data['email']
        recipient_list = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
        title = 'Thanks'
        confirm_message = 'Dear {} your message was sent sucessfully'.format(name)
        contact_form = None

    context = {'title': title, 'contact_form': contact_form, 'confirm_message': confirm_message}
    template = 'contact.html'
    return render(request, template, context)


# def contact(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         message = request.POST.get("message")
#
#         # Email ourselves the submitted contact message
#         subject = 'Message from musicadence.com'
#         emailFrom = settings.DEFAULT_FROM_EMAIL
#         emailTo = [settings.DEFAULT_FROM_EMAIL]
#
#         # Option 1
#         # contact_message = "{0}, from {1} with email {2}".format(comment, name, email)
#
#         # Option 2
#         context = {
#             'user': name,
#             'email': email,
#             'message': message
#         }
#
#         contact_message = get_template('contact_message.txt').render(context)
#
#         send_mail(
#                     subject,
#                     contact_message,
#                     emailFrom,
#                     emailTo,
#                     fail_silently=False
#                 )
#
#         return redirect("/contact")
#     return render(request, "contact.html", {})
