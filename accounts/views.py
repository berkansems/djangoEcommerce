from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from django.contrib import messages
from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage


from accounts.filters import OrderFilter
from accounts.forms import OrderForm, CustomerForm, CreateUserForm
from accounts.models import Customer, Order, Product


def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    totalOrders = orders.count()
    totalCustomers = customers.count()
    pending = orders.filter(status="Pending").count()
    delivered = orders.filter(status="Delivered").count()

    context = {'customers': customers,
               'orders': orders,
               'totalOrders': totalOrders,
               'totalCustomers': totalCustomers,
               'pending': pending,
               'delivered': delivered
               }
    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'accounts/products.html', context)


def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    orderCount = orders.count()
    myFilter = OrderFilter(queryset=orders)
    orders = myFilter.qs
    context = {
        'customer': customer,
        'orderCount': orderCount,
        'orders': orders,
        'myFilter': myFilter
    }
    return render(request, 'accounts/customer.html', context)


def updateCustomer(request, pk):
    customer=Customer.objects.get(id=pk)
    form=CustomerForm(instance=customer)
    if request.method=="POST":
        form=CustomerForm(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer',pk)
    context={'form':form}
    return render(request,'accounts/update_customer.html',context)

def deleteCustomer(request,pk):
    customer=Customer.objects.get(id=pk)

    if request.method=="POST":
        Customer.objects.get(id=pk).order_set.all().delete()
        Customer.objects.get(id=pk).delete()
        return redirect('home')
    context = {'customer': customer}
    return render(request,'accounts/delete_customer.html',context)

def createCustomer(request):
    form= CustomerForm()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'accounts/create_customer.html',context)


def createOrder(request, pk):
    orderFormSet = inlineformset_factory(Customer,Order, fields=('product','status'),extra=5)
    customer = Customer.objects.get(id=pk)
    formSet = orderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method == 'POST':
        formSet = orderFormSet(request.POST, instance=customer)
        if formSet.is_valid():
            formSet.save()
            return redirect('customer',pk)
    context = {'formSet': formSet}
    return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    formSet = OrderForm(instance=order)
    if request.method == "POST":
        formSet= OrderForm(request.POST,instance=order)
        if formSet.is_valid():
            formSet.save()
            return redirect('customer',order.customer.pk)
    context = {'formSet': formSet}
    return render(request, 'accounts/update_order.html', context)

def deleteOrder(request,pk):
    order= Order.objects.get(id=pk)
    if request.method=="POST":
        order.delete()
        return redirect('customer',order.customer.pk)
    context={'order': order}
    return render(request,'accounts/delete_order.html',context)


def signUp(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=user.username
            )
            username = form.cleaned_data.get('username')
            messages.success(request, 'Accounts was created for ' + username)
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)

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




#    orderFormSet = inlineformset_factory( Customer, Order, fields=('product', 'status'), extra=5)
#    customer = Customer.objects.get(id=pk)
#    formSet = orderFormSet(queryset=Order.objects.none(), instance=customer)
#    if request.method == 'POST':
#        formSet = orderFormSet(request.POST, instance=customer)
#        if formSet.is_valid():
#            formSet.save()
#            return redirect('customer', pk)
#    context = {'formSet': formSet}
#    return render(request, 'accounts/order_form.html', context)
