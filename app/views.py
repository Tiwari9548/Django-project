from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse
from .models import Product , Customer ,Cart 
from .forms import CustomerRegistrationForm , CustomerProfileForm
from django.contrib import messages
from django.db.models import Q




# Create your views here.
def home(request):
    return render(request,"app/home.html")

def about(request):
    return render(request,"app/about.html")

def contact(request):
    return render(request,"app/contact.html")    

def CategoryView(request,val):
       product=Product.objects.filter(category=val)
    #    title=product.objects.filter(category=val).values('title')
       return render(request,'app/category.html',locals())


def CategoryTitle(request,val):
       product=Product.objects.filter(category=val)
       title=product.objects.filter(category=product[0].category).values('title')
       return render(request,'app/category.html',locals())


def ProductDetail(request,pk):
       product=Product.objects.get(pk=pk)
    #  
       context = {
          'product': product
       }
       return render(request,"app/productdetail.html", context) 


class CustomerRegistrationView(View):
    def get(self,request):
        forms= CustomerRegistrationForm()
        return render (request,'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
           form.save()
           messages.success(request,"congratulation ! user register successfull")
        else:
            messages.warning(request,"invalid input data")
        return render(request,"app/customerregistration.html",locals())

class ProfileView(View):
    def get(self,request):
        forms= CustomerProfileForm()
        return render(request, 'app/profile.html', locals())
    def post(self,request):
        return render(request, 'app/profile.html', locals())  
        form =CustomerProfileForm(request.POST)
        if form.is_valid():
            user= request.user
            name=forms.cleaned_data['name']
            locality= forms.cleaned_data['locality']
            city= forms.cleaned_data['city']
            mobile= forms.cleaned_data['mobile']
            state= forms.cleaned_data['state']
            zipcode= forms.cleaned_data['zipcode']

            reg= Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request,"congratulation ! profiles save successfully")
        else:
            messages.warning(request,"invalid input data")
        return render(request,'app/profile.html',locals())  


def address(request):
        add=Customer.objects.filter(user=request.user)
        return render(request, 'app/address.html',locals())  

class UpdateAddress(View):
    def get(self,request,pk):
        add= Customer.objects.get(pk=pk)
        form= CustomerProfileForm(instance=add)
        return render(request, 'app/updateadd.html',locals())
    def post(self,request,pk):
        forms =CustomerProfileForm(request.POST)
        if forms.is_valid():
            add= Customer.objects.get(pk=pk)
            add.name=forms.cleaned_data['name']
            add.locality= forms.cleaned_data['locality']
            add.city= forms.cleaned_data['city']
            add.mobile= forms.cleaned_data['mobile']
            add.state= forms.cleaned_data['state']
            add.zipcode= forms.cleaned_data['zipcode']
            add.save()
            messages.success(request,"congratulation ! profiles save successfully")
        else:
            messages.warning(request,"invalid input data")
        return redirect("address")                   
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product= Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")  

def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
     value=p.quantity *p.product.discounted_price
     amount= amount + value
    totalamount = amount + 40    
    return render(request, 'app/addtocart.html', locals())

class checkout(View):
    def get(self,request):
        user= request.user  
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value= p.quantity * p.product.discounted_price
            famount= famount + value
        totalamount = famount + 40
        context = {
            'add': add,
            'cart_items': cart_items,
            'totalamount': totalamount
        }
        return render(request, 'app/checkout.html', context)
        
def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity *p.product.discounted_price
            amount= amount + value
        totalamount =  amount + 40    
        data={
              'quantity':c.quantity,
              'amount' :amount,
              'totalamount' :totalamount
        }  
        return JsonResponse(data)        

def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity *p.product.discounted_price
            amount= amount + value
        totalamount =  amount + 40    
        data={
              'quantity':c.quantity,
              'amount' :amount,
              'totalamount' :totalamount
        }  
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity *p.product.discounted_price
            amount= amount + value
        totalamount =  amount + 40    
        data={
              'amount' :amount,
              'totalamount' :totalamount
        }  
        return JsonResponse(data)    

def search(request):
    query = request.GET['search']
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))    
    return render(request, 'app/search.html',locals())
    




       











  