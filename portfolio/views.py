from django.shortcuts import render, redirect, get_object_or_404, render
from django.contrib import messages
from .models import Author, Category, Work, Service, Testimony, Item, Message
from django.core.mail import send_mail
from django.conf import settings


def index(request):
    categories = Category.objects.all()
    works = Work.objects.all()
    services = Service.objects.all()
    testimonies = Testimony.objects.all()

    context = {
       'categories': categories,
       'works': works,
       'services': services,
       'testimonies': testimonies,
   }

    return render(request, 'index.html', context)

def about(request):
    author = Author.objects.get()
    return render(request, 'about.html', {'author': author})


def work_detail(request, slug):
    work = get_object_or_404(Work, slug=slug)
    testimonies = Testimony.objects.all()
    context = {
        'work': work,
        'testimonies': testimonies,
    }
    return render(request, 'work_detail.html', context)


def contact(request):
    if request.method == 'POST':
        msg = Message(
            name=request.POST['name'],  
            email=request.POST['email'],
            subject=request.POST['subject'],  
            message=request.POST['message']
         )
        msg.save()
        messages.success(request, 'Сообщение отправлено!')
        return redirect('contact') 
  
    return render(request, 'contact.html')



def contact_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        # Send email
        send_mail(
            subject,
            f'Имя: {name}\nEmail: {email}\nСообщение: {message}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],  # Replace with your email
            fail_silently=False,
        )
        return render(request, 'contact.html', {'message_sent': True})  # Adjust template name

    return render(request, 'contact.html')  # Adjust template name
