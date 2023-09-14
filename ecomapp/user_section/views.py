from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from admin_section.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import json
from .forms import RegistrationForm
from user_section.models import Customer
from django.views.decorators.csrf import csrf_exempt


categories = Category.objects.all()
cart_items = OrderDetail.objects.all()


def home(request):
    return render(request, 'user_section/home.html', {'categories': categories, 'products': products})


def category_products(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category)
    return render(request, 'user_section/category_products.html', {'category': category, 'products': products, 'categories': categories})


def products(request):
    all_products = Product.objects.all()
    products_per_page = 12
    paginator = Paginator(all_products, products_per_page)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    return render(request, 'user_section/products.html', {'products': products, 'categories': categories})


def search_products(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name_en__icontains=query)
    return render(request, 'user_section/search_results.html', {'query': query, 'products': products, 'categories': categories})


def product_detail(request, product_id):
    print("Product ID views:", product_id)
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'user_section/product_detail.html', {'product': product, 'categories': categories})


def cart(request):
    cart_subtotal = 0
    shipping_fee = 40
    total_price = 0
    cart_items = []
    print(request.user)

    if request.user.is_authenticated:
        print("auth? ", request.user)
        customer = Customer.objects.get(user=request.user)
        print("customer retrieved? ", customer)
        order = Order.objects.filter(
            customer=customer, status='Pending').first()
        print("any order? ", order)

        if order:
            cart_items = OrderDetail.objects.filter(order=order)
            cart_subtotal = sum(
                item.unit_price * item.ordered_count for item in cart_items)

    total_price = cart_subtotal + shipping_fee

    context = {
        'cart_items': cart_items,
        'categories': categories,
        'cart_subtotal': cart_subtotal,
        'shipping_fee': shipping_fee,
        'total_price': total_price,
    }
    return render(request, 'user_section/cart.html', context)


@csrf_exempt
@login_required
def place_order(request):
    if request.method == 'POST':
        # print("User id ", request.user.id)
        # print("User id again ", request.user)
        # print("request body ", request.body)
        cart_data = json.loads(request.body)
        customer = Customer.objects.get(id=request.user.id)

        total_price = 0

        order = Order.objects.create(
            customer=customer,
            total_price=total_price,
            status='Pending'
        )
        print(f"Cart data: {cart_data} ")
        for item in cart_data.get('cart_products'):
            product_id = item.get('product_id')
            quantity = item.get('quantity')

            product = Product.objects.get(id=product_id)
            unit_price = product.unit_price
            total_price += unit_price * quantity

        order.total_price = total_price
        order.save()
        return redirect('home')

    return render(request, 'user_section/cart.html')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the homepage after login
    else:
        form = AuthenticationForm()
    return render(request, 'user_section/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            customer = Customer(user=user)
            customer.save()

            # Redirect to the homepage after registration
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'user_section/registration.html', {'form': form})
