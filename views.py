from django.shortcuts import render
from django.http import HttpResponse
from math import ceil
from .models import Product, Contact, Orders, OrderUpdate
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides + 1), nSlides])
    bud = {
        'allProds':allProds
        }
    return render(request, 'shop/index.html', bud)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank':thank})

def tracker(request):
        if request.method == "POST":
            orderId = request.POST.get('orderId', '')
            email = request.POST.get('email', '')
            try:
                order = Orders.objects.filter(order_id=orderId, email=email)
                if len(order) > 0:
                    update = OrderUpdate.objects.filter(order_id=orderId)
                    updates = []
                    for item in update:
                        updates.append({'text': item.update_desc, 'time': item.timestamp})
                        response = json.dumps({"status":"success", "updates":updates, "itemjson": order[0].item_json}, default=str)
                    return HttpResponse(response)
                else:
                    return HttpResponse('{"status":"No Item"}')
            except Exception as e:
                return HttpResponse('{"status":"Error"}')

        return render(request, 'shop/tracker.html')

def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.subcategory.lower() or query in item.category.lower():
        return True
    else:
        return False
def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
              allProds.append([prod, range(1, nSlides + 1), nSlides])
    bud = {'allProds': allProds, 'msg': ""}
    if len(allProds) == 0:
        bud = {'msg': "Please make sure to enter relevent search Query."}
    return render(request, 'shop/search.html', bud)

def productview(request, myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/productview.html', {'product':product[0]})

def checkout(request):
    if request.method == "POST":
        item_json = request.POST.get('item_json', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(item_json=item_json, name=name, amount=amount, email=email, address=address,
                         city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The Order has been placed.")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html',  {'thank': thank, 'id': id})
        # Request to paytm for amount

    return render(request, 'shop/checkout.html')

@csrf_exempt
def handlerequest(request):
    pass