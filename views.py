from django.shortcuts import render, redirect
from ecom_app.form import CustomUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from .models import *
import json

# Create your views here.

def home(request):
  products = Product.objects.filter(trending = 1)
  return render(request, "shop/index.html", {'products': products})

def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request, 'logged out successfully')
  return redirect('/')


def addtocart(request):
  if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    if request.user.is_authenticated:
      data = json.load(request)
      
      product_qty = data['product_qty']
      product_id =  data['pid']
      print(data['pid'])

      product_status = Product.objects.get( id = product_id )
      if product_status:
        if Cart.objects.filter(user = request.user.id, product_id = product_id):
          return JsonResponse({'status': 'Product already in cart'}, status = 200)
        else:
          if product_status.quantity >= product_qty:
            Cart.objects.create(user = request.user, product_id = product_id, product_qty = product_qty)
            return JsonResponse({'status': 'Product Added to cart'}, status = 200)
          else:
            return JsonResponse({'status': 'Product stock not available'}, status = 200)
      
    else:
      return JsonResponse({'status': 'Login to add cart'}, status = 200)
  else:
    return JsonResponse({'status': 'Invalid Access'}, status = 200)

def fav(request):
  if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    if request.user.is_authenticated:
      data = json.load(request)
      print(data['pid'])
      
      product_status = Product.objects.get( id = product_id )

      if product_status:
        if Favourite.objects.filter(user = request.user.id, product_id = product_id):
          return JsonResponse({'status': 'Product already in Favourite'}, status = 200)
        else:
          Favourite.objects.create(user = request.user, product_id = product_id)
          return JsonResponse({'status': 'Added to favourite '}, status = 200)
      
    else:
      return JsonResponse({'status': 'Login to add favourite '}, status = 200)
  else:
    return JsonResponse({'status': 'Invalid Access'}, status = 200)

def login_(request):
  if request.user.is_authenticated:
    return redirect('/')
  else:
    if request.method == 'POST':
      name = request.POST.get('username')
      pwd_ = request.POST.get('password')
      user = authenticate(request, username = name, password = pwd_)

      if user is not None:
        login(request, user)
        messages.success(request, 'logged in successfully...')
        return redirect('/')

      else:
        messages.error(request, 'invalid user name or password')
        return redirect('/login')

    return render(request, 'shop/login.html')

def remove(request, cid, pqt):
  if request.user.is_authenticated:
    cart = Cart.objects.get(id = cid)
    
    print(cart)

    cart.delete()
    return redirect('/cart')

def remove_f(request, fid):
  if request.user.is_authenticated:
    fa = Favourite.objects.get(id = fid)
    fa.delete()
    return redirect('/fav_page')


def cart(request):
  if request.user.is_authenticated:
    cart = Cart.objects.filter(user = request.user)
    return render(request, 'shop/cart.html', {'cart': cart})
  else:
    return redirect('/')

def confirm(request):

  if request.user.is_authenticated:
    cart = Cart.objects.filter(user = request.user)
    return render(request, 'shop/confirm.html', {'cart': cart})
  else:
    return redirect('/')

def changes(request):
  pass
  


def fav_page(request):
  if request.user.is_authenticated:
    fav = Favourite.objects.filter(user = request.user)
    return render(request, 'shop/fav.html', {'fav': fav})
  else:
    return redirect('/')
'''
def register(request): 
  form = CustomUserForm()
  if request.method == 'POST':
    form = CustomUserForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Registration successfully')
      return redirect('/login')
    else:
      messages.warning(request, 'Registration not done')
  return render(request, "shop/register.html", {'form': form})'''

def collections(request):
  cat_list = Catagory.objects.filter(status = 0)
  return render(request, "shop/collections.html", {'cat_list': cat_list})
            
def collections_view(request, name):
  if (Catagory.objects.filter( name = name, status = 0)):
    products = Product.objects.filter(category__name = name)
    return render(request, 'shop/products/index.html', {'products': products, 'category_name': name})

  else:
    messages.warning(request, 'no its initial problem..')
    return redirect('collections')

def product_details(request, cat_name, pro_name):
  if (Catagory.objects.filter(name = cat_name, status = 0)):
    if (Product.objects.filter(name = pro_name, status = 0)):
      products = Product.objects.filter(name = pro_name, status = 0).first()
      return render(request, 'shop/products/product_details.html', {'products': products})
    else:
      messages.error(request, 'no product')
      return redirect('collections')
  else:
    messages.error(request, 'no category')
    return redirect('collections')

def register(request):

  if request.method == 'POST':

    name = request.POST['username']
    email = request.POST['email']
    password1 = request.POST['password1']
    password2 = request.POST['password2']

    if name.isalpha():
      if len(name) > 3:
        '''
        if User.objects.filter(username = name).exists():
          messages.error(request, "user_name already exists...")
        elif User.objects.filter(email = email).exists():
          messages.error(request, "e-mail already exists...")'''
        if password1 == password2:
          if len(password1) >= 8:
            pass_chck = {}
            character = []
            for i in password1:
              if i not in pass_chck:
                if i.islower():   pass_chck[i] = 'L' # lowercase
                elif i.isupper(): pass_chck[i] = 'U' # uppercase
                elif i.isdigit(): pass_chck[i] = 'N' # numeric_digits
                else:             pass_chck[i] = 'S' # special_characters
                
            for idx in pass_chck:
              character.append(pass_chck[idx])
            CHECKED = '-'.join(sorted(list(set(character))))
#---------------------------------------------------------------------------------------------------------------------------------------------->

            if CHECKED == 'L-N-S-U':  

              user = User.objects.create_user(username = name, password = password1, email = email)
              user.save()
              messages.success(request, "User created ✅ ")
              return redirect('/login')
#---------------------------------------------------------------------------------------------------------------------------------------------->
            # either missing one of the field
            elif CHECKED == 'L-N-S':  messages.error(request, 'your password missing uppercase')
            elif CHECKED == 'L-N-U':  messages.error(request, 'your password missing special character')       
            elif CHECKED == 'L-S-U':  messages.error(request, 'your password missing numeric')
            elif CHECKED == 'N-S-U':  messages.error(request, 'your password missing lowercase')
            # either missing two of the field
            elif CHECKED == 'L-N':    messages.error(request, 'your password missing uppercase, special_characters')
            elif CHECKED == 'L-S':    messages.error(request, 'your password missing numeric, uppercase')
            elif CHECKED == 'N-S':    messages.error(request, 'your password missing lowercase, uppercase')
            elif CHECKED == 'L-U':    messages.error(request, 'your password missing special_characters, numeric')
            elif CHECKED == 'N-U':    messages.error(request, 'your password missing lowercase, special special_characters')
            elif CHECKED == 'S-U':    messages.error(request, 'your password missing numeric, lowercase') 
              # which has only one
            elif CHECKED == 'N':      messages.error(request, 'your password missing uppercase, lowercase and special_characters')
            elif CHECKED == 'L':      messages.error(request, 'your password missing uppercase, numeric and special_characters') 
            elif CHECKED == 'U':      messages.error(request, 'your password missing numeric, lowercase and special_characters')  
            elif CHECKED == 'S':      messages.error(request, 'your password missing uppercase, lowercase and special_characters')
            else:                     messages.error(request, 'please enter password') 
          else:                       messages.error(request, 'password not have 8 characters ')
        else: 
          messages.error(request, "password not matching....")  
        
      else:
        messages.error(request, "user name should have more than 3 characters")
    elif name.isdigit():
      messages.error(request, "should be in only alphabetics")
    else:
      messages.error(request, "should not have special characters")


    return redirect('/register')

  else:
    return render(request, 'shop/dup_reg.html')