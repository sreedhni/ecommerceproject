from django.shortcuts import render,redirect,get_object_or_404
from ecommerceapp.models import Contact,Product,Category
from django.contrib import messages
from math import ceil
from ecommerceapp.forms import EditproductForm,ProductForm
from django.contrib.auth.decorators import login_required
from users.models import User
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from cart.models import Order

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}  
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) * (n // 4))  
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, "index.html", params)

def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        desc=request.POST.get("desc")
        pnumber=request.POST.get("pnumber")
        myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        messages.info(request, "we will get back to you soon..")
        return render(request, "contact.html")
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")



def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category')
        if category_name:
            Category.objects.create(category=category_name)
            return redirect('ecommerceapp:category_list')  
    return render(request, 'add_category.html') 
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def add_product(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to add a product.')
        return redirect("ecommerceapp:index")
    if not request.user.is_seller:
        messages.warning(request, 'Permission denied.')
        return redirect("ecommerceapp:index")
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.created_by = request.user
            product.save()
            messages.info(request, 'New product has been added.')
            return redirect('ecommerceapp:manage-orders')
        else:
            messages.warning(request, 'Something went wrong with the form submission.')
            context = {'form': form}
            return render(request, 'add_product.html', context)
    else:
        form = ProductForm()
        context = {'form': form}
        return render(request, 'add_product.html', context)

def edit_product(request, pk):
    item = get_object_or_404(Product, pk=pk)
    if item.created_by != request.user:
        messages.warning(request, 'Permission denied.')
        return redirect("/")
    if request.method == 'POST':
        form = EditproductForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.info(request, 'Product has been updated successfully.')
            return redirect('ecommerceapp:product_detail', product_id=item.id)
        else:
            messages.warning(request, 'Something went wrong. Please check the form.')
    else:
        form = EditproductForm(instance=item)
    return render(request, 'edit_pro.html', {
        'form': form,
        'title': 'Edit item',
    })

def manage_orders(request):
    orders=Product.objects.filter(created_by=request.user)
    context={"orders":orders}
    return render(request, 'manage_orders.html',context)







def change_applicant_status(request, order_id, new_status):
    try:
        order = Order.objects.get(pk=order_id)
        order.delivery_status= new_status
        order.save()
        return redirect('ecommerceapp:manage-orders')
    except Order.DoesNotExist:
        return HttpResponseNotFound('<h1>order not found</h1>')






def product_detail(request, product_id):
    product = get_object_or_404(Product,pk=product_id)
    return render(request, 'product_detail.html', {'product': product})




def all_customers(request, pk):
    try:
        products = Product.objects.get(pk=pk)
        orders = products.order_set.all()
        context = {'products': products, 'orders': orders}
        return render(request, 'all_orders.html', context)
    except Product.DoesNotExist:
        return HttpResponseNotFound('<h1>Produt not found </h1>')






from django.shortcuts import render
from django.db.models import Q
from .models import Product, Category

def product_list(request):
    all_prods = []
    query = request.GET.get('q')
    category_filter = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products_with_categories = Product.objects.select_related('category').all()

    if query:
        products_with_categories = products_with_categories.filter(
            Q(product_name__icontains=query) | Q(description__icontains=query)
        )

    if category_filter:
        products_with_categories = products_with_categories.filter(category__category=category_filter)

    if min_price:
        products_with_categories = products_with_categories.filter(price__gte=min_price)

    if max_price:
        products_with_categories = products_with_categories.filter(price__lte=max_price)

    for product in products_with_categories:
        category_name = product.category.category  
        found = False
        for category, prods in all_prods:
            if category == category_name:
                prods.append(product)
                found = True
                break
        if not found:
            all_prods.append((category_name, [product]))

    categories = Category.objects.all()  

    return render(request, "product_list.html", {
        'all_prods': all_prods,
        'categories': categories,
        'selected_category': category_filter,
        'search_query': query,
        'min_price': min_price,
        'max_price': max_price
    })

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('ecommerceapp:index')  # Redirect to product list after deletion
    template_name = 'product_confirm_delete.html'  # Template for confirmation page

def orders_pro(request):
    if request.user.is_authenticated and request.user.is_customer:
        orderd_products = Order.objects.filter(user=request.user)
        context = {'orderd_products': orderd_products}
        return render(request, 'order.html', context)
    else:
        return render(request, 'unauthorized.html')
