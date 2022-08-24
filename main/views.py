from functools import total_ordering
import re
from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse,HttpResponse
from html5lib import serialize
from .models import CartOrderItems, Category, Product, ProductAttribute, Brand, ProductReview, CartOrder, UserAddressBook
from django.db.models import Max, Min, Count, Avg
from .forms import ReviewForm
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from .serializer import CartSerializer
from django.db.models import Sum
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.conf import settings


def search(request):
	if request.method=='GET':
		str=request.Get.get('gets')
		if str!=None:
			searches=Category.objects.filter(title__icontains=str)
		else:
			print('Not Found')
	return render(request,'categories.html',{'searches':searches})

def Categories(request):
	data=Category.objects.all()
	searches=[]
	if request.method=='GET':
		str=request.GET.get('gets')
		if str!=None:
			searches=Category.objects.filter(title__icontains=str)

	return render(request,'categories.html',{
		'data':data,
		'searches':searches,
	})

	# data=Category.objects.all()
    # return render(request,'categories.html',{'data':data})
    

def brand_list(request):
    data=Brand.objects.all().order_by('-id')
    return render(request,'brand_list.html',{'data':data})

# Product List
def product_list(request):
	total_data=Product.objects.count()
	data=Product.objects.all().order_by('-id')
	min_price=ProductAttribute.objects.aggregate(Min('price'))
	max_price=ProductAttribute.objects.aggregate(Max('price'))
	return render(request,'product_list.html',
		{
			'data':data,
			'total_data':total_data,
			'min_price':min_price,
			'max_price':max_price,
		}
		)

# Product List According to Category
def category_product_list(request,cat_id):
	category=Category.objects.get(id=cat_id)
	data=Product.objects.filter(category=category).order_by('-id')
	return render(request,'cat_productlist.html',{
			'data':data,
			})


def product_detail(request,slug,id):
	#produc_slug=get_object_or_404(Product, slug)
	#category=Category.objects
	all_products=Product.objects.all()
	product=Product.objects.get(id=id)
	related_products=Product.objects.filter(category=product.category).exclude(id=id)[:4]
	colors=ProductAttribute.objects.filter(product=product).values('color__id','color__title','color__color_code').distinct()
	sizes=ProductAttribute.objects.filter(product=product).values('size__id','size__title','price','color__id').distinct()
	reviewForm=ReviewForm() 

	# Check
	canAdd=True
	reviewCheck=ProductReview.objects.filter(user=request.user,product=product).count()
	if request.user.is_authenticated:
		if reviewCheck > 0:
			canAdd=False
	# End

	# Fetch reviews
	reviews=ProductReview.objects.filter(product=product)
	# End

	# Fetch avg rating for reviews
	avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
	# End

	return render(request, 'product_detail.html',{'data':product, 'all':all_products, 'related':related_products,'colors':colors,'sizes':sizes,'reviewForm':reviewForm,'canAdd':canAdd,'reviews':reviews,'avg_reviews':avg_reviews})


#Product List According to Brands
def brand_productList(request, brand_id):
	brand=Brand.objects.get(id=brand_id)
	data=Product.objects.filter(brand=brand).order_by('-id')
	return render(request,'cat_productlist.html',{
		'data':data})


# def search(request):
# 	q=request.GET['q']
# 	data=Product.objects.filter(title__icontains=q).order_by('-id')
# 	return render(request,'search.html',{'data':data})

class API_details(generics.ListCreateAPIView):
	queryset=CartOrderItems.objects.all()
	serializer_class=CartSerializer
	

def cart_list(request,id):
	product=Product.objects.get(id=id)
	Cart=CartOrderItems.objects.all()
	total=CartOrderItems.objects.all().aggregate(Sum('price'))

	# total_amt=CartOrderItems.objects.all().annotate(total_price=Sum('price'))
	# sums=total_amt.first().total_price
	return render(request,'cart.html',{
		'Cart':Cart,
		'total':total,
		'product':product,
		})
	# total_amt=0
	# if 'cartdata' in request.session:
	# 	total_amt=list(request.session['cartdata'])[-1]
	# 	# for p_id,item in request.session['cartdata']:
	# 		#print(type(request.session['cartdata'].items()))    
	# 		#+=item['qty']*item['price']
	# 	print(type(total_amt))
			
	# 	return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	# else:
	# 	return render(request, 'cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt})


def delete_product(request, product_id):
    product_id = int(product_id)
    try:
        product_sel = CartOrderItems.objects.get(id = product_id)
    except CartOrderItems.DoesNotExist:
        return redirect('categories')
    product_sel.delete()
    return redirect('categories')


def update_cart_item(request, Product_id):
	Product_id=int(Product_id)
	
	try:
		product_sel=CartOrderItems.objects.get(id=Product_id)
		quantity=request.GET.get('quantity')
	except CartOrderItems.DoesNotExist:
		return redirect('categories')

	
