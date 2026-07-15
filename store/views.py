from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Cart, Order, OrderItem, SubCategory, Feedback, ContactFeedback
from .forms import ProductForm, FeedbackForm, ContactFeedbackForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render


@csrf_exempt
def payment_success(request):
    return HttpResponse("Payment Success - OK")

# HOME
def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:8]
    all_products = Product.objects.all()[:8]
    categories = Category.objects.all()

    return render(request, 'home.html', {
        'products': featured_products if featured_products.exists() else all_products,
        'categories': categories
    })


# BROWSE CATEGORIES
def browse_categories(request):
    categories = Category.objects.all()
    return render(request, 'browse_categories.html', {'categories': categories})


def search_products(request):
    query = request.GET.get('q', '').strip()
    products = []

    if query:
        products = Product.objects.filter(
            name__icontains=query
        ) | Product.objects.filter(
            brand__icontains=query
        ) | Product.objects.filter(
            description__icontains=query
        )

    return render(request, 'search.html', {
        'products': products,
        'query': query
    })


# CATEGORY
def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    subcategories = SubCategory.objects.filter(category=category)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {
        'category': category,
        'subcategories': subcategories,
        'products': products
    })


# PRODUCT DETAIL
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    feedbacks = Feedback.objects.filter(product=product).order_by('-created_at')
    
    return render(request, 'product_detail.html', {
        'product': product,
        'feedbacks': feedbacks
    })


# SUBMIT FEEDBACK
@login_required
def submit_feedback(request, pk):
    product = get_object_or_404(Product, id=pk)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.product = product
            feedback.user = request.user
            feedback.save()
            return redirect('product_detail', pk=pk)
    
    return redirect('product_detail', pk=pk)


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

    if not cart_items.exists():
        return redirect('cart')

    total = sum(item.product.price * item.quantity for item in cart_items)

    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    for item in cart_items:

        OrderItem.objects.create(
            order=order,
            product=item.product.name,   # Agar OrderItem me product CharField hai
            price=item.product.price,
            quantity=item.quantity
        )

    cart_items.delete()

    return render(request, "checkout.html", {
        "order": order,
        "total": total,
    })

# ORDERS
@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})


# ORDER ITEMS
@login_required
def order_items(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)

    total = 0
    for item in items:
        item.subtotal = item.price * item.quantity
        total += item.subtotal

    return render(request, "order_items.html", {
        "order": order,
        "items": items,
        "total": total,
    })

# REORDER
@login_required
def reorder(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)
    
    # Add all items from the order to cart
    for item in items:
        # Try to find the original product (since OrderItem stores product as CharField)
        try:
            product = Product.objects.get(name=item.product)
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': item.quantity}
            )
            if not created:
                cart_item.quantity += item.quantity
                cart_item.save()
        except Product.DoesNotExist:
            pass
    
    messages_list = ["Order items added to your cart!", "Ready to checkout!"]
    return render(request, 'order_items.html', {
        'order': order,
        'items': items,
        'success_message': messages_list[0]
    })


# INVOICE
@login_required
def download_invoice(request, order_id):
    from django.http import HttpResponse
    from datetime import datetime
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)
    
    # Generate HTML invoice
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Invoice #{order.id}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .invoice-header {{ text-align: center; margin-bottom: 30px; }}
            .invoice-header h1 {{ color: #333; margin: 0; }}
            .invoice-header p {{ margin: 5px 0; color: #666; }}
            .invoice-details {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }}
            .detail-box {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
            .detail-box h3 {{ margin: 0 0 10px 0; color: #333; }}
            .detail-box p {{ margin: 5px 0; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
            table th {{ background: #333; color: white; padding: 12px; text-align: left; }}
            table td {{ padding: 12px; border-bottom: 1px solid #ddd; }}
            table tbody tr:hover {{ background: #f9f9f9; }}
            .total {{ text-align: right; font-size: 18px; font-weight: bold; margin-top: 20px; }}
            .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 40px; }}
        </style>
    </head>
    <body>
        <div class="invoice-header">
            <h1>📄 Invoice</h1>
            <p>Order #{order.id}</p>
        </div>
        
        <div class="invoice-details">
            <div class="detail-box">
                <h3>Bill To:</h3>
                <p><strong>{order.user.get_full_name() or order.user.username}</strong></p>
                <p>Email: {order.user.email}</p>
            </div>
            <div class="detail-box">
                <h3>Order Information:</h3>
                <p>Order Date: {order.created_at.strftime('%B %d, %Y')}</p>
                <p>Status: <strong>{order.get_status_display()}</strong></p>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Product Name</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
"""
    
    for item in items:
        item_total = item.price * item.quantity
        html_content += f"""
                <tr>
                    <td>{item.product}</td>
                    <td>₹{item.price}</td>
                    <td>{item.quantity}</td>
                    <td>₹{item_total}</td>
                </tr>
"""
    
    html_content += f"""
            </tbody>
        </table>
        
        <div class="total">
            <p>Order Total: <strong>₹{order.total_price}</strong></p>
        </div>
        
        <div class="footer">
            <p>Thank you for your purchase! | PATEL STORE</p>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
    </body>
    </html>
    """
    
    response = HttpResponse(html_content, content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.html"'
    return response


# SUBCATEGORY
def subcategory_products(request, slug):
    subcategory = get_object_or_404(SubCategory, slug=slug)
    products = Product.objects.filter(subcategory=subcategory)
    return render(request, 'subcategory.html', {
        'subcategory': subcategory,
        'category': subcategory.category,
        'products': products
    })


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
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        # Validation
        if not username or not password:
            return render(request, 'register.html', {'error': 'Username and password are required'})
        
        if password != password_confirm:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        
        if len(password) < 6:
            return render(request, 'register.html', {'error': 'Password must be at least 6 characters'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        # Create user
        User.objects.create_user(username=username, password=password)
        return render(request, 'register.html', {'success': 'Account created successfully! Please login.'})

    return render(request, 'register.html')


# LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not User.objects.filter(username=username).exists():
            return render(request, 'login.html', {'error': 'Username does not exist'})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('home')


# CONTACT FEEDBACK
def contact_feedback(request):
    if request.method == 'POST':
        form = ContactFeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'feedback.html', {
                'form': ContactFeedbackForm(),
                'success': 'Thank you! Your feedback has been received. We appreciate your input!'
            })
    else:
        form = ContactFeedbackForm()
    
    return render(request, 'feedback.html', {'form': form})

# ==========================
# PROFILE
# ==========================

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    total_orders = Order.objects.filter(user=request.user).count()
    total_cart_items = Cart.objects.filter(user=request.user).count()

    return render(request, "profile.html", {
        "user": request.user,
        "total_orders": total_orders,
        "total_cart_items": total_cart_items,
    })

def search_products(request):
    query = request.GET.get("q")

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, "search.html", {
        "products": products,
        "query": query,
    })