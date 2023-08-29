from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from.models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import ContactMessage
from .forms import ContactForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(Custormer=customer, complete=False)  # Sử dụng tên trường đúng ở đây
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        customer = None
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems= order['get_cart_items']
    products= Product.objects.all()
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    page = request.GET.get('page', 1)

    paginator = Paginator(products, 6)  # Hiển thị 6 sản phẩm trên mỗi trang
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context= {'products': products, 'cartItems': cartItems,'categories': categories,'active_category': active_category}
    return render(request, 'app/home.html',context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(Custormer=customer, complete=False)  # Sử dụng tên trường đúng ở đây
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        customer = None
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems= order['get_cart_items']
    categories = Category.objects.filter(is_sub = False)
    context = {'items': items, 'order': order, 'customer': customer,'cartItems': cartItems,'categories': categories}
    return render(request, 'app/cart.html', context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(Custormer=customer, complete=False)  # Sử dụng tên trường đúng ở đây
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        customer = None
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems= order['get_cart_items']
    context = {'items': items, 'order': order, 'customer': customer, 'cartItems': cartItems}
    return render(request, 'app/checkout.html',context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId'] 
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(Custormer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product= product)
    if action == 'add':
        orderItem.quantity+=1
    elif action=='remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
        
    return JsonResponse('added', safe= False)
def register(request):
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    context={'form': form}
    return render(request,'app/register.html',context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username= username,password= password) 
        if user is not None:
            login(request,user)
            return redirect('home')
        else: messages.info(request,'user or password not correct')
                 
    
    context={}
    return render(request,'app/login.html',context)
def logoutPage(request):
    logout(request)
    return redirect('login')
def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(Custormer=customer, complete=False)  # Sử dụng tên trường đúng ở đây
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        customer = None
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems= order['get_cart_items']
    products= Product.objects.all()
    return render(request,'app/search.html',{"searched":searched,"keys":keys,'products': products, 'cartItems': cartItems})

def category(request):
    categories = Category.objects.filter(is_sub = True)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(Custormer=customer, complete=False)  # Sử dụng tên trường đúng ở đây
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        customer = None
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems= order['get_cart_items']
    context = {'categories': categories,'products': products,'active_category': active_category,'products': products, 'cartItems': cartItems}
    return render(request,'app/category.html',context)
def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(Custormer=customer, complete=False)  # Sử dụng tên trường đúng ở đây
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        customer = None
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems= order['get_cart_items']
    id = request.GET.get('id','')
    product = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub = False)
    context = {'items': items, 'order': order, 'customer': customer,'cartItems': cartItems,'categories': categories,'product': product}
    return render(request, 'app/detail.html', context)
def preview(request):
    return render(request,'app/preview.html')

def contact(request):
    if request.method == "POST":
        cf = ContactForm(request.POST)
        if cf.is_valid():
            cf.save()
            return redirect('contact:contact')  # Redirect to a success page
    else:
        cf = ContactForm()
    return render(request, 'app/contact.html', {'cf': cf})

