from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

# Create your views here.
from accounts.decorators import unauthenticated_user, allowed_users, user_analyser
from accounts.filters import OrderFilter
from accounts.forms import OrderForm, CustomerForm, CreateUserForm
from accounts.models import Order, Customer, Product
from django.forms import inlineformset_factory


@login_required(login_url='signin')
# @allowed_users(allowed_roles=['customer', 'admin'])
@user_analyser
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    totalCustomers = customers.count()
    totalOrders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders,
               'customers': customers,
               'totalOrders': totalOrders,
               'totalCustomers': totalCustomers,
               'delivered': delivered,
               'pending': pending
               }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'accounts/products.html', context)


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    ordersCount = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer,
               'orders': orders,
               'ordersCount': ordersCount,
               'myFilter': myFilter}

    return render(request, 'accounts/customer.html', context)


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    orderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formSet = orderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        formSet = orderFormSet(request.POST, instance=customer)
        if formSet.is_valid():
            formSet.save()
            return redirect('customer', pk)
    context = {'formSet': formSet}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('customer', order.customer.pk)
    context = {'form': form}
    return render(request, 'accounts/update_order.html', context)


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('customer', order.customer.pk)
    context = {'order': order}
    return render(request, 'accounts/delete_order.html', context)


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer', pk)
    context = {'form': form}
    return render(request, 'accounts/update_customer.html', context)


@unauthenticated_user
def signUp(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            #user = form.save()
            form.save()
            #group = Group.objects.get(name='customer')
            #user.groups.add(group)
            #Customer.objects.create(
            #    user=user,
            #    name=user.username,
            #    email=user.email
            #)

            return redirect('signin')
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


@unauthenticated_user
def signIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'accounts/signin.html', context)


def signOut(request):
    logout(request)
    return redirect('signin')


@allowed_users(allowed_roles=['customer'])
@login_required(login_url='signin')
def userPage(request):
    orders = request.user.customer.order_set.all()
    totalOrders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders,
               'totalOrders': totalOrders,
               'delivered': delivered,
               'pending': pending}
    return render(request, 'accounts/user.html', context)


def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)