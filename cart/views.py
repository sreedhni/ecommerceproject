from django.http import HttpResponseNotFound,HttpResponseBadRequest
from django.shortcuts import render,redirect
from ecommerceapp.models import Product
from .models import Cart,Order
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm 
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, get_object_or_404
from .models import Review, Product


# Create your views here.
@login_required
def cartview(request):
    total=0
    user=request.user
    try:
       product_detail=Cart.objects.filter(user=user)
       for i in product_detail:
           total+=i.quantity*i.products.price
    except Cart.DoesNotExist:
        pass

    return render(request,"cart.html",{"product_details":product_detail,"total":total})


@login_required
def add_cart(request,p):
    product=Product.objects.get(id=p)

    user=request.user
    try:
        cart=Cart.objects.get(products=product,user=user)
        if cart.quantity < cart.products.stock:
            cart.quantity+=1
            cart.save()
    except Cart.DoesNotExist:
        cart=Cart.objects.create(user=user,products=product,quantity=1)
        cart.save()
    return redirect('cart:cartview')




@login_required
def cart_item_less(request, id):
    selected_item = get_object_or_404(Product, id=id)
    user = request.user
    try:
        cart_item = Cart.objects.get(products=selected_item, user=user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Cart.DoesNotExist:
        pass
    return redirect('cart:cartview')







@login_required
def cart_remove(request, id):
    selected_item = get_object_or_404(Product, id=id)
    user = request.user
    print(selected_item)
    try:
        cart_item = Cart.objects.get(products=selected_item, user=user)
        cart_item.delete()
    except Cart.DoesNotExist:
        pass
    return redirect('cart:cartview')


@login_required
def orderform(request):
    if request.method == "POST":
        a = request.POST.get('a', '')  
        p = request.POST.get('p', '')  
        pay=request.POST.get('pay','')
        if not a or not p or not pay:
            return HttpResponseBadRequest("Shipping address and phone number are required.")

        user = request.user
        cart = Cart.objects.filter(user=user)
        total = 0

        for i in cart:
            total += i.quantity * i.products.price
            o = Order.objects.create(user=user, products=i.products, address=a, phone=p, order_status="Confirmed", mode_of_payment=pay,
                         delivery_status="Pending", no_of_items=i.quantity)
            i.products.stock -= i.quantity
            i.products.save()
            o.save()
            send_order_confirmation_email(user, o)

        cart.delete()
        msg = "Order placed successfully"
        return render(request, "orderdetail.html", {'msg': msg, 'total': total})

    return render(request, "orderform.html")

def send_order_confirmation_email(user, order):
    subject = 'Order Confirmation'
    html_message = render_to_string('order_confirmation_email.html', {'user': user, 'order': order})
    plain_message = strip_tags(html_message)
    from_email = 'your@example.com'  
    to_email = user.email
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)


@login_required
def add_review(request, order_id):
    product = get_object_or_404(Product, id=order_id)    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('ecommerceapp:product_detail', product_id=review.product.id)  
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form})


def product_search(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'product_search.html', {'products': products})

def product_filter(request):
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    products = Product.objects.filter(category=category, price__gte=min_price, price__lte=max_price)
    return render(request, 'product_filter.html', {'products': products})


def display_all_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'all_review.html', {'product': product, 'reviews': reviews})
    