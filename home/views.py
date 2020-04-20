from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactFormMessage, ContactForm
from product.models import Product, Category


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:3]
    category = Category.objects.all()

    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderdata':sliderdata}
    return render(request, 'index.html', context)


def about(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'about.html', context)


def references(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'references.html', context)


def contact(request):

    if request.method == 'POST': #form post edilirse
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage() #model ile baglanti kur
            data.name = form.cleaned_data['name'] #formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.save()
            messages.success(request,"Mesajınız başarı ile iletilmiştir.Teşekkür ederiz.")
            return HttpResponseRedirect('/contact')


    setting = Setting.objects.get(pk=1)
    form = ContactForm()
    context = {'setting': setting,'form': form}
    return render(request, 'contact.html', context)

def category_products(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)
    context = {'products': products,
               'category': category,
               'categorydata': categorydata
               }
    return render(request, 'products.html', context)