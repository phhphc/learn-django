from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
from .forms import *
# Create your views here.


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


def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {
        "products": products
    })


def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    orders_count = orders.count()

    return render(request, 'accounts/customer.html', {
        "customer": customer,
        "orders": orders,
        "orders_count": orders_count,
    })


def create_order(request):

    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/order_form.html', {
        "form": form,
    })


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


def delete_order(request, pk):

    order = Order.objects.get(id=pk)
    
    if request.method == "POST":
        order.delete()
        return redirect('/')
    
    return render(request, 'accounts/delete.html', {
        "item": order,
    })
