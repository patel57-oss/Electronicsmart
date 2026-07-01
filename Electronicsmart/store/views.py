from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Cart, Order, OrderItem
from .forms import ProductForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


@csrf_exempt
def payment_success(request):
    return HttpResponse("Payment Success - OK")

# HOME
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    return render(request, 'home.html', {
        'products': products,
        'categories': categories
    })


# CATEGORY
def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {
        'category': category,
        'products': products
    })


# PRODUCT DETAIL
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'product_detail.html', {'product': product})


# ADD TO CART
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


# CART
@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# REMOVE CART ITEM
@login_required
def remove_from_cart(request, pk):
    item = Cart.objects.get(id=pk, user=request.user)
    item.delete()
    return redirect('cart')


# 🔥 CHECKOUT (THIS FIXES YOUR ERROR)
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items:
        return redirect('home')

    total = sum(item.product.price * item.quantity for item in cart_items)

    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product.name,
            price=item.product.price,
            quantity=item.quantity
        )

    cart_items.delete()

    return render(request, 'checkout.html', {'order': order})


# ORDERS
@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})


# ADD PRODUCT
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


# REGISTER
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'register.html')


# LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('home')