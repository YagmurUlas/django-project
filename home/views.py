import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormMessage, ContactForm
from product.models import Product, Category, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:3]
    category = Category.objects.all()
    newimages = Product.objects.all().order_by('?')[:6]
    dayproducts = Product.objects.all().order_by('?')[:6]
    lastproducts = Product.objects.all().order_by('-id')[:3]
    randomproducts = Product.objects.all().order_by('?')[:4]

    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderdata':sliderdata,
               'dayproducts': dayproducts,
               'lastproducts': lastproducts,
               'randomproducts': randomproducts,
               'newimages': newimages
               }
    return render(request, 'index.html', context)


def about(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,
               'category' : category}
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

    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    form = ContactForm()
    context = {'setting': setting,
               'form': form,
               'category': category,}
    return render(request, 'contact.html', context)

def category_products(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id).order_by('-id')
    context = {'products': products,
               'category': category,
               'categorydata': categorydata
               }
    return render(request, 'products.html', context)

def product_detail(request,id,slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id,status='True')
    context = {'product': product,
               'category': category,
               'images': images,
               'comments': comments,
               }
    return render(request,'product_detail.html',context)


def product_search(request):
    if request.method == 'POST': #CHECK FORM POST
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()

            query = form.cleaned_data['query'] #get form data
            catid = form.cleaned_data['catid']  # get form data
            if catid == 0:
                products = Product.objects.filter(title__icontains=query)#select * from product where title like %query%
            else:
                products = Product.objects.filter(title__icontains=query,category_id=catid)
            #return HttpResponse(products)
            context = {'products': products,
                       'category': category,
                       }
            return render(request, 'products_search.html', context)

    return HttpResponseRedirect('/')

def product_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,"Login Hatası! Kullanıcı adı ya da şifre yanlış")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {'category': category,
               }
    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1 ')
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               }
    return render(request, 'signup.html', context)



