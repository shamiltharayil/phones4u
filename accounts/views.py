
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts import forms
from accounts.forms import RegistrationForm,UserForm,UserProfileForm
from carts.models import Cart, CartItem
from .models import Account, UserProfile
from django.contrib import messages ,auth
from django.contrib.auth.decorators import login_required
# from orders.models import Order
#mail verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from carts.views import _cart_id
from carts.models import Cart
from store.models import Product
from orders.models import Order, OrderProduct
# Create your views here.
def register(request):
    if request.method == 'POST': 
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            #Create User Profile
            profile = UserProfile()
            profile.user_id=user.id
            profile.profile_picture='default-user.png'
            profile.save()
            
            #user activation
            
            current_site = get_current_site(request)
            mail_subject = 'please activate your accoungt'
            message = render_to_string('accounts/account_verification_email.html', {
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            }) 
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send() 
            # messages.success(request,'Rgistration succesful.')
            return redirect('/accounts/login/?command=verification&email='+email)
            
            
    else:    
        form = RegistrationForm()
    context = {
            'form': form,
        }
    return render(request, 'accounts/register.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email,password=password)
        
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists() 
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    for item in cart_item:
                        item.user = user
                        item.save()
            except: 
                print('entering inside except block')   
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('home')
        else:
            messages.error(request,'invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url= 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are logged out.')
    return redirect('login')
    

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')
@login_required(login_url='login')    
def dashboard(request):
    # orders = Order.objects.order_by('_created_at').filter(user_id=request.user.id, is_ordered=True)
    # orders_count =orders.count()
    # context = {
    #     'orders_count':orders_count
    # }
    return render(request,'accounts/dashboard.html') 


def forgotpassword(request):
    if request.method == 'POST':
        email =request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
        
        
            #reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            }) 
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send() 
            
            messages.success(request,'password reset email has been send to your email address')
            return redirect('login')
        else:
            messages.error(request,'Account doesnt exist')
            return redirect('forgotpassword')
    return render(request, 'accounts/forgotpassword.html')

def resetpassword_validate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request,'please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request,'this link is expired')
        return redirect('login')
    
    
def resetpassword(request):
    if request.method == 'POST':
        password =request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)     
            user.save()
            messages.success(request,'password reset succesful')
            return redirect('login')       
        else:
            messages.error(request,'password do not match')
            return redirect('resetpassword')
    else:   
        return render(request,'accounts/resetpassword.html')  

@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)
    
    

@login_required(login_url='login')
def change_password(request):
    
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)
        
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                #auth.logout(request)
                messages.success(request,'password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request,'please enter valid password')
                return redirect('change_password')
        else:
                messages.error(request,'password does not match!')
                return redirect('change_password')
        
    return render(request,'accounts/change_password.html')
#Wishlist
def wishlist(request):
    products = Product.objects.filter(user_wishlist=request.user)
    context = {
        'products': products
    }
    return render(request,'accounts/wishlist.html',context)

#Wishlist - add to wishlist
login_required(login_url='signin')
def add_to_wishlist(request,id):
    product = get_object_or_404(Product,id=id)
    if product.user_wishlist.filter(id=request.user.id).exists():
        messages.error(request,"Product already in wishlist")
    else:
        product.user_wishlist.add(request.user)
        messages.success(request,"Successfully added to wishlist")
    return redirect('wishlist')

#Wishlist - delete from wishlist
def delete_wishlist(request,id):
    product = get_object_or_404(Product,id=id)
    product.user_wishlist.remove(request.user)
    messages.success(request,"Removed from wishlist")
    return redirect('wishlist')

@login_required(login_url="usersignin")
def my_orders(request):
    orderproducts = OrderProduct.objects.filter(
        user=request.user,ordered=True).order_by("-created_at")
    orders = Order.objects.filter(
        user=request.user,is_ordered=True).order_by("-created_at")

    context = {"orders": orders,"orderproducts":orderproducts}
    return render(request, "accounts/my_orders.html", context)


@login_required(login_url='usersignin')
def userdashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/userdashboard.html', context)