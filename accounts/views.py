from django.shortcuts import redirect, render
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from .forms import *
from .models import *
from .filters import *
from .decorators import *

from django.contrib.auth.decorators import login_required
# Create your views here.


@unauthenticated_user
def registerPage(request):
    
    form = CreateUserForm()
    if (request.method == 'POST'):
        form = CreateUserForm(request.POST)
        if (form.is_valid()):
            user = form.save()
            username = form.cleaned_data.get('username')
            
            
            messages.success(request, "Account was created for " + username)

            return redirect('/login')

    return render(request, 'accounts/register.html', {
        'form': form,
    })

@unauthenticated_user
def loginPage(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Username or Password is incorrect")

    return render(request, 'accounts/login.html', {

    })


def logoutUser(request):
    logout(request)

    return redirect('/login')


@login_required(login_url='/login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    return render(request, 'accounts/dashboard.html', {
        "orders": orders,
        "customers": customers,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "delivered": delivered,
        "pending": pending
    })
    
    
@login_required(login_url='/login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    
    orders = request.user.customer.order_set.all()
    
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    
    return render(request, 'accounts/user.html', {
        "orders": orders,
        "total_orders": total_orders,
        "delivered": delivered,
        "pending": pending
    })


@login_required(login_url='/login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
        
    return render(request, 'accounts/account_settings.html', {
        'form': form,
    })


@login_required(login_url='/login')
def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {
        "products": products
    })


@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    orders_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    return render(request, 'accounts/customer.html', {
        "customer": customer,
        "orders": orders,
        "orders_count": orders_count,
        "myFilter": myFilter,
    })


@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    return render(request, 'accounts/customer_form.html', {
        "formset": formset,
    })


@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/order_form.html', {
        "form": form,
    })


@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):

    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('/')

    return render(request, 'accounts/delete.html', {
        "item": order,
    })
