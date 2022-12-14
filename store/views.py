# from tkinter import E
from django.shortcuts import get_object_or_404, redirect, render


from .models import Product,Account
from category.models import Category
from django.contrib import messages

from carts.views import _cart_id
# from django.http import HttpResponse
from carts.models import CartItem
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.http import HttpResponse
from django.db.models import Q
from .forms import ReviewForm,ReviewRating


# Create your views here.
def store(request,category_slug=None):
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=categories,is_available=True)
        paginator =Paginator(products, 1)
        page= request.GET.get('page')
        paged_products =paginator.get_page(page)
        product_count = products.count()
    else:
        
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator =Paginator(products, 6)
        page= request.GET.get('page')
        paged_products =paginator.get_page(page)
        product_count = products.count() 
    
    context = {
        'products': paged_products,
        'product_count':product_count,
    }    
    
    return render(request,'store/store.html',context)
    
    
def product_detail(request,category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart =CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        #wishlist = Whishlist.objects.filter(Q(product=Product)& Q(user=request.user))
        # return HttpResponse(in_cart )
    except Exception as e:
        raise e
    context = {
        'single_product':single_product,
        'in_cart'       :in_cart,
    }
    return render(request, 'store/product_detail.html',context)    


#search
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products =Product.objects.order_by( 'created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword) )
            product_count = products.count()
            
        context = {
            'products' : products,
            'product_count' :product_count,
    }     
    return render(request,'store/store.html',context)    
def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request,'Thank you! Your review has been updated.')
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,"Thank you! Your review has been submitted.")
                return redirect(url)
