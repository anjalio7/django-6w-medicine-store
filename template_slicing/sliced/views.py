from dataclasses import dataclass
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError

from .models import Diseases, Medicine, user, Order


# Create your views here.
def index(request):
    disCount = Diseases.objects.all().count()
    medCount = Medicine.objects.all().count()
    orderCount = Order.objects.all().count()
    return render (request,'sliced/home.html', {'disCount': disCount, 'medCount': medCount, 'orderCount': orderCount})



def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username,
        password=password)
        # Check if authentication successful
        if user is not None:
            if user.is_superuser:
                login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "sliced/login.html", {
            "message": "Invalid username and/or password."
        })
    else:
        return render(request, "sliced/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def add_diseases(request):
    if request.method =="POST":
        obj = Diseases()
        obj.name = request.POST['dis']
        obj.save()
        return HttpResponseRedirect(reverse('listDisease'))
    else:
        return render(request, 'sliced/add_diseases.html') 

def edit_diseases(request,ids):
    disease = Diseases.objects.get(id=ids)
    if request.method =="POST":
        edis = request.POST['dis']
        disease.name = edis
        disease.save()
        return HttpResponseRedirect(reverse('listDisease'))
    else:
        return render(request, 'sliced/edit_diseases.html', {'data': disease})

def listDisease(request):
    data = Diseases.objects.all()
    return render(request, 'sliced/list_diseases.html', {'data': data})


def deletedisease(request, ids):
    data = Diseases.objects.get(id = ids)
    data.delete()
    return HttpResponseRedirect(reverse('listDisease'))

#def add_medicine(request):
    #return render( request, 'sliced/add_medicine.html')
    
def add_medicine(request):
    data = Diseases.objects.all()
    if request.method =="POST":
        dis = request.POST['disease-name']
        name = request.POST['name']
        img = request.FILES['image']
        price = request.POST['price']
        mfg = request.POST['mfgdate']
        exp = request.POST['expiry-date']
        manfc = request.POST['manfc']
        desc = request.POST['desc']

        stock = request.POST['stock']

        selDis = Diseases.objects.get(id = dis)

        a = Medicine(Disease_id = selDis, Name = name, Image = img, Price = price, MfgDate = mfg, Expirydate = exp, Description = desc, ManufacturedBy = manfc, stock = stock)
        a.save()
        return HttpResponseRedirect(reverse('listmedicine'))
    else:
        return render(request, 'sliced/add_medicine.html', {'data': data}) 

def edit_medicine(request,ids):
    data = Diseases.objects.all()
    med = Medicine.objects.get(id = ids)
    if request.method =="POST":
        print(request.POST)
        dis = request.POST['disease-name']
        name = request.POST['name']
        img = request.FILES.get('image')
        price = request.POST['price']
        mfg = request.POST.get('mfgdate')
        exp = request.POST.get('expiry-date')
        manfc = request.POST['manfc']
        desc = request.POST['desc']

        stock = request.POST['stock']


        selDis = Diseases.objects.get(id = dis)

        med.Disease_id = selDis
        if img is not None:
            med.Image = img
        if (mfg != ''):
            print('yay')
            med.MfgDate = mfg
        if (exp != ''):
            med.Expirydate = exp
        med.Name = name
        med.Price = price
        med.Description = desc
        med.ManufacturedBy = manfc
        med.stock = stock
        med.save()
        return HttpResponseRedirect(reverse('listmedicine'))
    
    else:
        return render(request, 'sliced/edit_medicine.html', {'data': data, 'med': med})   

def listmedicine(request):
    data = Medicine.objects.all()
    return render(request, 'sliced/list_medicine.html', {'data': data})

def deletemedicine(request, ids):
    data = Medicine.objects.get(id = ids)
    data.delete()
    return HttpResponseRedirect(reverse('listmedicine'))

def allOrders(request):
    data = Order.objects.all()
    print(data)
    return render(request, 'sliced/allOrders.html', {'data': data})

def updateOrder(request, id, type):
    orderData = Order.objects.get(id = id)
    orderData.status = type
    orderData.save()
    if type == 'Accept':
        med = Medicine.objects.get(id = orderData.medicineId.id)
        # print(f'books is {books}')
        med.stock = int(med.stock) - int(orderData.quantity)
        med.save()
    return HttpResponseRedirect(reverse('adminOrders'))