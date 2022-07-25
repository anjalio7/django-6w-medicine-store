from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError

from .models import Diseases, Medicine, user


# Create your views here.
def index(request):
    return render (request,'sliced/layout.html')



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


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "sliced/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = user.objects.create_user(username, email, password)
            user.save()
        except ValidationError as v:
                return render(request, 'sliced/register.html', {'message': 'Characters must be greater than 3.'})
        except IntegrityError:
            return render(request, "sliced/register.html", {
                "message": "Username already taken."
            })
        return render(request, 'sliced/register.html', {"message": 'Registered successfully.'})
    else:
        return render(request, "sliced/register.html")

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
    if request.method =="POST":
        obj = Medicine()
        obj.name = request.POST['dis']
        obj.save()
        return HttpResponseRedirect(reverse('listMedicine'))
    else:
        return render(request, 'sliced/add_medicine.html') 

def edit_medicine(request,ids):
    medicine = Medicine.objects.get(id=ids)
    if request.method =="POST":
        edis = request.POST['dis']
        medicine.name = edis
        medicine.save()
        return HttpResponseRedirect(reverse('listmedicine'))
    else:
        return render(request, 'sliced/edit_medicine.html', {'data': medicine})   

def listmedicine(request):
    data = Medicine.objects.all()
    return render(request, 'sliced/list_medicine.html', {'data': data})

def deletemedicine(request, ids):
    data = Medicine.objects.get(id = ids)
    data.delete()
    return HttpResponseRedirect(reverse('listmedicine'))



