from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from .models import Category, Product
from users.models import Cart

def home(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            cart_id = request.user
            product_id = request.GET.get('add')
            if product_id != None:
                product = Product.objects.filter(product_name=product_id)
                product_price = product.values('price')
                price = product_price[0]['price']
                Cart.objects.create(cart_id=cart_id, product_id=product_id, product_price=price)
                return redirect('store-home')
        cart_count = Cart.objects.filter(cart_id=request.user).count()
        return render(request, 'store/index.html', { 'products': Product.objects.all(), 'cart_count': cart_count })
    else:
        return auth_views.LoginView.as_view(template_name='store/index.html')(request)

def about(request):
    return render(request, 'store/about.html', { 'title': 'About' })
