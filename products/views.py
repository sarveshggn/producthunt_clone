from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone

# Create your views here.

def home(request):
    products = Product.objects
    return render(request, 'products/home.html', {'products':products})

@login_required(login_url='/accounts/signup')
def create(request):
    if request.method == 'POST':
        if request.POST['Title'] and request.POST['Body'] and request.POST['URL'] and request.FILES['Icon'] and request.FILES['Image']:
            product = Product()
            product.title = request.POST['Title']
            product.body = request.POST['Body']
            if request.POST['URL'].startswith('http://') or request.POST['URL'].startswith('https://'):
                product.url = request.POST['URL']
            else:
                product.url = 'http://' + request.POST['URL']
            product.icon = request.FILES['Icon']
            product.image = request.FILES['Image']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html')
    else:
        return render(request, 'products/create.html')


def detail(request,product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product':product})

@login_required(login_url='/accounts/signup')
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/' + str(product.id))