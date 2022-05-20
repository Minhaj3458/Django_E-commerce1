from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .import forms
from .import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.views import generic
# Create your views here.
def Templates_common(request):
    return render(request, 'Templates_common.html')
def Index(request):
    addproduct = models.Product.objects.all()
    Context = {
        'product': addproduct
    }
    return render(request, 'index.html', Context)

def Register(request):
     if request.user.is_authenticated:
         return HttpResponse('you are already ')
     else:
         form = forms.Registerform()
         if request.method == 'post' or request.method == 'POST':
             form = forms.Registerform(request.POST)
             if form.is_valid():
                 form.save()
                 return HttpResponse('your account created')
         context = {
             'form': form
         }
     return render(request, 'register.html', context)
def Login(request):
    if request.user.is_authenticated:
        return HttpResponse('you are already login')
    else:
        if request.method == 'post' or request.method == 'POST':
            username = request.POST['user']
            password = request.POST['password']
            user =authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponse('you are successfully login')


    return render(request, 'login.html')
class Product_details_view(generic.DetailView):
    model = models.Product
    template_name = 'single-product.html'
    context_object_name = 'prod'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_images'] = models.ProductImages.objects.filter(product=self.object.id)
        return context

#def product_details(request, pk):
    #item = models.Product.objects.get(id=pk)
    #images = models.ProductImages.objects.filter(product=item).order_by(-created_at)
    #context = {
      #  'prod': item
      # 'photos': images
    #}
    #return render(request, 'single-product.html', context)

def add_to_cart(request,pk):
    iteam = get_object_or_404(models.Product, pk=pk)
    order_iteam = models.Cart.objects.get_or_create(item=iteam, user=request.user, purchased=False)
    order_qs = models.Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderiteam.filter(item=iteam).exists():
            order_iteam[0].quantity +=1
            order_iteam[0].save()
            return redirect('EcommerceApp:Index')
        else:
            order.orderiteam.add(order_iteam[0])
            return redirect('EcommerceApp:Index')
    else:
        order = models.Order(user=request.user)
        order.save()
        order.orderiteam.add(order_iteam[0])
        return redirect('EcommerceApp:Index')

def cart_view(request):
    carts = models.Cart.objects.filter(user=request.user, purchased=False)
    orders = models.Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        context = {
            'carts': carts,
            'order': order
        }
        return render(request, 'shopping-cart.html', context)

def remove_item_from_cart(request, pk):
    item = get_object_or_404(models.Product, pk=pk)
    orders = models.Order.objects.filter(user=request.user, ordered=False)
    if orders.exists():
        order = orders[0]
        if order.orderiteam.filter(item=item).exists():
            order_item = models.Cart.objects.filter(item=item, user=request.user,  purchased=False)[0]
            order.orderiteam.remove(order_item)
            order_item.delete()
            return redirect('EcommerceApp:cart_view')
        else:
            return redirect('EcommerceApp:cart_view')
    else:
        return redirect('EcommerceApp:cart_view')
def incresae_cart(request,pk):
    iteam = get_object_or_404(models.Product, pk=pk)
    order_qs = models.Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderiteam.filter(item=iteam).exists():
            order_iteam = models.Cart.objects.filter(item=iteam, user=request.user, purchased=False)[0]
            if order_iteam. quantity >= 1:
               order_iteam.quantity += 1
               order_iteam.save()
               return redirect('EcommerceApp:cart_view')
            else:
                return redirect('EcommerceApp:Index')
        else:
            return redirect('EcommerceApp:Index')
    else:
        return redirect('EcommerceApp:Index')

def decrease_cart(request,pk):
    iteam = get_object_or_404(models.Product, pk=pk)
    order_qs = models.Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderiteam.filter(item=iteam).exists():
            order_iteam = models.Cart.objects.filter(item=iteam, user=request.user, purchased=False)[0]
            if order_iteam. quantity > 1:
               order_iteam.quantity -= 1
               order_iteam.save()
               return redirect('EcommerceApp:cart_view')
            else:
                order.orderiteam.remove(order_iteam)
                order_iteam.delete()
                return redirect('EcommerceApp:Index')
        else:
            return redirect('EcommerceApp:Index')
    else:
        return redirect('EcommerceApp:Index')



def athur_reg(request):

    if request.method=="POST":
        form=forms.SingupFrom(request.POST)
        if form.is_valid():
            form.save()

            return render(request, 'Athur_res.html')

    else:
        form = forms.SingupFrom
        return render(request, 'Athur_res.html', {'form': form})