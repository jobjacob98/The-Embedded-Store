from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Count, Sum
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .forms import UserSignupForm, ContactForm, UserUpdateForm, AccountUpdateForm
from .models import Cart
from store.models import Product

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Account created successfully!!")
            return redirect('login')
    else:
        form = UserSignupForm()
    return render(request, 'users/signup.html', { 'title': 'Sign Up', 'form': form })

def login(request):
    if request.user.is_authenticated:
        return redirect('store-home')
    else:
        return auth_views.LoginView.as_view(template_name='users/login.html')(request)

def logout(request):
    if request.user.is_authenticated:
        return auth_views.LogoutView.as_view(template_name='users/logout.html')(request)
    else:
        return redirect('store-home')

def contact_us(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                subject = form.cleaned_data['subject']
                from_email = request.user.email
                message = form.cleaned_data['message']
                message = "From: " + from_email + "\n" + message
                try:
                    send_mail(subject, message, from_email, ['']) # fill the list with your email id
                except BadHeaderError:
                    messages.success(request, f"Couldn't sent message. Invalid header found.")
                    return render(request, "users/contact-us.html", { 'title': 'Contact Us', 'form': form })
                return redirect('contact_success')
    return render(request, "users/contact-us.html", { 'title': 'Contact Us', 'form': form })

def contact_success(request):
    return render(request, 'users/contact-success.html', { 'title': 'Message Sent Successfully' })

@login_required
def account(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        a_form = AccountUpdateForm(request.POST, instance=request.user.account)
        if u_form.is_valid() and a_form.is_valid():
            u_form.save()
            a_form.save()
            messages.success(request, f"Account updated successfully!!")
            return redirect('my-account')
    else:
        u_form = UserUpdateForm(instance=request.user)
        a_form = AccountUpdateForm(instance=request.user.account)
    return render(request, 'users/my-account.html', { 'title': 'My Account', 'u_form': u_form, 'a_form': a_form })

@login_required
def cart(request):
    cart_count = Cart.objects.filter(cart_id=request.user).count()
    if cart_count == 0:
        return render(request, 'users/my-cart.html', { 'title': 'My Cart', 'cart_count': cart_count })
    else:
        cart = Cart.objects.filter(cart_id=request.user)
        cart_products = cart.values('product_id').annotate(pcount=Count('product_id'))
        cart_price = cart.aggregate(Sum('product_price'))
        if request.method == "GET":
            product_id = request.GET.get('add')
            if product_id != None:
                cart = Cart.objects.filter(cart_id=request.user)
                cart.filter(product_id=product_id).delete()
                return redirect('my-cart')
    return render(request, 'users/my-cart.html', { 'title': 'My Cart', 'cart_count': cart_count, 'cart_products': cart_products, 'products': Product.objects.all(), 'cart_price': cart_price['product_price__sum'] })
