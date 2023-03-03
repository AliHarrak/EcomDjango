from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, logout, login
import datetime
from django.views.generic import ListView, DetailView

from .forms import ProductFilter, UserRegisterForm
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login as myLogin


def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	filter = ProductFilter(request.GET, queryset=products)
	products = filter.qs
	context = {'products':products, 'cartItems':cartItems,'filter':filter}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == float(order.get_cart_total):
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)


def register(request):

    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            messages.success(request,f'Le compte de {username} à été bien crée')
            form.save()
            return redirect('store')
    else:
        form=UserRegisterForm()
    return render(request,'store/register.html',{'form':form})	


def userLogin(request):
    if request.method == 'POST':
  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, f' welcome {username} !!')
            myLogin(request, user)
            
            return redirect('store')
        else:
                messages.success(request, 'Credentials error')    

              

        

    return render(request,'store/login.html')




def userLogout(request):
	logout(request)
	return redirect('login')




def product_list(request):
	
	filter=ProductFilter(request.GET, queryset=Product.objects.all())
	return render(request, 'store/main.html', {'filter':filter})




class ProductDetailView(DetailView):
    model=Product  